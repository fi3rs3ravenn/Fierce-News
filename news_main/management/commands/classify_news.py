from django.core.management.base import BaseCommand
from news_main.models import News
import openai

openai.api_key = "my API key"

CATEGORIES = [
    "Искусственный интеллект",
    "Нейросети",
    "Роботы",
    "Программирование",
    "Разработка ПО",
    "Информационные технологии",
    "Космос",
    "Астрономия",
    "Смартфоны",
    "Гаджеты",
    "Ноутбуки",
    "Электромобили",
    "Автомобильные технологии",
    "Кибербезопасность",
    "Игровая индустрия",
    "Блокчейн и криптовалюты",
    "Социальные сети",
    "Образование",
    "Наука и технологии",
    "Здравоохранение и технологии",
]

CONFIDENCE_THRESHOLD = 0.7

def get_category_with_openai(text, categories):
    prompt = f"Определи категорию для следующего текста:\n\n'{text}'\n\nКатегории: {', '.join(categories)}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты помощник, который определяет категорию текста."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.3
    )
    category = response['choices'][0]['message']['content'].strip()
    return category

class Command(BaseCommand):
    help = 'Classify existing news in database using OpenAI API'

    def handle(self, *args, **kwargs):
        news_without_category = News.objects.filter(category='Не классифицировано')
        total = news_without_category.count()
        self.stdout.write(f"Found {total} news articles to classify.")

        if total == 0:
            self.stdout.write(self.style.WARNING("No news articles need classification."))
            return

        for news in news_without_category:
            text = f"Заголовок: {news.title}. Описание: {news.description}."
            try:
                category = get_category_with_openai(text, CATEGORIES)
                news.category = category
                news.save()
                self.stdout.write(f'Updated news "{news.title[:30]}" -> {category}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing '{news.title[:30]}': {e}"))

        self.stdout.write(self.style.SUCCESS("All articles have been classified successfully!"))
