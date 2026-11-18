from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    RANK_CHOICES = [
        ('Rookie Sleuth', 'Rookie Sleuth'),
        ('Junior Detective', 'Junior Detective'),
        ('Senior Investigator', 'Senior Investigator'),
        ('Chief Inspector', 'Chief Inspector'),
        ('Master Detective', 'Master Detective'),
    ]

    SECURITY_QUESTION_CHOICES = [
        ('first_school', 'What was the name of your first school?'),
        ('childhood_friend', 'What was the first name of your childhood best friend?'),
        ('birth_city', 'In which city were you born?'),
        ('favorite_teacher', 'What was the surname of a favorite teacher?'),
        ('memorable_place', 'What was the name of a memorable place from your childhood?'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_score = models.IntegerField(default=0)
    rank = models.CharField(max_length=50, choices=RANK_CHOICES, default='Rookie Sleuth')
    cases_solved = models.IntegerField(default=0)
    bio = models.TextField(blank=True, default="Specialized in fictional mystery investigations and deductive reasoning.")
    badge_level = models.CharField(max_length=20, default='Bronze')
    security_question = models.CharField(max_length=32, choices=SECURITY_QUESTION_CHOICES, blank=True, default='')
    security_answer_hash = models.CharField(max_length=128, blank=True, default='')

    @property
    def has_recovery_setup(self):
        return bool(self.security_question and self.security_answer_hash)

    class Meta:
        ordering = ['-total_score', '-cases_solved']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} - {self.rank} ({self.total_score} pts)"

    def update_rank_and_score(self, additional_points=0, case_solved=False):
        if additional_points:
            self.total_score += additional_points
        if case_solved:
            self.cases_solved += 1

        if self.total_score >= 800:
            self.rank, self.badge_level = 'Master Detective', 'Platinum'
        elif self.total_score >= 500:
            self.rank, self.badge_level = 'Chief Inspector', 'Gold'
        elif self.total_score >= 250:
            self.rank, self.badge_level = 'Senior Investigator', 'Silver'
        elif self.total_score >= 100:
            self.rank, self.badge_level = 'Junior Detective', 'Bronze'
        else:
            self.rank, self.badge_level = 'Rookie Sleuth', 'Cadet'
        self.save()


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """Ensure users have a profile; get_or_create is safe for repeated saves."""
    profile, profile_created = UserProfile.objects.get_or_create(user=instance)
    if not profile_created and not created:
        profile.save()
