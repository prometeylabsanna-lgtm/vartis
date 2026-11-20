from django.core.management.base import BaseCommand

from src.core.i18n_seed import apply_english_copy


class Command(BaseCommand):
    help = 'Заливає англійські тексти публічного сайту, якщо поле ще порожнє або повторює українське.'

    def handle(self, *args, **options):
        apply_english_copy()
        self.stdout.write(self.style.SUCCESS('Англійські тексти оновлено.'))
