from pathlib import Path
import tempfile

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command
from django.db import connections


class Command(BaseCommand):
    help = (
        "Copy records from the local db.sqlite3 into the configured Turso database. "
        "The Turso application tables must be empty."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            default=str(settings.BASE_DIR / "db.sqlite3"),
            help="Path to the SQLite database to import (default: BASE_DIR/db.sqlite3).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate the source and show record counts without importing data.",
        )

    def handle(self, *args, **options):
        source = Path(options["source"]).expanduser().resolve()
        if not source.is_file():
            raise CommandError(
                f"SQLite source not found: {source}. Copy your original db.sqlite3 "
                "to the project root or pass --source with its path."
            )

        target = settings.DATABASES["default"]
        if target.get("ENGINE") != "django_libsql":
            raise CommandError(
                "The default database is not configured for Turso. Set "
                "TURSO_DB_URL and TURSO_AUTH_TOKEN before running this command."
            )

        if not settings.TURSO_DB_URL or not settings.TURSO_AUTH_TOKEN:
            raise CommandError("Both Turso environment variables are required.")

        # Register the old SQLite file as a temporary, read-only source connection.
        connections.databases["legacy_sqlite"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(source),
            "OPTIONS": {"timeout": 30},
        }

        try:
            with connections["legacy_sqlite"].cursor() as cursor:
                cursor.execute("PRAGMA quick_check")
                integrity = cursor.fetchone()[0]
                if integrity != "ok":
                    raise CommandError(f"SQLite integrity check failed: {integrity}")

            self.stdout.write("Checking and applying Turso schema migrations...")
            call_command("migrate", database="default", interactive=False, verbosity=0)

            # Never silently overwrite or mix records with an already-used database.
            protected_models = [
                model
                for model in apps.get_models()
                if model._meta.app_label in {"accounts", "investigation"}
                or (
                    model._meta.app_label == "auth"
                    and model._meta.model_name == "user"
                )
            ]
            occupied = []
            for model in protected_models:
                count = model.objects.using("default").count()
                if count:
                    occupied.append(f"{model._meta.label}={count}")
            if occupied:
                raise CommandError(
                    "Import stopped because the Turso database already contains "
                    "application data: "
                    + ", ".join(occupied)
                    + ". Back up both databases and reconcile records before importing; "
                    "this command deliberately will not overwrite existing data."
                )

            models_to_copy = [
                model
                for model in apps.get_models()
                if model._meta.app_label in {"accounts", "investigation", "auth"}
                and not (
                    model._meta.app_label == "auth"
                    and model._meta.model_name == "permission"
                )
            ]
            source_counts = {}
            for model in models_to_copy:
                try:
                    count = model.objects.using("legacy_sqlite").count()
                except Exception as exc:
                    raise CommandError(
                        f"Could not read {model._meta.label} from the SQLite source. "
                        "Make sure this database was created by a compatible version "
                        f"of Mystery Quest. Details: {exc}"
                    ) from exc
                if count:
                    source_counts[model._meta.label] = count

            self.stdout.write("SQLite records found:")
            if source_counts:
                for label, count in source_counts.items():
                    self.stdout.write(f"  {label}: {count}")
            else:
                self.stdout.write("  No application records found.")

            if options["dry_run"]:
                self.stdout.write(self.style.SUCCESS(
                    "Dry run complete. No application records were imported."
                ))
                return

            excluded = [
                "sessions",
                "admin.logentry",
            ]
            with tempfile.TemporaryDirectory(prefix="mystery-quest-import-") as temp_dir:
                fixture = Path(temp_dir) / "legacy-data.json"
                self.stdout.write("Exporting SQLite data to a temporary fixture...")
                call_command(
                    "dumpdata",
                    database="legacy_sqlite",
                    output=str(fixture),
                    format="json",
                    indent=2,
                    natural_foreign=True,
                    natural_primary=True,
                    exclude=excluded,
                    verbosity=0,
                )

                if not fixture.exists() or fixture.stat().st_size == 0:
                    raise CommandError("Django produced an empty export fixture.")

                self.stdout.write("Importing records into Turso...")
                call_command(
                    "loaddata",
                    str(fixture),
                    database="default",
                    verbosity=1,
                )

            mismatches = []
            for model in models_to_copy:
                expected = source_counts.get(model._meta.label, 0)
                actual = model.objects.using("default").count()
                if expected != actual:
                    mismatches.append(
                        f"{model._meta.label}: SQLite={expected}, Turso={actual}"
                    )

            if mismatches:
                raise CommandError(
                    "Import ran, but record-count verification found differences:\n"
                    + "\n".join(mismatches)
                    + "\nDo not rerun blindly; inspect the Turso data first."
                )

            self.stdout.write(self.style.SUCCESS(
                "Import completed and record counts match. Your SQLite records are "
                "now in Turso. Keep the original db.sqlite3 as a backup."
            ))
        finally:
            connections["legacy_sqlite"].close()
            connections.databases.pop("legacy_sqlite", None)
