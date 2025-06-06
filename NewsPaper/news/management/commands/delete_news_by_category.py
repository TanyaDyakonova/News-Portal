from django.core.management.base import BaseCommand
from NewsPaper.news.models import Category, Post

class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории (с подтверждением)'

    def add_arguments(self, parser):
        parser.add_argument('category',   type=int)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалены все новости из категории {category.name}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не найдена категория {options['category']}'))