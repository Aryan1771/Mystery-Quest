from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_detective',
            email='test@detective.org',
            password='Password123!'
        )

    def test_user_profile_signal_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.rank, 'Rookie Sleuth')
        self.assertEqual(self.user.profile.total_score, 0)

    def test_rank_update_logic(self):
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

    def test_registration_creates_profile_and_hashed_password(self):
        response = self.client.post(reverse('register'), {
            'username': 'new_detective',
            'email': 'new@detective.org',
            'first_name': 'New',
            'last_name': 'Detective',
            'password1': 'A-Strong-Password-928!',
            'password2': 'A-Strong-Password-928!',
        })
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='new_detective')
        self.assertTrue(user.check_password('A-Strong-Password-928!'))
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_login_and_profile_views(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
        self.assertTrue(self.client.login(
            username='test_detective', password='Password123!'
        ))
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_detective')

    def test_login_rejects_external_next_url(self):
        response = self.client.post(
            reverse('login') + '?next=https://evil.example/',
            {'username': 'test_detective', 'password': 'Password123!'}
        )
        self.assertRedirects(response, reverse('home'))
