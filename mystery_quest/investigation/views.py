from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import (
    Case, Clue, Suspect, Evidence, WitnessStatement,
    UserCaseProgress, Accusation
)
from accounts.models import UserProfile
from .forms import CaseForm, ClueForm, SuspectForm, AccusationForm
from .hint_engine import generate_investigative_hint


def home_view(request):
    """Landing homepage with investigation highlights, detective stats, and top ranking detectives."""
    cases = Case.objects.all()[:3]
    top_detectives = UserProfile.objects.select_related('user').order_by('-total_score', '-cases_solved')[:5]
    total_cases = Case.objects.count()
    total_solved = UserCaseProgress.objects.filter(completion_status='Solved').count()

    user_stats = None
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        active_investigations = UserCaseProgress.objects.filter(user=request.user, completion_status='In Progress').count()
        user_stats = {
            'profile': profile,
            'active_investigations': active_investigations,
        }

    context = {
        'featured_cases': cases,
        'top_detectives': top_detectives,
        'total_cases': total_cases,
        'total_solved': total_solved,
        'user_stats': user_stats,
    }
    return render(request, 'home.html', context)


def case_list_view(request):
    """Displays all fictional investigation cases with filter by difficulty and search."""
    difficulty = request.GET.get('difficulty', '')
    query = request.GET.get('q', '').strip()

    cases = Case.objects.all().prefetch_related('clues', 'suspects')

    if difficulty in ['Easy', 'Medium', 'Hard']:
        cases = cases.filter(difficulty=difficulty)

    if query:
        cases = cases.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(background__icontains=query)
        )

    user_progress_map = {}
    if request.user.is_authenticated:
        progresses = UserCaseProgress.objects.filter(user=request.user)
        for p in progresses:
            user_progress_map[p.case_id] = p

    cases_with_status = []
    for c in cases:
        prog = user_progress_map.get(c.id)
        cases_with_status.append({
            'case': c,
            'progress': prog,
        })

    context = {
        'cases_with_status': cases_with_status,
        'selected_difficulty': difficulty,
        'search_query': query,
    }
    return render(request, 'investigation/case_list.html', context)


def case_detail_view(request, case_id):
    """Case dossier briefing and entry portal."""
    case = get_object_or_404(Case, id=case_id)
    progress = None
    if request.user.is_authenticated:
        progress = UserCaseProgress.objects.filter(user=request.user, case=case).first()

    context = {
        'case': case,
        'progress': progress,
        'suspects_count': case.suspects.count(),
        'clues_count': case.clues.count(),
    }
    return render(request, 'investigation/case_detail.html', context)


@login_required
def start_investigation_view(request, case_id):
    """Starts or resumes an investigation for the authenticated detective."""
    case = get_object_or_404(Case, id=case_id)
    progress, created = UserCaseProgress.objects.get_or_create(
        user=request.user,
        case=case,
        defaults={'completion_status': 'In Progress'}
    )
    if created:
        messages.success(request, f"Dossier opened: Investigation into '{case.title}' officially begun!")
    return redirect('investigate', case_id=case.id)


@login_required
def investigate_view(request, case_id):
    """
    Main interactive investigation room:
    Displays clues, evidence, suspects, witness testimonies, hint panel, and accusation chamber.
    """
    case = get_object_or_404(Case, id=case_id)
    progress, _ = UserCaseProgress.objects.get_or_create(
        user=request.user,
        case=case,
        defaults={'completion_status': 'In Progress'}
    )

    collected_clue_ids = progress.collected_clues.values_list('id', flat=True)
    all_clues = case.clues.all()
    suspects = case.suspects.all()
    evidence_records = case.evidence_records.all().select_related('suspect', 'clue')
    witness_statements = case.witness_statements.all()
    latest_accusation = Accusation.objects.filter(user=request.user, case=case).order_by('-submission_date').first()

    accusation_form = AccusationForm(case=case)

    context = {
        'case': case,
        'progress': progress,
        'collected_clue_ids': set(collected_clue_ids),
        'all_clues': all_clues,
        'suspects': suspects,
        'evidence_records': evidence_records,
        'witness_statements': witness_statements,
        'latest_accusation': latest_accusation,
        'accusation_form': accusation_form,
    }
    return render(request, 'investigation/investigate.html', context)


