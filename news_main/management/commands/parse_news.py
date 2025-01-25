from django.core.management.base import BaseCommand
from news_main.parsers import run_all_parsers

class Command(BaseCommand):
    help = 'Parsing news from all sources...'

    def handle(self, *args, **kwargs):
        run_all_parsers()
        self.stdout.write(self.style.SUCCESS('Successfully parsed data!'))
        