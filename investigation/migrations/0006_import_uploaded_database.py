import base64
import json
import zlib

from django.db import migrations


# Snapshot of the supplied SQLite database. The source user "aryan" (ID 8)
# and every user-owned row belonging to that account were excluded.
PAYLOAD = """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"""


def import_legacy_database(apps, schema_editor):
    db = schema_editor.connection.alias
    data = json.loads(zlib.decompress(base64.b64decode(PAYLOAD)).decode("utf-8"))

    User = apps.get_model("auth", "User")
    Profile = apps.get_model("accounts", "UserProfile")
    Case = apps.get_model("investigation", "Case")
    Suspect = apps.get_model("investigation", "Suspect")
    Clue = apps.get_model("investigation", "Clue")
    Evidence = apps.get_model("investigation", "Evidence")
    Witness = apps.get_model("investigation", "WitnessStatement")
    Progress = apps.get_model("investigation", "UserCaseProgress")
    Accusation = apps.get_model("investigation", "Accusation")

    users = {}
    for row in data["auth_user"]:
        user, _ = User.objects.using(db).get_or_create(
            username=row["username"],
            defaults={
                "password": row["password"],
                "last_login": row["last_login"],
                "is_superuser": bool(row["is_superuser"]),
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "is_staff": bool(row["is_staff"]),
                "is_active": bool(row["is_active"]),
                "date_joined": row["date_joined"],
            },
        )
        users[row["id"]] = user

    for row in data["accounts_userprofile"]:
        user = users.get(row["user_id"])
        if user:
            Profile.objects.using(db).get_or_create(
                user_id=user.pk,
                defaults={
                    "total_score": row["total_score"],
                    "rank": row["rank"],
                    "cases_solved": row["cases_solved"],
                    "bio": row["bio"],
                    "badge_level": row["badge_level"],
                },
            )

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
            },
        )
        cases[row["id"]] = case
        Case.objects.using(db).filter(pk=case.pk).update(created_at=row["created_at"])

    suspects = {}
    case_suspects = {}
    for link in data["investigation_suspect_cases"]:
        source = next((s for s in data["investigation_suspect"] if s["id"] == link["suspect_id"]), None)
        case = cases.get(link["case_id"])
        if not source or not case:
            continue
        suspect = case.suspects.using(db).filter(
            name=source["name"], profile=source["profile"],
            motive=source["motive"], alibi=source["alibi"]
        ).first()
        if suspect is None:
            suspect = Suspect.objects.using(db).create(
                name=source["name"], profile=source["profile"],
                motive=source["motive"], alibi=source["alibi"],
                image=source["image"] or "", is_culprit=bool(source["is_culprit"])
            )
            suspect.cases.add(case)
        suspects[source["id"]] = suspect
        case_suspects[(link["case_id"], source["id"])] = suspect

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
            case_id=case.pk, title=row["title"],
            defaults={
                "description": row["description"],
                "clue_type": row["clue_type"],
                "image": row["image"] or "",
            },
        )
        Clue.objects.using(db).filter(pk=clue.pk).update(created_at=row["created_at"])
        clues[row["id"]] = clue

    for row in data["investigation_evidence"]:
        case = cases.get(row["case_id"])
        if not case:
            continue
        Evidence.objects.using(db).get_or_create(
            case_id=case.pk, description=row["description"],
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
                case_id=case.pk, witness_name=row["witness_name"],
                defaults={
                    "statement": row["statement"],
                    "credibility": row["credibility"],
                    "created_at": row["created_at"],
                },
            )

    progresses = {}
    for row in data["investigation_usercaseprogress"]:
        user, case = users.get(row["user_id"]), cases.get(row["case_id"])
        if not user or not case:
            continue
        progress, _ = Progress.objects.using(db).get_or_create(
            user_id=user.pk, case_id=case.pk,
            defaults={
                "completion_status": row["completion_status"],
                "score": row["score"],
                "hints_used": row["hints_used"],
                "investigation_notes": row["investigation_notes"],
                "completed_at": row["completed_at"],
            },
        )
        Progress.objects.using(db).filter(pk=progress.pk).update(
            started_at=row["started_at"], completed_at=row["completed_at"]
        )
        progresses[row["id"]] = progress

    for row in data["investigation_usercaseprogress_collected_clues"]:
        progress, clue = progresses.get(row["usercaseprogress_id"]), clues.get(row["clue_id"])
        if progress and clue:
            progress.collected_clues.add(clue)

    for row in data["investigation_accusation"]:
        user, case = users.get(row["user_id"]), cases.get(row["case_id"])
        suspect = suspects.get(row["selected_suspect_id"])
        if user and case and suspect:
            accusation, created = Accusation.objects.using(db).get_or_create(
                user_id=user.pk, case_id=case.pk,
                selected_suspect_id=suspect.pk,
                submission_date=row["submission_date"],
                defaults={
                    "correctness": bool(row["correctness"]),
                    "deduction_notes": row["deduction_notes"],
                },
            )
            if created:
                Accusation.objects.using(db).filter(pk=accusation.pk).update(
                    submission_date=row["submission_date"]
                )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_userprofile_security_recovery"),
        ("investigation", "0005_normalize_seeded_evidence"),
    ]
    operations = [
        migrations.RunPython(import_legacy_database, migrations.RunPython.noop),
    ]
