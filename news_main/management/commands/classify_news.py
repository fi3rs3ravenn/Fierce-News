from django.core.management.base import BaseCommand
from news_main.models import News
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

CATEGORIES = [
    'Искусственный интеллект и нейросети',
    'Роботы и технологии будущего',
    'Программирование и IT',
    'Новости космоса и астрономии',
    'Мобильные устройства и гаджеты',
    'Электрокары и автомобильные технологии'
]

def get_category(text):
    result = classifier(text, CATEGORIES, multi_class=False)
    category = result['labels'][0]
    scores = result['scores'][0]
    return category, scores

class Command(BaseCommand):
    help = 'Classify existing news in database'

    def handle(self, *args, **kwargs):
        news_without_category = News.objects.filter(category='Не классифицировано')
        total = news_without_category.count()

        self.stdout.write(f'Found {total} news to classify')

        if total == 0:
            self.stdout.write(self.style.WARNING('No news articles need classification.'))
            return

        for news in news_without_category:
            text = f'{news.title} {news.description}'
            category, confidence = get_category(text)
            news.category = category
            news.save()
            self.stdout.write(f'Updated news {news.title[:10]} with ctgry: {category} confidence: {confidence:.2f}')
        self.stdout.write(self.style.SUCCESS('ALL ARTICLES HAVE BEEN CLASSIFIED'))