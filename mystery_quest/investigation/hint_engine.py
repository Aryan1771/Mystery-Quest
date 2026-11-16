"""
Rule-Based AI Hint Engine for Mystery Quest.
Generates progressive investigative hints based on collected clues,
witness testimonies, and suspect alibis without revealing the solution directly.
"""

def generate_investigative_hint(case, collected_clues_queryset):
    """
    Analyzes current case progress and returns intelligent, rule-based deductive guidance.
    """
    total_clues_count = case.clues.count()
    collected_count = collected_clues_queryset.count()
    collected_types = set(collected_clues_queryset.values_list('clue_type', flat=True))
    all_clues = list(case.clues.all())

    # Stage 1: Zero clues collected
    if collected_count == 0:
        return {
            'level': 'Beginner Guidance',
            'hint': "Detective, you haven't inspected the crime scene yet! Start by examining physical and location clues to anchor your investigation timeline.",
            'focus_area': 'Crime Scene Examination',
            'penalty': 15
        }

    # Stage 2: 1 clue collected - push towards diverse evidence types
    if collected_count == 1:
        uncollected_types = [c.clue_type for c in all_clues if c not in collected_clues_queryset]
        target_type = uncollected_types[0] if uncollected_types else 'Forensic'
        return {
            'level': 'Intermediate Clue Lead',
            'hint': f"You've found an initial trace, but one angle is not enough. Focus on uncovering a {target_type} clue to substantiate how the perpetrator bypassed security.",
            'focus_area': f'{target_type} Evidence Analysis',
            'penalty': 15
        }

    # Stage 3: Between 2 clues and total_clues - 1: check suspect alibis and witness statements
    if collected_count < total_clues_count:
        # Cross reference witness statements
        contradictory_witness = case.witness_statements.filter(credibility='High').first()
        witness_name = contradictory_witness.witness_name if contradictory_witness else "the key eyewitness"
        return {
            'level': 'Advanced Alibi Cross-Examination',
            'hint': f"Carefully cross-examine witness testimonies against the suspects' claimed whereabouts. In particular, notice what {witness_name} observed around the time of the incident—one suspect's alibi is physically impossible.",
            'focus_area': 'Alibi Discrepancy & Timeline',
            'penalty': 15
        }

    # Stage 4: All clues collected - lead detective to connect the final dots
    culprit = case.correct_suspect
    culprit_hint = "Look closely at the motive and access privileges. Who had both the technical ability, the personal motive, and an alibi that broke down under scrutiny?"
    if culprit:
        # Hint at culprit's profile or profession without naming them
        culprit_hint = f"All clues are in your hands, Detective! Cross-reference the forensic evidence with the profile details of the suspects. Notice which suspect's personal items or technical expertise matches the recovered crime artifacts."

    return {
        'level': 'Final Deduction Synthesis',
        'hint': culprit_hint,
        'focus_area': 'Culprit Motive & Means Synthesis',
        'penalty': 15
    }
