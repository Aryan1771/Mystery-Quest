from django.contrib import admin
from .models import (
    Case, Clue, Suspect, Evidence, WitnessStatement,
    UserCaseProgress, Accusation
)


class ClueInline(admin.TabularInline):
    model = Clue
    extra = 1
    fields = ('title', 'clue_type', 'description')


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1
    fields = ('evidence_type', 'suspect', 'description')


class WitnessStatementInline(admin.TabularInline):
    model = WitnessStatement
    extra = 1
    fields = ('witness_name', 'statement', 'credibility')


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'status', 'correct_suspect', 'created_at')
    list_filter = ('difficulty', 'status')
    search_fields = ('title', 'description', 'background')
    inlines = [ClueInline, EvidenceInline, WitnessStatementInline]
    filter_horizontal = ()


@admin.register(Suspect)
class SuspectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_culprit')
    list_filter = ('is_culprit', 'cases')
    search_fields = ('name', 'profile', 'motive', 'alibi')
    filter_horizontal = ('cases',)


@admin.register(Clue)
class ClueAdmin(admin.ModelAdmin):
    list_display = ('title', 'case', 'clue_type', 'created_at')
    list_filter = ('clue_type', 'case')
    search_fields = ('title', 'description', 'case__title')


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('case', 'evidence_type', 'suspect', 'clue', 'created_at')
    list_filter = ('evidence_type', 'case')
    search_fields = ('description', 'case__title', 'suspect__name')


@admin.register(WitnessStatement)
class WitnessStatementAdmin(admin.ModelAdmin):
    list_display = ('witness_name', 'case', 'credibility', 'created_at')
    list_filter = ('credibility', 'case')
    search_fields = ('witness_name', 'statement', 'case__title')


@admin.register(UserCaseProgress)
class UserCaseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'case', 'completion_status', 'score', 'hints_used', 'started_at', 'completed_at')
    list_filter = ('completion_status', 'case')
    search_fields = ('user__username', 'case__title')
    filter_horizontal = ('collected_clues',)


@admin.register(Accusation)
class AccusationAdmin(admin.ModelAdmin):
    list_display = ('user', 'case', 'selected_suspect', 'correctness', 'submission_date')
    list_filter = ('correctness', 'case')
    search_fields = ('user__username', 'case__title', 'selected_suspect__name')
