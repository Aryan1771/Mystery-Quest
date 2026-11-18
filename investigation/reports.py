import io
import csv
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Case, UserCaseProgress, Accusation
from accounts.models import UserProfile

# ReportLab Imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


@login_required
def generate_case_pdf(request, case_id):
    """
    Generates a formal Detective Investigation Dossier PDF using ReportLab.
    """
    case = get_object_or_404(Case, id=case_id)
    progress = UserCaseProgress.objects.filter(user=request.user, case=case).first()
    active_progress = UserCaseProgress.objects.filter(user=request.user).exclude(
        completion_status='Solved'
    ).order_by('started_at').first()
    if not progress or (progress.completion_status != 'Solved' and
                        (not active_progress or active_progress.case_id != case.id)):
        return HttpResponseForbidden("This dossier is not assigned to your detective account.")
    accusation = Accusation.objects.filter(user=request.user, case=case).order_by('-submission_date').first()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom Detective Dossier Styles
    primary_color = colors.HexColor("#0f172a")  # Deep Navy
    accent_color = colors.HexColor("#b45309")   # Amber / Gold
    muted_color = colors.HexColor("#475569")

    title_style = ParagraphStyle(
        'DossierTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=primary_color,
        spaceAfter=4,
        alignment=1  # Centered
    )

    subtitle_style = ParagraphStyle(
        'DossierSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=accent_color,
        spaceAfter=15,
        alignment=1
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DossierBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.black
    )

    elements = []

    # 1. Header Banner
    elements.append(Paragraph("MYSTERY QUEST – INVESTIGATION DOSSIER", title_style))
    elements.append(Paragraph(f"CONFIDENTIAL CASE FILE: #{case.id:04d} // BUREAU OF INVESTIGATION", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=12))

    # 2. Case Overview Table
    status_str = progress.completion_status if progress else "Under Review"
    score_str = f"{progress.score} Points" if progress else "N/A"
    overview_data = [
        [
            Paragraph(f"<b>Case Title:</b> {case.title}", body_style),
            Paragraph(f"<b>Lead Detective:</b> {request.user.username}", body_style)
        ],
        [
            Paragraph(f"<b>Difficulty:</b> {case.difficulty}", body_style),
            Paragraph(f"<b>Date Filed:</b> {timezone.now().strftime('%Y-%m-%d %H:%M UTC')}", body_style)
        ],
        [
            Paragraph(f"<b>Investigation Status:</b> {status_str}", body_style),
            Paragraph(f"<b>Investigative Score:</b> {score_str}", body_style)
        ],
    ]
    overview_table = Table(overview_data, colWidths=[270, 260])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(overview_table)
    elements.append(Spacer(1, 12))

    # 3. Incident Background & Summary
    elements.append(Paragraph("1. INCIDENT BRIEF & BACKGROUND", section_heading))
    elements.append(Paragraph(case.description, body_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(f"<b>Crime Lore:</b> {case.background}", body_style))
    elements.append(Spacer(1, 10))

    # 4. Collected Clues Section
    elements.append(Paragraph("2. RECOVERED CLUES & FORENSIC ARTIFACTS", section_heading))
    if progress and progress.collected_clues.exists():
        clues_data = [["#", "Clue Title", "Category", "Field Description"]]
        for idx, clue in enumerate(progress.collected_clues.all(), 1):
            clues_data.append([
                str(idx),
                Paragraph(f"<b>{clue.title}</b>", body_style),
                clue.clue_type,
                Paragraph(clue.description, body_style)
            ])
        clue_table = Table(clues_data, colWidths=[25, 120, 85, 300])
        clue_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(clue_table)
    else:
        elements.append(Paragraph("<i>No clues formally logged in this field docket.</i>", body_style))
    elements.append(Spacer(1, 10))

    # 5. Suspect Analysis Section
    elements.append(Paragraph("3. SUSPECT DOSSIER ANALYSIS", section_heading))
    suspects_data = [["Suspect", "Profile / Occupation", "Claimed Alibi", "Investigated Motive"]]
    for s in case.suspects.all():
        suspects_data.append([
            Paragraph(f"<b>{s.name}</b>", body_style),
            Paragraph(s.profile[:80] + '...', body_style),
            Paragraph(s.alibi[:90] + '...', body_style),
            Paragraph(s.motive[:80] + '...', body_style),
        ])
    suspect_table = Table(suspects_data, colWidths=[100, 140, 150, 140])
    suspect_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(suspect_table)
    elements.append(Spacer(1, 10))

    # 6. Final Accusation & Verdict
    elements.append(Paragraph("4. FINAL ACCUSATION & JUDICIAL VERDICT", section_heading))
    if accusation:
        verdict_text = "GUILTY / CASE SOLVED" if accusation.correctness else "INCORRECT / CASE UNSOLVED"
        verdict_color = colors.HexColor("#166534") if accusation.correctness else colors.HexColor("#991b1b")
        acc_data = [
            [
                Paragraph("<b>Accused Suspect:</b>", body_style),
                Paragraph(f"<b>{accusation.selected_suspect.name}</b>", body_style)
            ],
            [
                Paragraph("<b>Official Finding:</b>", body_style),
                Paragraph(f"<font color='{verdict_color.hexval()}'><b>{verdict_text}</b></font>", body_style)
            ],
            [
                Paragraph("<b>Detective Deduction:</b>", body_style),
                Paragraph(accusation.deduction_notes or "No field deduction notes recorded.", body_style)
            ],
            [
                Paragraph("<b>Submission Timestamp:</b>", body_style),
                Paragraph(accusation.submission_date.strftime("%Y-%m-%d %H:%M UTC"), body_style)
            ],
        ]
        acc_table = Table(acc_data, colWidths=[140, 390])
        acc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(acc_table)
    else:
        elements.append(Paragraph("<i>No formal accusation has been filed yet by the lead detective.</i>", body_style))

    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=1, color=muted_color, spaceAfter=8))
    elements.append(Paragraph("OFFICIAL RECORD OF MYSTERY QUEST FORENSIC LAB // CERTIFIED FOR EXAMINATION", subtitle_style))

    doc.build(elements)
    buffer.seek(0)

    filename = f"MysteryQuest_Case_{case.id}_{request.user.username}.pdf"
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def export_cases_csv(request):
    """
    Exports all fictional investigation case records as a downloadable CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mystery_quest_cases.csv"'

    writer = csv.writer(response)
    writer.writerow(['Case ID', 'Title', 'Difficulty', 'Status', 'Suspects Count', 'Clues Count', 'Created At'])

    cases = Case.objects.all().prefetch_related('suspects', 'clues')
    for c in cases:
        writer.writerow([
            c.id,
            c.title,
            c.difficulty,
            c.status,
            c.suspects.count(),
            c.clues.count(),
            c.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response


def export_leaderboard_csv(request):
    """
    Exports the detective rankings leaderboard as a downloadable CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mystery_quest_leaderboard.csv"'

    writer = csv.writer(response)
    writer.writerow(['Rank #', 'Detective Username', 'Rank Title', 'Badge Level', 'Total Score', 'Cases Solved'])

    profiles = UserProfile.objects.select_related('user').order_by('-total_score', '-cases_solved')
    for rank_num, p in enumerate(profiles, 1):
        writer.writerow([
            rank_num,
            p.user.username,
            p.rank,
            p.badge_level,
            p.total_score,
            p.cases_solved
        ])

    return response
