"""Дефолти блоків: головна та оболонка сайту."""

from __future__ import annotations

from src.pages import design_copy

from .block_defaults import _reg, STATIC_FALLBACKS

HOME = design_copy.HOME


def register_home_blocks() -> None:
    _reg("home", "hero_section_visible", "1", label="Показувати Hero")
    _reg("home", "seo_title", "VARTIS INTELLIGENCE — стратегічна аналітика та перевірка контрагентів", label="SEO Title", inline=True)
    _reg(
        "home",
        "seo_description",
        (
            "Стратегічна аналітика, перевірка контрагентів та захист бізнесу. "
            "Допомагаємо виявляти приховані ризики й ухвалювати обґрунтовані рішення."
        ),
        label="SEO Description",
        multiline=True,
    )
    _reg("home", "h1", HOME["h1"], label="H1", inline=True)
    _reg("home", "hero_title", HOME["h1"].replace("\n", " "), label="Hero заголовок", inline=True)
    _reg("home", "hero_text", HOME["hero_text"], label="Hero текст", richtext=True)
    _reg("home", "hero_image", "", label="Hero зображення", content_type="image")
    STATIC_FALLBACKS[("home", "hero_image")] = "images/hero.png"
    _reg("home", "hero_cta", HOME["hero_cta"], label="Текст CTA", inline=True)

    _reg("home", "services_section_visible", "1", label="Показувати напрями")
    _reg("home", "services_title", HOME["services_title"], label="Заголовок напрямів", inline=True)
    _reg("home", "services_lead", HOME["services_lead"], label="Підзаголовок напрямів", multiline=True)

    _reg("home", "advantages_section_visible", "1", label="Показувати переваги")
    _reg("home", "advantages_title", HOME["advantages_title"], label="Заголовок переваг", inline=True)
    _reg("home", "advantages_lead", HOME["advantages_lead"], label="Підзаголовок переваг", inline=True)

    _reg("home", "mission_section_visible", "1", label="Показувати місію")
    _reg("home", "mission_title", HOME["mission_title"], label="Заголовок місії", inline=True)
    _reg("home", "mission_text", HOME["mission_text"], label="Текст місії", richtext=True)
    _reg("home", "mission_image", "", label="Фон місії", content_type="image")
    STATIC_FALLBACKS[("home", "mission_image")] = "images/about-bg.png"

    _reg("home", "process_section_visible", "1", label="Показувати процес")
    _reg("home", "process_title", HOME["process_title"], label="Заголовок процесу", inline=True)
    _reg("home", "process_lead", HOME["process_lead"], label="Підзаголовок процесу", inline=True)

    _reg("home", "blog_section_visible", "1", label="Показувати блог")
    _reg("home", "blog_title", HOME["blog_title"], label="Заголовок блогу", inline=True)
    _reg("home", "blog_lead", HOME["blog_lead"], label="Підзаголовок блогу", multiline=True)

    _reg(
        "site",
        "footer_cta_title",
        "Залишити заявку",
        label="Заголовок CTA у футері",
        inline=True,
    )
    _reg(
        "site",
        "footer_cta_text",
        (
            "Опишіть ситуацію — ми зв'яжемося, щоб уточнити завдання. "
            "Факт звернення залишається конфіденційним."
        ),
        label="Текст CTA у футері",
        richtext=True,
    )

    _reg("site", "header_cta_label", "Обговорити завдання", label="Текст CTA у хедері", inline=True)
    _reg("site", "header_services_label", "Послуги", label="Підпис меню «Послуги»", inline=True)

    _reg("site", "footer_nav_company_title", "Компанія", label="Заголовок колонки «Компанія»", inline=True)
    _reg("site", "footer_nav_services_title", "Послуги", label="Заголовок колонки «Послуги»", inline=True)

    _reg("site", "footer_contact_phone_label", "Тел", label="Підпис телефону у футері", inline=True)
    _reg("site", "footer_contact_email_label", "Email", label="Підпис email у футері", inline=True)
    _reg("site", "footer_contact_address_label", "Адр", label="Підпис адреси у футері", inline=True)
    _reg("site", "footer_contact_phone_placeholder", "[Телефон]", label="Плейсхолдер телефону", inline=True)
    _reg("site", "footer_contact_email_placeholder", "[Email]", label="Плейсхолдер email", inline=True)
    _reg(
        "site",
        "footer_contact_address_placeholder",
        "[Адреса офісу]",
        label="Плейсхолдер адреси",
        inline=True,
    )

    _reg("site", "form_name_label", "Ім'я", label="Підпис поля «Ім'я»", inline=True)
    _reg("site", "form_phone_label", "Телефон", label="Підпис поля «Телефон»", inline=True)
    _reg("site", "form_email_label", "Email", label="Підпис поля «Email»", inline=True)
    _reg(
        "site",
        "form_message_label",
        "Коротко про завдання",
        label="Підпис поля «Повідомлення»",
        inline=True,
    )
    _reg(
        "site",
        "form_phone_placeholder",
        "+380 XX XXX XX XX",
        label="Плейсхолдер телефону у формі",
        inline=True,
    )
    _reg(
        "site",
        "form_email_placeholder",
        "user@domain.com",
        label="Плейсхолдер email у формі",
        inline=True,
    )
    _reg("site", "form_message_placeholder", "", label="Плейсхолдер повідомлення", multiline=True)
    _reg(
        "site",
        "form_consent_text",
        (
            'Погоджуюся на обробку персональних даних відповідно до '
            '<a href="/polityka-konfidentsiynosti/">Політики конфіденційності</a>'
        ),
        label="Текст згоди у формі",
        richtext=True,
    )
    _reg("site", "form_submit_label", "Надіслати заявку", label="Текст кнопки відправки", inline=True)
