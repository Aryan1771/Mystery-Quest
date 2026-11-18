import base64
import json
import zlib

from django.db import migrations


# Game-content snapshot only. No accounts, password hashes, player progress,
# or account-linked accusations are imported.
PAYLOAD = """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"""


def import_game_content(apps, schema_editor):
    db = schema_editor.connection.alias
    data = json.loads(zlib.decompress(base64.b64decode(PAYLOAD)).decode("utf-8"))

    Case = apps.get_model("investigation", "Case")
    Suspect = apps.get_model("investigation", "Suspect")
    Clue = apps.get_model("investigation", "Clue")
    Evidence = apps.get_model("investigation", "Evidence")
    Witness = apps.get_model("investigation", "WitnessStatement")

    cases = {}
    for row in data["investigation_case"]:
        case, _ = Case.objects.using(db).get_or_create(
            title=row["title"],
            defaults={
                "description": row["description"],
                "background": row["background"],
                "difficulty": row["difficulty"],
                "image": row["image"] or "",
                "status": row["status"],
                "solution_explanation": row["solution_explanation"],
                "created_at": row["created_at"],
            },
        )
        cases[row["id"]] = case

    source_suspects = {row["id"]: row for row in data["investigation_suspect"]}
    suspects = {}
    for link in data["investigation_suspect_cases"]:
        source = source_suspects.get(link["suspect_id"])
        case = cases.get(link["case_id"])
        if not source or not case:
            continue
        suspect = case.suspects.using(db).filter(
            name=source["name"], profile=source["profile"],
            motive=source["motive"], alibi=source["alibi"],
        ).first()
        if suspect is None:
            suspect = Suspect.objects.using(db).create(
                name=source["name"],
                profile=source["profile"],
                motive=source["motive"],
                alibi=source["alibi"],
                image=source["image"] or "",
                is_culprit=bool(source["is_culprit"]),
            )
            suspect.cases.db_manager(db).add(case)
        suspects[source["id"]] = suspect

    for row in data["investigation_case"]:
        case = cases.get(row["id"])
        suspect = suspects.get(row["correct_suspect_id"])
        if case and suspect and not case.correct_suspect_id:
            Case.objects.using(db).filter(pk=case.pk).update(correct_suspect_id=suspect.pk)

    clues = {}
    for row in data["investigation_clue"]:
        case = cases.get(row["case_id"])
        if not case:
            continue
        clue, _ = Clue.objects.using(db).get_or_create(
            case_id=case.pk,
            title=row["title"],
            defaults={
                "description": row["description"],
                "clue_type": row["clue_type"],
                "image": row["image"] or "",
                "created_at": row["created_at"],
            },
        )
        clues[row["id"]] = clue

    for row in data["investigation_evidence"]:
        case = cases.get(row["case_id"])
        if not case:
            continue
        Evidence.objects.using(db).get_or_create(
            case_id=case.pk,
            description=row["description"],
            defaults={
                "evidence_type": row["evidence_type"],
                "created_at": row["created_at"],
                "clue_id": clues[row["clue_id"]].pk if row["clue_id"] in clues else None,
                "suspect_id": suspects[row["suspect_id"]].pk if row["suspect_id"] in suspects else None,
            },
        )

    for row in data["investigation_witnessstatement"]:
        case = cases.get(row["case_id"])
        if case:
            Witness.objects.using(db).get_or_create(
                case_id=case.pk,
                witness_name=row["witness_name"],
                defaults={
                    "statement": row["statement"],
                    "credibility": row["credibility"],
                    "created_at": row["created_at"],
                },
            )


class Migration(migrations.Migration):
    dependencies = [
        ("investigation", "0005_normalize_seeded_evidence"),
    ]
    operations = [
        migrations.RunPython(import_game_content, migrations.RunPython.noop),
    ]
