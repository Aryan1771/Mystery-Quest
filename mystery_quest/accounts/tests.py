from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_detective',
            email='test@detective.org',
            password='Password123!'
        )

    def test_user_profile_signal_creation(self):
        """Tests that UserProfile is automatically created via post_save signal."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.rank, 'Rookie Sleuth')
        self.assertEqual(self.user.profile.total_score, 0)

    def test_rank_update_logic(self):
        """Tests score addition and rank updates."""
        profile = self.user.profile
        profile.update_rank_and_score(additional_points=120, case_solved=True)
        self.assertEqual(profile.total_score, 120)
        self.assertEqual(profile.cases_solved, 1)
        self.assertEqual(profile.rank, 'Junior Detective')

        profile.update_rank_and_score(additional_points=400, case_solved=True)
        self.assertEqual(profile.total_score, 520)
        self.assertEqual(profile.cases_solved, 2)
        self.assertEqual(profile.rank, 'Chief Inspector')

        profile.update_rank_and_score(additional_points=300, case_solved=True)
        self.assertEqual(profile.total_score, 820)
        self.assertEqual(profile.rank, 'Master Detective')

    def test_login_and_profile_views(self):
        """Tests authentication access."""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        # Log in
        login_success = self.client.login(username='test_detective', password='Password123!')
        self.assertTrue(login_success)

        # Profile view
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_detective')