@login_required
def collect_clue_view(request, case_id, clue_id):
    """Collects an investigation clue and adds it to the detective's progress."""
    case = get_object_or_404(Case, id=case_id)
    clue = get_object_or_404(Clue, id=clue_id, case=case)
    progress, _ = UserCaseProgress.objects.get_or_create(user=request.user, case=case)

    if clue not in progress.collected_clues.all():
        progress.collected_clues.add(clue)
        collected = True
        msg = f"Clue cataloged: {clue.title} ({clue.clue_type})"
    else:
        collected = False
        msg = f"Clue {clue.title} is already recorded in your notebook."

    # Return JSON for AJAX fetch call or redirect for standard POST
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({
            'success': True,
            'collected': collected,
            'message': msg,
            'clue_id': clue.id,
            'clue_title': clue.title,
            'clue_type': clue.clue_type,
            'clue_desc': clue.description,
            'progress_percent': progress.progress_percentage,
            'collected_count': progress.collected_clues.count(),
            'total_count': case.clues.count(),
        })

    messages.success(request, msg)
    return redirect('investigate', case_id=case.id)


@login_required
def get_hint_view(request, case_id):
    """Rule-based AI hint generator endpoint."""
    case = get_object_or_404(Case, id=case_id)
    progress, _ = UserCaseProgress.objects.get_or_create(user=request.user, case=case)

    hint_data = generate_investigative_hint(case, progress.collected_clues.all())

    # Increment hint tally
    progress.hints_used += 1
    progress.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({
            'success': True,
            'hint': hint_data['hint'],
            'level': hint_data['level'],
            'focus_area': hint_data['focus_area'],
            'penalty': hint_data['penalty'],
            'hints_used': progress.hints_used,
        })

    messages.info(request, f"AI Hint ({hint_data['level']}): {hint_data['hint']}")
    return redirect('investigate', case_id=case.id)


@login_required
def submit_accusation_view(request, case_id):
    """Validates the detective's accusation against the case solution and calculates score."""
    case = get_object_or_404(Case, id=case_id)
    progress, _ = UserCaseProgress.objects.get_or_create(user=request.user, case=case)

    if request.method == 'POST':
        form = AccusationForm(request.POST, case=case)
        if form.is_valid():
            selected_suspect = form.cleaned_data['selected_suspect']
            deduction_notes = form.cleaned_data['deduction_notes']

            # Check correctness against fictional culprit
            is_correct = (selected_suspect == case.correct_suspect) or (selected_suspect.is_culprit)

            # Record accusation
            Accusation.objects.create(
                user=request.user,
                case=case,
                selected_suspect=selected_suspect,
                correctness=is_correct,
                deduction_notes=deduction_notes
            )

            if is_correct:
                # Calculate score
                base = case.base_points
                clues_bonus = progress.collected_clues.count() * 10
                hints_penalty = progress.hints_used * 15
                earned_score = max(50, base + clues_bonus - hints_penalty)

                # Check if already solved previously to prevent repeat score exploits
                previously_solved = (progress.completion_status == 'Solved')

                progress.completion_status = 'Solved'
                progress.score = earned_score
                progress.completed_at = timezone.now()
                progress.save()

                if not previously_solved:
                    profile, _ = UserProfile.objects.get_or_create(user=request.user)
                    profile.update_rank_and_score(additional_points=earned_score, case_solved=True)

                messages.success(
                    request,
                    f"BRILLIANT DEDUCTION! {selected_suspect.name} has confessed to the crime! "
                    f"You earned {earned_score} points for solving this case."
                )
            else:
                progress.completion_status = 'Failed'
                progress.save()
                messages.error(
                    request,
                    f"INVESTIGATION FLAWED! {selected_suspect.name}'s alibi holds firm. "
                    "Re-examine the evidence and clues before attempting another accusation."
                )

            return redirect('investigate', case_id=case.id)

    return redirect('investigate', case_id=case.id)


def leaderboard_view(request):
    """Dynamic Leaderboard displaying detective rankings and stats."""
    detectives = UserProfile.objects.select_related('user').order_by('-total_score', '-cases_solved')

    current_user_rank = None
    if request.user.is_authenticated:
        for idx, det in enumerate(detectives, 1):
            if det.user == request.user:
                current_user_rank = idx
                break

    context = {
        'detectives': detectives,
        'current_user_rank': current_user_rank,
    }
    return render(request, 'investigation/leaderboard.html', context)


