from django.core.management.base import BaseCommand
from news_main.parsers import parse_habr_news

class Command(BaseCommand):
    help = 'Parsing Habr data...'

    def handle(self, *args, **kwargs):
        parse_habr_news()
        self.stdout.write(self.style.SUCCESS('Successfully parsed data!'))
        