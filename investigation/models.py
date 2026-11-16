from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Case(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Solved', 'Solved'),
        ('Archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Executive summary of the crime.")
    background = models.TextField(help_text="Detailed lore, setting, and timeline.")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Medium')
    image = models.ImageField(upload_to='cases/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    solution_explanation = models.TextField(help_text="Comprehensive revelation of the culprit and method.")
    correct_suspect = models.ForeignKey(
        'Suspect',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solved_cases',
        help_text="The true fictional culprit."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.difficulty})"

    @property
    def base_points(self):
        points_map = {'Easy': 100, 'Medium': 150, 'Hard': 200}
        return points_map.get(self.difficulty, 100)


class Suspect(models.Model):
    name = models.CharField(max_length=150)
    profile = models.TextField(help_text="Occupation, relationship to victim, demeanor.")
    motive = models.TextField(help_text="Potential reason for committing the crime.")
    alibi = models.TextField(help_text="Account of whereabouts during the crime.")
    cases = models.ManyToManyField(Case, related_name='suspects', blank=True)
    image = models.ImageField(upload_to='suspects/', blank=True, null=True)
    is_culprit = models.BooleanField(default=False, help_text="True if this suspect is the actual culprit.")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Clue(models.Model):
    CLUE_TYPE_CHOICES = [
        ('Textual', 'Textual Document'),
        ('Physical', 'Physical Evidence'),
        ('Forensic', 'Forensic Analysis'),
        ('Location', 'Location Discovery'),
        ('Digital', 'Digital / Cyber Clue'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='clues')
    title = models.CharField(max_length=150)
    description = models.TextField()
    clue_type = models.CharField(max_length=50, choices=CLUE_TYPE_CHOICES, default='Physical')
    image = models.ImageField(upload_to='clues/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.case.title}] {self.title} ({self.clue_type})"


class Evidence(models.Model):
    EVIDENCE_TYPE_CHOICES = [
        ('Fingerprint', 'Fingerprint Trace'),
        ('Weapon', 'Incriminating Weapon / Object'),
        ('Document', 'Confidential Document'),
        ('CCTV Footage', 'Surveillance / Witness Log'),
        ('Digital Log', 'Digital / Encryption Log'),
        ('Chemical Trace', 'Chemical / Biological Residue'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidence_records')
    suspect = models.ForeignKey(
        Suspect,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence_records'
    )
    description = models.TextField()
    evidence_type = models.CharField(max_length=50, choices=EVIDENCE_TYPE_CHOICES, default='Document')
    clue = models.ForeignKey(
        Clue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence_links'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.case.title} - {self.evidence_type} ({self.suspect.name if self.suspect else 'Unassigned'})"


class WitnessStatement(models.Model):
    CREDIBILITY_CHOICES = [
        ('High', 'High Credibility'),
        ('Medium', 'Medium Credibility'),
        ('Questionable', 'Questionable / Suspicious'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='witness_statements')
    witness_name = models.CharField(max_length=150)
    statement = models.TextField()
    credibility = models.CharField(max_length=30, choices=CREDIBILITY_CHOICES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.witness_name} - {self.case.title} ({self.credibility})"


class UserCaseProgress(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Solved', 'Solved'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_progresses')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='user_progresses')
    collected_clues = models.ManyToManyField(Clue, blank=True, related_name='collected_by_users')
    completion_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='In Progress')
    score = models.IntegerField(default=0)
    hints_used = models.IntegerField(default=0)
    investigation_notes = models.TextField(blank=True, default='', help_text="Detective's personal field notes and scratchpad.")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'case')
        verbose_name = 'User Case Progress'
        verbose_name_plural = 'User Case Progresses'

    def __str__(self):
        return f"{self.user.username} - {self.case.title} ({self.completion_status})"

    @property
    def progress_percentage(self):
        total = self.case.clues.count()
        if total == 0:
            return 100 if self.completion_status == 'Solved' else 0
        collected = self.collected_clues.count()
        return min(int((collected / total) * 100), 100)


class Accusation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accusations')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='accusations')
    selected_suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE, related_name='accusations')
    correctness = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    deduction_notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-submission_date']

    def __str__(self):
        verdict = "CORRECT" if self.correctness else "INCORRECT"
        return f"{self.user.username} accused {self.selected_suspect.name} on {self.case.title} - {verdict}"