def ajax_search_view(request):
    """
    AJAX Live Search endpoint.
    Returns JSON formatted matching cases, clues, and suspects in real time.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'all').lower()

    if not query:
        return JsonResponse({'query': '', 'cases': [], 'clues': [], 'suspects': [], 'total_count': 0})

    results = {'query': query, 'cases': [], 'clues': [], 'suspects': [], 'total_count': 0}

    # Search Cases
    if category in ['all', 'cases']:
        cases = Case.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(background__icontains=query)
        )[:6]
        for c in cases:
            results['cases'].append({
                'id': c.id,
                'title': c.title,
                'difficulty': c.difficulty,
                'status': c.status,
                'description': c.description[:120] + ('...' if len(c.description) > 120 else ''),
                'url': f'/case/{c.id}/',
            })

    # Search Clues
    if category in ['all', 'clues']:
        clues = Clue.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).select_related('case')[:6]
        for cl in clues:
            results['clues'].append({
                'id': cl.id,
                'title': cl.title,
                'clue_type': cl.clue_type,
                'case_id': cl.case.id,
                'case_title': cl.case.title,
                'description': cl.description[:120] + ('...' if len(cl.description) > 120 else ''),
                'url': f'/case/{cl.case.id}/investigate/',
            })

    # Search Suspects
    if category in ['all', 'suspects']:
        suspects = Suspect.objects.filter(
            Q(name__icontains=query) |
            Q(profile__icontains=query) |
            Q(motive__icontains=query)
        )[:6]
        for s in suspects:
            results['suspects'].append({
                'id': s.id,
                'name': s.name,
                'profile': s.profile[:120] + ('...' if len(s.profile) > 120 else ''),
                'motive': s.motive[:100] + ('...' if len(s.motive) > 100 else ''),
            })

    results['total_count'] = len(results['cases']) + len(results['clues']) + len(results['suspects'])
    return JsonResponse(results)


def search_page_view(request):
    """Dedicated interactive search page showcasing the AJAX Live Search system."""
    return render(request, 'investigation/search.html')


@login_required
def save_case_notes_view(request, case_id):
    """Saves the detective's personal field notes and scratchpad for a case."""
    case = get_object_or_404(Case, id=case_id)
    progress, _ = UserCaseProgress.objects.get_or_create(user=request.user, case=case)

    if request.method == 'POST':
        notes = request.POST.get('notes', '').strip()
        progress.investigation_notes = notes
        progress.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({
                'success': True,
                'message': 'Field notes saved to case docket archive.',
                'timestamp': timezone.now().strftime('%H:%M:%S UTC'),
            })

        messages.success(request, "Field notes successfully updated.")
        return redirect('investigate', case_id=case.id)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


def crime_lab_view(request):
    """Interactive Forensic Crime Lab, Evidence Clinic & Decryption Station across ALL cases."""
    import json
    cases = Case.objects.all().prefetch_related('clues', 'suspects', 'evidence_records').order_by('id')
    evidence_list = Evidence.objects.all().select_related('case', 'suspect', 'clue').order_by('case__id', 'id')

    # Prepare complete data payload for interactive frontend forensics across all cases
    cases_data = []
    for c in cases:
        case_ev_list = []
        for e in c.evidence_records.all():
            case_ev_list.append({
                'id': e.id,
                'evidence_type': e.evidence_type,
                'description': e.description,
                'suspect_id': e.suspect.id if e.suspect else None,
                'suspect_name': e.suspect.name if e.suspect else 'Unassigned / Scene Trace',
                'clue_title': e.clue.title if e.clue else 'General Crime Scene Discovery',
            })

        case_susp_list = []
        for s in c.suspects.all():
            case_susp_list.append({
                'id': s.id,
                'name': s.name,
                'profile': s.profile,
                'is_culprit': s.is_culprit,
            })

        case_clue_list = []
        for cl in c.clues.all():
            case_clue_list.append({
                'id': cl.id,
                'title': cl.title,
                'clue_type': cl.clue_type,
                'description': cl.description,
            })

        cases_data.append({
            'id': c.id,
            'title': c.title,
            'difficulty': c.difficulty,
            'status': c.status,
            'evidence': case_ev_list,
            'suspects': case_susp_list,
            'clues': case_clue_list,
        })

    return render(request, 'investigation/crime_lab.html', {
        'cases': cases,
        'evidence_list': evidence_list,
        'cases_json': json.dumps(cases_data),
    })


