from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'total_score', 'cases_solved', 'badge_level')
    list_filter = ('rank', 'badge_level')
    search_fields = ('user__username', 'user__email', 'bio')
    ordering = ('-total_score', '-cases_solved')
