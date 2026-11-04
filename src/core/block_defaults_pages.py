"""Дефолти блоків: внутрішні сторінки."""

from __future__ import annotations

from src.core.seo_copy import SEO

from .block_defaults import _reg, STATIC_FALLBACKS


def register_page_blocks() -> None:
    # --- About ---
    _reg("about", "hero_section_visible", "1", label="Показувати Hero")
    _reg("about", "seo_title", SEO["about"]["title"], label="SEO Title", inline=True)
    _reg("about", "seo_description", SEO["about"]["description"], label="SEO Description", multiline=True)
    _reg("about", "h1", "Про компанію", label="H1", inline=True)
    _reg("about", "hero_title", "Про компанію", label="Hero заголовок", inline=True)
    _reg(
        "about",
        "hero_text",
        "Ми допомагаємо бізнесу ухвалювати рішення на основі перевірених фактів",
        label="Hero текст",
        richtext=True,
    )
    _reg("about", "hero_image", "", label="Hero зображення", content_type="image")
    STATIC_FALLBACKS[("about", "hero_image")] = "images/about-bg.webp"

    _reg("about", "intro_section_visible", "1", label="Показувати «Про нас»")
    _reg("about", "intro_title", "Аналітика та безпека для вашого бізнесу", label="Заголовок «Про нас»", inline=True)
    _reg(
        "about",
        "intro_text",
        (
            "Ми допомагаємо бізнесу ухвалювати рішення на основі перевірених фактів. "
            "Досліджуємо компанії та людей, бізнес-групи й корпоративні структури."
        ),
        label="Текст «Про нас»",
        richtext=True,
    )

    _reg("about", "principles_section_visible", "1", label="Показувати принципи")
    _reg("about", "principles_title", "Наші принципи", label="Заголовок принципів", inline=True)

    _reg("about", "team_section_visible", "1", label="Показувати команду")
    _reg("about", "team_title", "Засновники", label="Заголовок команди", inline=True)
    _reg(
        "about",
        "team_lead",
        "Поєднуємо практичний досвід роботи в правоохоронних органах із науковим підходом до аналізу інформації",
        label="Лід команди",
        richtext=True,
    )

    _reg("about", "science_section_visible", "1", label="Показувати методологію")
    _reg("about", "science_eyebrow", "Наукова основа", label="Eyebrow науки", inline=True)
    _reg("about", "science_title", "Власний сервіс VI Analysis", label="Заголовок методології", inline=True)
    _reg(
        "about",
        "science_text",
        "Методологічна основа сервісу швидкої перевірки контрагентів викладена у статті засновників компанії.",
        label="Текст методології",
        richtext=True,
    )
    _reg("about", "science_doi_url", "https://doi.org/10.32842/2078-3736/2026.1.1.28", label="DOI посилання", content_type="url")
    _reg("about", "science_doi_label", "doi.org/10.32842/2078-3736/2026.1.1.28", label="DOI підпис", inline=True)

    _reg("about", "partners_section_visible", "1", label="Показувати партнерів")
    _reg("about", "partners_eyebrow", "Міжнародна діяльність", label="Eyebrow партнерів", inline=True)
    _reg("about", "partners_title", "Для бізнесу з інтересами за межами України", label="Заголовок партнерів", inline=True)
    _reg(
        "about",
        "partners_text",
        "Партнерами Vartis Intelligence є провідні профільні компанії в державах ЄС.",
        label="Текст партнерів",
        richtext=True,
    )

    _reg("about", "stats_section_visible", "1", label="Показувати цифри")
    _reg("about", "stats_title", "Ключові цифри", label="Заголовок цифр", inline=True)

    _reg("about", "process_section_visible", "1", label="Показувати процес")
    _reg("about", "process_title", "Як ми працюємо", label="Заголовок процесу", inline=True)

    # --- Services index ---
    _reg("services", "hero_section_visible", "1", label="Показувати Hero")
    _reg("services", "seo_title", SEO["services"]["title"], label="SEO Title", inline=True)
    _reg(
        "services",
        "seo_description",
        SEO["services"]["description"],
        label="SEO Description",
        multiline=True,
    )
    _reg("services", "h1", "Послуги", label="H1", inline=True)
    _reg("services", "hero_title", "Послуги", label="Hero заголовок", inline=True)
    _reg(
        "services",
        "hero_text",
        (
            "Комплексні рішення для бізнесу — від перевірки інформації "
            "до стратегічного аналізу та управління ризиками"
        ),
        label="Hero текст",
        richtext=True,
    )
    _reg("services", "hero_image", "", label="Hero зображення", content_type="image")

    # --- Analysis ---
    _reg("analysis", "hero_section_visible", "1", label="Показувати Hero")
    _reg("analysis", "seo_title", SEO["analysis"]["title"], label="SEO Title", inline=True)
    _reg("analysis", "seo_description", SEO["analysis"]["description"], label="SEO Description", multiline=True)
    _reg("analysis", "h1", "VI Analysis", label="H1", inline=True)
    _reg("analysis", "title", "VI Analysis", label="Назва в меню", inline=True)
    _reg("analysis", "hero_title", "VI Analysis", label="Hero заголовок", inline=True)
    _reg("analysis", "hero_text", "Власний сервіс швидкої перевірки контрагентів", label="Hero текст", richtext=True)
    _reg("analysis", "hero_image", "", label="Hero зображення", content_type="image")
    _reg("analysis", "short", "", label="Короткий опис у меню", inline=True)

    _reg("analysis", "steps_section_visible", "1", label="Показувати кроки")
    _reg("analysis", "steps_title", "Три кроки від реквізитів до рішення", label="Заголовок кроків", inline=True)

    _reg("analysis", "risks_section_visible", "1", label="Показувати ризики")
    _reg("analysis", "risks_title", "Що перевіряє VI ANALYSIS", label="Заголовок ризиків", inline=True)

    _reg("analysis", "recommendation_section_visible", "1", label="Показувати рекомендацію")
    _reg("analysis", "recommendation_title", "Рекомендація щодо співпраці", label="Заголовок рекомендації", inline=True)
    _reg("analysis", "recommendation_text", "", label="Текст рекомендації", richtext=True)

    _reg("analysis", "result_section_visible", "1", label="Показувати результат")
    _reg("analysis", "result_title", "Що отримує замовник", label="Заголовок результату", inline=True)
    _reg("analysis", "result_text", "", label="Текст результату", richtext=True)

    _reg("analysis", "paket_section_visible", "1", label="Показувати пакет")
    _reg("analysis", "paket_title", "Пакетне обслуговування", label="Заголовок пакета", inline=True)
    _reg("analysis", "paket_subtitle", "для постійних клієнтів", label="Підзаголовок пакета", inline=True)
    _reg("analysis", "paket_text", "", label="Текст пакета", richtext=True)

    _reg("analysis", "include_section_visible", "1", label="Показувати «Що входить»")
    _reg("analysis", "include_title", "Що входить до пакета", label="Заголовок «Що входить»", inline=True)

    _reg("analysis", "why_section_visible", "1", label="Показувати «Чому вигідно»")
    _reg("analysis", "why_title", "Чому це вигідно", label="Заголовок «Чому вигідно»", inline=True)

    _reg("analysis", "price_section_visible", "1", label="Показувати вартість")
    _reg("analysis", "price_title", "Скільки це коштує", label="Заголовок вартості", inline=True)

    _reg("analysis", "order_section_visible", "1", label="Показувати форму")
    _reg("analysis", "order_title", "Перевірте контрагента до підписання договору", label="Заголовок форми", inline=True)
    _reg("analysis", "order_text", "", label="Текст форми", richtext=True)

    # --- Contacts ---
    _reg("contacts", "hero_section_visible", "1", label="Показувати Hero")
    _reg("contacts", "seo_title", SEO["contacts"]["title"], label="SEO Title", inline=True)
    _reg("contacts", "seo_description", SEO["contacts"]["description"], label="SEO Description", multiline=True)
    _reg("contacts", "h1", "Контакти", label="H1", inline=True)
    _reg("contacts", "hero_title", "Контакти", label="Hero заголовок", inline=True)
    _reg("contacts", "hero_text", "", label="Hero текст", richtext=True)
    _reg("contacts", "hero_image", "", label="Hero зображення", content_type="image")
    _reg("contacts", "info_title", "Контактні дані", label="Заголовок блоку", inline=True)

    # --- Privacy ---
    _reg("privacy", "hero_section_visible", "1", label="Показувати Hero")
    _reg("privacy", "seo_title", SEO["privacy"]["title"], label="SEO Title", inline=True)
    _reg("privacy", "seo_description", SEO["privacy"]["description"], label="SEO Description", multiline=True)
    _reg("privacy", "h1", "Політика конфіденційності", label="H1", inline=True)
    _reg("privacy", "hero_title", "Політика конфіденційності", label="Hero заголовок", inline=True)
    _reg("privacy", "body", "", label="Текст політики", richtext=True)
