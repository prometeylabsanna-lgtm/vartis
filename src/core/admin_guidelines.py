"""Підказки CMS: ліміти тексту та профілі зображень."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageProfile:
    label: str
    width: int
    height: int
    max_kb: int

    @property
    def hint(self) -> str:
        return (
            f"Рекомендовано {self.width}×{self.height} px, "
            f"JPG/WebP/PNG, до {self.max_kb} КБ. "
            "Превʼю нижче — поточне фото на сайті."
        )


@dataclass(frozen=True)
class TextLimit:
    max_chars: int
    soft: bool = False  # soft = підказка без жорсткого maxlength

    @property
    def hint(self) -> str:
        if self.soft:
            return f"Рекомендовано до {self.max_chars} символів (щоб не зламати верстку)."
        return f"Максимум {self.max_chars} символів."


# Профілі зображень за ключем / суфіксом
IMAGE_PROFILES: dict[str, ImageProfile] = {
    "hero": ImageProfile("Hero", 1600, 900, 900),
    "mission": ImageProfile("Місія / фон", 1600, 900, 900),
    "card": ImageProfile("Картка", 640, 360, 400),
    "team": ImageProfile("Фото команди", 800, 1000, 500),
    "style": ImageProfile("Фон сторінки", 1920, 1080, 1200),
    "default": ImageProfile("Зображення", 1200, 800, 700),
}

# Ліміти тексту: точні ключі + патерни
TEXT_LIMITS: dict[str, TextLimit] = {
    "seo_title": TextLimit(70),
    "seo_description": TextLimit(160),
    "h1": TextLimit(90),
    "hero_title": TextLimit(90),
    "hero_cta": TextLimit(40),
    "hero_text": TextLimit(280, soft=True),
    "short": TextLimit(160),
    "services_title": TextLimit(80),
    "services_lead": TextLimit(180, soft=True),
    "advantages_title": TextLimit(80),
    "advantages_lead": TextLimit(120),
    "mission_title": TextLimit(100),
    "mission_text": TextLimit(600, soft=True),
    "process_title": TextLimit(80),
    "process_lead": TextLimit(120),
    "blog_title": TextLimit(80),
    "blog_lead": TextLimit(180, soft=True),
    "intro_title": TextLimit(100),
    "intro_text": TextLimit(900, soft=True),
    "team_title": TextLimit(80),
    "team_lead": TextLimit(280, soft=True),
    "footer_cta_title": TextLimit(60),
    "footer_cta_text": TextLimit(280, soft=True),
    "header_cta_label": TextLimit(40),
    "header_services_label": TextLimit(30),
    "form_phone_placeholder": TextLimit(40),
    "form_email_placeholder": TextLimit(60),
    "form_message_placeholder": TextLimit(80),
    "form_submit_label": TextLimit(40),
    "form_consent_text": TextLimit(220, soft=True),
    "body": TextLimit(20000, soft=True),
}


def image_profile_for_key(key: str) -> ImageProfile:
    low = (key or "").lower()
    if "hero" in low:
        return IMAGE_PROFILES["hero"]
    if "mission" in low or "background" in low or key.startswith("style_"):
        return IMAGE_PROFILES["mission"] if "mission" in low else IMAGE_PROFILES["style"]
    if "card" in low:
        return IMAGE_PROFILES["card"]
    if "team" in low or "photo" in low:
        return IMAGE_PROFILES["team"]
    return IMAGE_PROFILES["default"]


def text_limit_for_key(key: str) -> TextLimit | None:
    if key in TEXT_LIMITS:
        return TEXT_LIMITS[key]
    if key.endswith("_cta") or key.endswith("_cta_label") or key.endswith("_label"):
        return TextLimit(40)
    if key.endswith("_title") or key.endswith("_eyebrow"):
        return TextLimit(100)
    if key.endswith("_lead") or key.endswith("_subtitle"):
        return TextLimit(160, soft=True)
    if key.endswith("_text") or key.endswith("_body"):
        return TextLimit(800, soft=True)
    if key.endswith("_placeholder"):
        return TextLimit(60)
    return None


def help_for_key(key: str, *, page: str = "") -> str:
    parts: list[str] = []
    if key.endswith("_image") or key == "style_background_image":
        parts.append(image_profile_for_key(key).hint)
    elif key.endswith("_section_visible") or key.endswith("_visible"):
        parts.append("Якщо вимкнено — секція не показується на сайті.")
    elif key in {"seo_title", "seo_description"}:
        parts.append("Мета-теги для пошукових систем.")
    limit = text_limit_for_key(key)
    if limit and not key.endswith("_image"):
        parts.append(limit.hint)
    return " ".join(parts)


def help_for_section(page_slug: str, section_slug: str) -> str:
    if section_slug == "style":
        return "Кольори та фон застосовуються до контенту сторінки між шапкою і підвалом."
    return ""
