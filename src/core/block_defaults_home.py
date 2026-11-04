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
