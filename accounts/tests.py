from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.hashers import make_password, check_password


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

    def test_security_question_recovery_changes_password(self):
        from django.contrib.auth.hashers import check_password

        profile = self.user.profile
        profile.security_question = 'birth_city'
        profile.security_answer_hash = make_password('gaya')
        profile.save()
        response = self.client.post(reverse('password_reset'), {'username': self.user.username})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'In which city were you born?')
        response = self.client.post(reverse('password_reset'), {
            'username': self.user.username,
            'security_answer': ' GAYA ',
            'new_password1': 'New-Strong-Password-928!',
            'new_password2': 'New-Strong-Password-928!',
        })
        self.assertRedirects(response, reverse('login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('New-Strong-Password-928!'))

    def test_security_question_answer_is_hashed(self):
        self.client.login(username='test_detective', password='Password123!')
        response = self.client.post(reverse('profile'), {
            'form_type': 'security',
            'security_question': 'birth_city',
            'security_answer': ' Gaya ',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.profile.refresh_from_db()
        self.assertNotEqual(self.user.profile.security_answer_hash, 'gaya')
        self.assertTrue(check_password('gaya', self.user.profile.security_answer_hash))

    def test_profile_prompts_unconfigured_users(self):
        self.client.login(username='test_detective', password='Password123!')
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'ACCOUNT RECOVERY')
        self.assertContains(response, 'security_question')

    def test_password_reset_link_uses_security_question_flow(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, reverse('password_reset'))

    def test_login_rejects_external_next_url(self):
        response = self.client.post(
            reverse('login') + '?next=https://evil.example/',
            {'username': 'test_detective', 'password': 'Password123!'}
        )
        self.assertRedirects(response, reverse('home'))
