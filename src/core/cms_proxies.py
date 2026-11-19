"""Proxy-секції адмінки: та сама таблиця, що й публічна модель сторінки."""

from src.core.models import SiteSettings
from src.core.models_cms import PageStyle
from src.pages.models import (
    AboutPage,
    AnalysisPage,
    ContactsPage,
    HomePage,
    PrivacyPage,
    ServicesIndex,
)


def _meta(verbose: str):
    return type(
        "Meta",
        (),
        {
            "proxy": True,
            "verbose_name": verbose,
            "verbose_name_plural": verbose,
        },
    )


def _proxy(name: str, base, verbose: str):
    cls = type(name, (base,), {"Meta": _meta(verbose), "__module__": __name__})
    return cls


HomeHeroSettings = _proxy("HomeHeroSettings", HomePage, "Головна — Перший екран")
HomeStyleSettings = _proxy("HomeStyleSettings", PageStyle, "Головна — Оформлення")
HomeServicesSettings = _proxy("HomeServicesSettings", HomePage, "Головна — Напрями")
HomeAdvantagesSettings = _proxy("HomeAdvantagesSettings", HomePage, "Головна — Переваги")
HomeMissionSettings = _proxy("HomeMissionSettings", HomePage, "Головна — Місія")
HomeProcessSettings = _proxy("HomeProcessSettings", HomePage, "Головна — Процес")
HomeBlogSettings = _proxy("HomeBlogSettings", HomePage, "Головна — Блог")

SiteHeaderSettings = _proxy("SiteHeaderSettings", SiteSettings, "Шапка сайту")
SiteFooterSettings = _proxy("SiteFooterSettings", SiteSettings, "Підвал сайту")

AboutHeroSettings = _proxy("AboutHeroSettings", AboutPage, "Про компанію — Перший екран")
AboutStyleSettings = _proxy("AboutStyleSettings", PageStyle, "Про компанію — Оформлення")
AboutIntroSettings = _proxy("AboutIntroSettings", AboutPage, "Про компанію — Вступ")
AboutPrinciplesSettings = _proxy("AboutPrinciplesSettings", AboutPage, "Про компанію — Принципи")
AboutTeamSettings = _proxy("AboutTeamSettings", AboutPage, "Про компанію — Команда")
AboutScienceSettings = _proxy("AboutScienceSettings", AboutPage, "Про компанію — Наука")
AboutPartnersSettings = _proxy("AboutPartnersSettings", AboutPage, "Про компанію — Партнери")
AboutStatsSettings = _proxy("AboutStatsSettings", AboutPage, "Про компанію — Цифри")
AboutProcessSettings = _proxy("AboutProcessSettings", AboutPage, "Про компанію — Процес")

ServicesHeroSettings = _proxy("ServicesHeroSettings", ServicesIndex, "Послуги — Перший екран")
ServicesStyleSettings = _proxy("ServicesStyleSettings", PageStyle, "Послуги — Оформлення")

AnalysisHeroSettings = _proxy("AnalysisHeroSettings", AnalysisPage, "VI Analysis — Перший екран")
AnalysisStyleSettings = _proxy("AnalysisStyleSettings", PageStyle, "VI Analysis — Оформлення")
AnalysisStepsSettings = _proxy("AnalysisStepsSettings", AnalysisPage, "VI Analysis — Кроки")
AnalysisRisksSettings = _proxy("AnalysisRisksSettings", AnalysisPage, "VI Analysis — Ризики")
AnalysisRecommendationSettings = _proxy(
    "AnalysisRecommendationSettings", AnalysisPage, "VI Analysis — Рекомендація",
)
AnalysisResultSettings = _proxy("AnalysisResultSettings", AnalysisPage, "VI Analysis — Результат")
AnalysisPaketSettings = _proxy("AnalysisPaketSettings", AnalysisPage, "VI Analysis — Пакет")
AnalysisIncludeSettings = _proxy("AnalysisIncludeSettings", AnalysisPage, "VI Analysis — Що входить")
AnalysisWhySettings = _proxy("AnalysisWhySettings", AnalysisPage, "VI Analysis — Чому вигідно")
AnalysisPriceSettings = _proxy("AnalysisPriceSettings", AnalysisPage, "VI Analysis — Вартість")
AnalysisOrderSettings = _proxy("AnalysisOrderSettings", AnalysisPage, "VI Analysis — Заявка")

ContactsHeroSettings = _proxy("ContactsHeroSettings", ContactsPage, "Контакти — Перший екран")
ContactsStyleSettings = _proxy("ContactsStyleSettings", PageStyle, "Контакти — Оформлення")

PrivacyHeroSettings = _proxy("PrivacyHeroSettings", PrivacyPage, "Політика — Перший екран")
PrivacyStyleSettings = _proxy("PrivacyStyleSettings", PageStyle, "Політика — Оформлення")

STYLE_PAGE = {
    "HomeStyleSettings": "home",
    "AboutStyleSettings": "about",
    "ServicesStyleSettings": "services",
    "AnalysisStyleSettings": "analysis",
    "ContactsStyleSettings": "contacts",
    "PrivacyStyleSettings": "privacy",
}
