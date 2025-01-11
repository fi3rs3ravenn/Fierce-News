from django.core.management.base import BaseCommand
from news_main.parsers import parse_habr_news, parse_tengrinews

class Command(BaseCommand):
    help = 'Parse news from specific sources'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            help='Specify the source: "habr" or "tengrinews"',
        )

    def handle(self, *args, **kwargs):
        source = kwargs.get('source')
        if source == 'habr':
            parse_habr_news()
            self.stdout.write(self.style.SUCCESS('Successfully parsed Habr news!'))
        elif source == 'tengrinews':
            parse_tengrinews()
            self.stdout.write(self.style.SUCCESS('Successfully parsed Tengrinews news!'))
        else:
            self.stdout.write(self.style.WARNING('Please specify a valid source: "habr" or "tengrinews".'))
