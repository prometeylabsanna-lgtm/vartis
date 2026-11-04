"""Proxy-моделі CMS-секцій (слоти sidebar)."""

from src.core.models import SiteSettings


class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Hero"
        verbose_name_plural = "Головна — Hero"


class HomeStyleSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Оформлення"
        verbose_name_plural = "Головна — Оформлення"


class HomeServicesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Напрями"
        verbose_name_plural = "Головна — Напрями"


class HomeAdvantagesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Переваги"
        verbose_name_plural = "Головна — Переваги"


class HomeMissionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Місія"
        verbose_name_plural = "Головна — Місія"


class HomeProcessSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Процес"
        verbose_name_plural = "Головна — Процес"


class HomeBlogSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Блог"
        verbose_name_plural = "Головна — Блог"


class SiteHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Оболонка — Хедер"
        verbose_name_plural = "Оболонка — Хедер"


class SiteFooterSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Оболонка — Футер"
        verbose_name_plural = "Оболонка — Футер"


class AboutHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Hero"
        verbose_name_plural = "Про компанію — Hero"


class AboutStyleSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Оформлення"
        verbose_name_plural = "Про компанію — Оформлення"


class AboutIntroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Про нас"
        verbose_name_plural = "Про компанію — Про нас"


class AboutPrinciplesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Принципи"
        verbose_name_plural = "Про компанію — Принципи"


class AboutTeamSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Команда"
        verbose_name_plural = "Про компанію — Команда"


class AboutScienceSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Методологія"
        verbose_name_plural = "Про компанію — Методологія"


class AboutPartnersSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Партнери"
        verbose_name_plural = "Про компанію — Партнери"


class AboutStatsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Цифри"
        verbose_name_plural = "Про компанію — Цифри"


class AboutProcessSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про компанію — Процес"
        verbose_name_plural = "Про компанію — Процес"


class ServicesHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Послуги — Hero"
        verbose_name_plural = "Послуги — Hero"


class ServicesStyleSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Послуги — Оформлення"
        verbose_name_plural = "Послуги — Оформлення"


class AnalysisHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Hero"
        verbose_name_plural = "VI Analysis — Hero"


class AnalysisStyleSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Оформлення"
        verbose_name_plural = "VI Analysis — Оформлення"


class AnalysisStepsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Кроки"
        verbose_name_plural = "VI Analysis — Кроки"


class AnalysisRisksSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Ризики"
        verbose_name_plural = "VI Analysis — Ризики"


class AnalysisRecommendationSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Рекомендація"
        verbose_name_plural = "VI Analysis — Рекомендація"


class AnalysisResultSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Результат"
        verbose_name_plural = "VI Analysis — Результат"


class AnalysisPaketSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Пакет"
        verbose_name_plural = "VI Analysis — Пакет"


class AnalysisIncludeSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Що входить"
        verbose_name_plural = "VI Analysis — Що входить"


class AnalysisWhySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Чому вигідно"
        verbose_name_plural = "VI Analysis — Чому вигідно"


class AnalysisPriceSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Вартість"
        verbose_name_plural = "VI Analysis — Вартість"


class AnalysisOrderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "VI Analysis — Форма"
        verbose_name_plural = "VI Analysis — Форма"


class ContactsHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Контакти — Hero"
        verbose_name_plural = "Контакти — Hero"


class ContactsStyleSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Контакти — Оформлення"
        verbose_name_plural = "Контакти — Оформлення"


class PrivacyHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Політика — Hero"
        verbose_name_plural = "Політика — Hero"


class PrivacyStyleSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Політика — Оформлення"
        verbose_name_plural = "Політика — Оформлення"
