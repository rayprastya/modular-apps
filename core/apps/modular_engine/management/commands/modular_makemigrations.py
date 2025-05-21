from django.core.management.base import BaseCommand
from django.core.management import call_command
from core.utils.metadata_updater import update_module_version

class Command(BaseCommand):
    help = "Run makemigrations and auto-increment metadata version"

    def add_arguments(self, parser):
        parser.add_argument("app_label", type=str, help="App label to makemigrations and upgrade metadata")

    def handle(self, *args, **options):
        app_label = options["app_label"]

        # run makemigrations
        self.stdout.write(self.style.SUCCESS(f"Running makemigrations for {app_label}..."))
        call_command("makemigrations", app_label)

        # update metadata.json
        try:
            update_module_version(app_label)
            self.stdout.write(self.style.SUCCESS("metadata.json updated!"))
        except Exception as e:
            self.stderr.write(f"Failed to update metadata.json: {e}")
