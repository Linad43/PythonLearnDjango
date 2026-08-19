from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        call_command(
            'dumpdata',
            'catalog.Category',
            output='category_fixture.json',
            indent=2
        )
        call_command(
            'dumpdata',
            'catalog.Product',
            output='category_fixture.json',
            indent=2
        )
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded data from fixture')
        )
