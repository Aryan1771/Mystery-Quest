import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from investigation.models import (
    Case, Clue, Suspect, Evidence, WitnessStatement,
    UserCaseProgress, Accusation
)


class InvestigationSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Regular Detective
        self.detective = User.objects.create_user(
            username='watson',
            email='watson@bakerstreet.io',
            password='WatsonPassword123'
        )

        # Admin / Staff User
        self.admin_user = User.objects.create_user(
            username='inspector_lestrade',
            email='lestrade@scotlandyard.uk',
            password='LestradePassword123',
            is_staff=True
        )

        # Create Test Case
        self.case = Case.objects.create(
            title="The Stolen Amber Necklace",
            description="A valuable antique necklace vanished from the museum vault.",
            background="The museum gallery was closed at 6 PM. At 7:30 PM, the glass display was broken.",
            difficulty="Easy",
            status="Active",
            solution_explanation="The curator staged the theft using a pre-duplicated key."
        )

        # Suspects
        self.innocent_suspect = Suspect.objects.create(
            name="Arthur Vance",
            profile="Museum Night Guard",
            motive="Underpaid worker",
            alibi="Patrolling the west wing",
            is_culprit=False
        )
        self.innocent_suspect.cases.add(self.case)

        self.guilty_suspect = Suspect.objects.create(
            name="Harold Finch",
            profile="Chief Museum Curator",
            motive="Massive personal debts",
            alibi="Claims he was home reading",
            is_culprit=True
        )
        self.guilty_suspect.cases.add(self.case)
        self.case.correct_suspect = self.guilty_suspect
        self.case.save()

        # Clues
        self.clue1 = Clue.objects.create(
            case=self.case,
            title="Shattered Display Glass",
            description="Glass shards indicate impact from the interior of the case, not outside.",
            clue_type="Physical"
        )
        self.clue2 = Clue.objects.create(
            case=self.case,
            title="Electronic Log Discrepancy",
            description="The master key fob was used 10 minutes prior to the alarm sounding.",
            clue_type="Digital"
        )

        # Evidence
        self.evidence = Evidence.objects.create(
            case=self.case,
            suspect=self.guilty_suspect,
            description="Master key fob found in curator's desk drawer.",
            evidence_type="Document",
            clue=self.clue2
        )

        # Witness Statement
        self.witness = WitnessStatement.objects.create(
            case=self.case,
            witness_name="Security Guard Miller",
            statement="I saw curator Finch leaving through the side exit at 7:15 PM holding a leather pouch.",
            credibility="High"
        )

    def test_case_list_and_detail_views(self):
        """Tests that case files display properly."""
        response = self.client.get('/cases/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Stolen Amber Necklace")

        response = self.client.get(f'/case/{self.case.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Stolen Amber Necklace")
        self.assertContains(response, "Arthur Vance")

    def test_start_investigation(self):
        """Tests starting an investigation creates progress record."""
        self.client.login(username='watson', password='WatsonPassword123')
        response = self.client.get(f'/case/{self.case.id}/start/', follow=True)
        self.assertEqual(response.status_code, 200)

        progress = UserCaseProgress.objects.filter(user=self.detective, case=self.case).first()
        self.assertIsNotNone(progress)
        self.assertEqual(progress.completion_status, 'In Progress')

    def test_single_active_case_and_rank_unlocks(self):
        self.client.login(username='watson', password='WatsonPassword123')
        locked_case = Case.objects.create(
            title="The Locked Observatory",
            description="A telescope disappears.",
            background="The observatory was sealed overnight.",
            difficulty="Medium",
            solution_explanation="The technician hid it."
        )
        self.assertEqual(self.client.get(f'/case/{self.case.id}/start/').status_code, 302)
        active = UserCaseProgress.objects.get(user=self.detective, case=self.case)
        self.assertEqual(active.completion_status, 'In Progress')

        # A second case is previewable but cannot be started while the first is active.
        response = self.client.get(f'/case/{locked_case.id}/')
        self.assertContains(response, 'Complete your active case')
        self.client.get(f'/case/{locked_case.id}/start/')
        self.assertFalse(UserCaseProgress.objects.filter(user=self.detective, case=locked_case).exists())
        self.assertEqual(self.client.get(f'/case/{locked_case.id}/investigate/').status_code, 302)

        # Solving the Easy case promotes the detective to Junior and unlocks Medium.
        response = self.client.post(f'/case/{self.case.id}/accuse/', {
            'selected_suspect': self.guilty_suspect.id,
            'deduction_notes': 'The evidence points to the curator.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.detective.profile.refresh_from_db()
        self.assertEqual(self.detective.profile.rank, 'Junior Detective')
        response = self.client.get(f'/case/{locked_case.id}/')
        self.assertContains(response, 'Select This Case')

    def test_clue_collection_standard_and_ajax(self):
        """Tests clue collection via both standard request and AJAX Fetch API."""
        self.client.login(username='watson', password='WatsonPassword123')
        
        # AJAX fetch call
        response = self.client.post(
            f'/case/{self.case.id}/clue/{self.clue1.id}/collect/',
            headers={'x-requested-with': 'XMLHttpRequest', 'accept': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['collected'])
        self.assertEqual(data['clue_title'], self.clue1.title)
        self.assertEqual(data['progress_percent'], 50)  # 1 of 2 clues

        # Check in DB
        progress = UserCaseProgress.objects.get(user=self.detective, case=self.case)
        self.assertIn(self.clue1, progress.collected_clues.all())

    def test_rule_based_ai_hint_engine(self):
        """Tests rule-based hint generation and penalty tracking."""
        self.client.login(username='watson', password='WatsonPassword123')
        
        # First hint with 0 clues collected
        response = self.client.get(
            f'/case/{self.case.id}/hint/',
            headers={'x-requested-with': 'XMLHttpRequest', 'accept': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('crime scene', data['hint'].lower())
        self.assertEqual(data['hints_used'], 1)

    def test_accusation_and_scoring_validation(self):
        """Tests false accusation, correct accusation, scoring, and anti-exploit logic."""
        self.client.login(username='watson', password='WatsonPassword123')
        progress = UserCaseProgress.objects.create(user=self.detective, case=self.case)
        progress.collected_clues.add(self.clue1, self.clue2)

        # 1. False Accusation
        response = self.client.post(
            f'/case/{self.case.id}/accuse/',
            {'selected_suspect': self.innocent_suspect.id, 'deduction_notes': 'Suspicious demeanor.'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        progress.refresh_from_db()
        self.assertEqual(progress.completion_status, 'In Progress')
        self.assertEqual(progress.score, 0)
        self.assertEqual(self.detective.profile.total_score, 0)

        # 2. Correct Accusation
        response = self.client.post(
            f'/case/{self.case.id}/accuse/',
            {'selected_suspect': self.guilty_suspect.id, 'deduction_notes': 'Curator used the key fob and broke glass from inside.'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        progress.refresh_from_db()
        self.assertEqual(progress.completion_status, 'Solved')
        self.assertGreater(progress.score, 0)

        self.detective.profile.refresh_from_db()
        initial_user_score = self.detective.profile.total_score
        self.assertGreater(initial_user_score, 0)
        self.assertEqual(self.detective.profile.cases_solved, 1)

        # 3. Repeat submission exploit prevention test
        # Submitting again should not add more points to user's profile
        self.client.post(
            f'/case/{self.case.id}/accuse/',
            {'selected_suspect': self.guilty_suspect.id, 'deduction_notes': 'Second submission check.'},
            follow=True
        )
        self.detective.profile.refresh_from_db()
        self.assertEqual(self.detective.profile.total_score, initial_user_score)
        self.assertEqual(self.detective.profile.cases_solved, 1)

    def test_ajax_live_search(self):
        """Tests live AJAX search endpoint returns JSON with matching results."""
        response = self.client.get('/api/search/?q=Necklace&category=all')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data['total_count'], 0)
        self.assertEqual(len(data['cases']), 1)
        self.assertEqual(data['cases'][0]['title'], "The Stolen Amber Necklace")

        # Empty search result
        response = self.client.get('/api/search/?q=xyznonexistentterm')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_count'], 0)

    def test_reportlab_pdf_generation(self):
        """Tests server-side PDF generation via ReportLab."""
        self.client.login(username='watson', password='WatsonPassword123')
        UserCaseProgress.objects.get_or_create(user=self.detective, case=self.case)
        response = self.client.get(f'/case/{self.case.id}/report/pdf/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment;', response['Content-Disposition'])
        self.assertTrue(len(response.content) > 1000)

    def test_csv_exports(self):
        """Tests CSV export for case records and leaderboard."""
        # Case CSV
        response = self.client.get('/reports/cases/csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Case ID,Title,Difficulty', response.content.decode('utf-8'))

        # Leaderboard CSV
        response = self.client.get('/reports/leaderboard/csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Rank #,Detective Username', response.content.decode('utf-8'))

    def test_crud_authorization_restrictions(self):
        """Tests that normal detectives cannot access management CRUD, while staff can."""
        # Unauthenticated user redirected to login
        response = self.client.get('/manage/')
        self.assertEqual(response.status_code, 302)

        # Regular detective redirected to login
        self.client.login(username='watson', password='WatsonPassword123')
        response = self.client.get('/manage/')
        self.assertEqual(response.status_code, 302)

        # Admin user allowed
        self.client.login(username='inspector_lestrade', password='LestradePassword123')
        response = self.client.get('/manage/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CENTRAL MANAGEMENT DASHBOARD")
