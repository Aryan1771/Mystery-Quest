from django.db import migrations


def normalize_seeded_evidence(apps, schema_editor):
    Evidence = apps.get_model("investigation", "Evidence")
    db = schema_editor.connection.alias
    # "Physical" is a valid Clue type, but not an Evidence type. The
    # 0004 seed migration accidentally used it for some evidence records.
    Evidence.objects.using(db).filter(evidence_type="Physical").update(
        evidence_type="Chemical Trace"
    )


class Migration(migrations.Migration):
    dependencies = [("investigation", "0004_seed_seventeen_more_cases")]
    operations = [
        migrations.RunPython(normalize_seeded_evidence, migrations.RunPython.noop),
    ]
