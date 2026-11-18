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

    def test_password_reset_email_and_confirmation_flow(self):
        from django.core import mail
        from django.test import override_settings
        from django.urls import reverse
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.client.post(reverse('password_reset'), {'email': self.user.email})
            self.assertRedirects(response, reverse('password_reset_done'))
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn('password reset', mail.outbox[0].subject.lower())

            uid = urlsafe_base64_encode(force_bytes(self.user.pk))
            token = default_token_generator.make_token(self.user)
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            response = self.client.get(reset_url)
            self.assertEqual(response.status_code, 200)
            response = self.client.post(reset_url, {
                'new_password1': 'New-Strong-Password-928!',
                'new_password2': 'New-Strong-Password-928!',
            })
            self.assertRedirects(response, reverse('password_reset_complete'))
            self.user.refresh_from_db()
            self.assertTrue(self.user.check_password('New-Strong-Password-928!'))

    def test_password_reset_page_is_linked_from_login(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, reverse('password_reset'))

    def test_login_rejects_external_next_url(self):
        response = self.client.post(
            reverse('login') + '?next=https://evil.example/',
            {'username': 'test_detective', 'password': 'Password123!'}
        )
        self.assertRedirects(response, reverse('home'))
