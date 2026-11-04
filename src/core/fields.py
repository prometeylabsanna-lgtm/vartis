"""Кастомні поля моделей."""

from __future__ import annotations

from django.db.models import ImageField

from src.core.image_webp import convert_upload_to_webp


class WebPImageField(ImageField):
    """
    ImageField з автоконвертацією нового upload → WebP.
    SVG / анімований GIF / уже WebP — без змін.
    """

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        if file and not getattr(file, '_committed', True):
            converted = convert_upload_to_webp(file)
            if converted is not None:
                setattr(model_instance, self.attname, converted)
        return super().pre_save(model_instance, add)

    def deconstruct(self):
        # Уникаємо зайвих AlterField-міграцій: у БД це той самий ImageField.
        name, _path, args, kwargs = super().deconstruct()
        return name, 'django.db.models.ImageField', args, kwargs