# ==========================================
# CRUD Operations (Restricted to Staff/Admin)
# ==========================================

def staff_required(view_func):
    """Decorator to enforce staff authorization."""
    return user_passes_test(lambda u: u.is_authenticated and (u.is_staff or u.is_superuser), login_url='login')(view_func)


@staff_required
def crud_dashboard_view(request):
    """Admin CRUD management dashboard."""
    cases = Case.objects.all()
    clues = Clue.objects.all().select_related('case')
    suspects = Suspect.objects.all()

    context = {
        'cases': cases,
        'clues': clues,
        'suspects': suspects,
    }
    return render(request, 'investigation/crud_dashboard.html', context)


# --- Case CRUD ---
@staff_required
def case_create_view(request):
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save()
            messages.success(request, f"Case '{case.title}' created successfully.")
            return redirect('crud_dashboard')
    else:
        form = CaseForm()
    return render(request, 'investigation/case_form.html', {'form': form, 'title': 'Create New Case'})


@staff_required
def case_update_view(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, f"Case '{case.title}' updated successfully.")
            return redirect('crud_dashboard')
    else:
        form = CaseForm(instance=case)
    return render(request, 'investigation/case_form.html', {'form': form, 'title': f'Edit Case: {case.title}', 'case': case})


@staff_required
def case_delete_view(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        title = case.title
        case.delete()
        messages.success(request, f"Case '{title}' deleted permanently.")
        return redirect('crud_dashboard')
    return render(request, 'investigation/confirm_delete.html', {'object': case, 'type': 'Case'})


# --- Clue CRUD ---
@staff_required
def clue_create_view(request):
    if request.method == 'POST':
        form = ClueForm(request.POST, request.FILES)
        if form.is_valid():
            clue = form.save()
            messages.success(request, f"Clue '{clue.title}' created successfully.")
            return redirect('crud_dashboard')
    else:
        form = ClueForm()
    return render(request, 'investigation/clue_form.html', {'form': form, 'title': 'Add New Clue'})


@staff_required
def clue_update_view(request, clue_id):
    clue = get_object_or_404(Clue, id=clue_id)
    if request.method == 'POST':
        form = ClueForm(request.POST, request.FILES, instance=clue)
        if form.is_valid():
            form.save()
            messages.success(request, f"Clue '{clue.title}' updated successfully.")
            return redirect('crud_dashboard')
    else:
        form = ClueForm(instance=clue)
    return render(request, 'investigation/clue_form.html', {'form': form, 'title': f'Edit Clue: {clue.title}', 'clue': clue})


@staff_required
def clue_delete_view(request, clue_id):
    clue = get_object_or_404(Clue, id=clue_id)
    if request.method == 'POST':
        title = clue.title
        clue.delete()
        messages.success(request, f"Clue '{title}' deleted permanently.")
        return redirect('crud_dashboard')
    return render(request, 'investigation/confirm_delete.html', {'object': clue, 'type': 'Clue'})


# --- Suspect CRUD ---
@staff_required
def suspect_create_view(request):
    if request.method == 'POST':
        form = SuspectForm(request.POST, request.FILES)
        if form.is_valid():
            suspect = form.save()
            messages.success(request, f"Suspect '{suspect.name}' created successfully.")
            return redirect('crud_dashboard')
    else:
        form = SuspectForm()
    return render(request, 'investigation/suspect_form.html', {'form': form, 'title': 'Register New Suspect'})


@staff_required
def suspect_update_view(request, suspect_id):
    suspect = get_object_or_404(Suspect, id=suspect_id)
    if request.method == 'POST':
        form = SuspectForm(request.POST, request.FILES, instance=suspect)
        if form.is_valid():
            form.save()
            messages.success(request, f"Suspect '{suspect.name}' updated successfully.")
            return redirect('crud_dashboard')
    else:
        form = SuspectForm(instance=suspect)
    return render(request, 'investigation/suspect_form.html', {'form': form, 'title': f'Edit Suspect: {suspect.name}', 'suspect': suspect})


@staff_required
def suspect_delete_view(request, suspect_id):
    suspect = get_object_or_404(Suspect, id=suspect_id)
    if request.method == 'POST':
        name = suspect.name
        suspect.delete()
        messages.success(request, f"Suspect '{name}' deleted permanently.")
        return redirect('crud_dashboard')
    return render(request, 'investigation/confirm_delete.html', {'object': suspect, 'type': 'Suspect'})
