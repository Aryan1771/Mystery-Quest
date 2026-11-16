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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_score = models.IntegerField(default=0)
    rank = models.CharField(max_length=50, choices=RANK_CHOICES, default='Rookie Sleuth')
    cases_solved = models.IntegerField(default=0)
    bio = models.TextField(blank=True, default="Specialized in fictional mystery investigations and deductive reasoning.")
    badge_level = models.CharField(max_length=20, default='Bronze')

    class Meta:
        ordering = ['-total_score', '-cases_solved']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} - {self.rank} ({self.total_score} pts)"

    def update_rank_and_score(self, additional_points=0, case_solved=False):
        """Calculates and updates score, solved cases, and rank."""
        if additional_points:
            self.total_score += additional_points
        if case_solved:
            self.cases_solved += 1

        if self.total_score >= 800:
            self.rank = 'Master Detective'
            self.badge_level = 'Platinum'
        elif self.total_score >= 500:
            self.rank = 'Chief Inspector'
            self.badge_level = 'Gold'
        elif self.total_score >= 250:
            self.rank = 'Senior Investigator'
            self.badge_level = 'Silver'
        elif self.total_score >= 100:
            self.rank = 'Junior Detective'
            self.badge_level = 'Bronze'
        else:
            self.rank = 'Rookie Sleuth'
            self.badge_level = 'Cadet'

        self.save()


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """Automatically create UserProfile when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
