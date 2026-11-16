from django import forms
from .models import Case, Clue, Suspect, Accusation


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'background', 'difficulty', 'status', 'solution_explanation', 'correct_suspect', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 3}),
            'background': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 5}),
            'difficulty': forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'}),
            'status': forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'}),
            'solution_explanation': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 4}),
            'correct_suspect': forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'}),
            'image': forms.FileInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
        }


class ClueForm(forms.ModelForm):
    class Meta:
        model = Clue
        fields = ['case', 'title', 'description', 'clue_type', 'image']
        widgets = {
            'case': forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'}),
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 3}),
            'clue_type': forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'}),
            'image': forms.FileInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
        }


class SuspectForm(forms.ModelForm):
    class Meta:
        model = Suspect
        fields = ['name', 'profile', 'motive', 'alibi', 'cases', 'is_culprit', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'profile': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 3}),
            'motive': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 3}),
            'alibi': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 3}),
            'cases': forms.SelectMultiple(attrs={'class': 'form-select bg-dark text-light border-secondary', 'size': 4}),
            'is_culprit': forms.CheckboxInput(attrs={'class': 'form-check-input bg-dark border-secondary'}),
            'image': forms.FileInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
        }


class AccusationForm(forms.ModelForm):
    class Meta:
        model = Accusation
        fields = ['selected_suspect', 'deduction_notes']
        widgets = {
            'selected_suspect': forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary', 'required': 'required'}),
            'deduction_notes': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 4,
                'placeholder': 'Explain your investigative deduction. What evidence breaks their alibi and links them to the crime?'
            }),
        }

    def __init__(self, *args, **kwargs):
        case = kwargs.pop('case', None)
        super().__init__(*args, **kwargs)
        if case:
            self.fields['selected_suspect'].queryset = case.suspects.all()
