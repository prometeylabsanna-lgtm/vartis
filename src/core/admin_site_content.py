"""Динамічна CMS-форма секції + view."""

from __future__ import annotations

import re

from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_guidelines import (
    help_for_key,
    help_for_section,
    image_profile_for_key,
    text_limit_for_key,
)
from src.core.admin_site_content_widgets import (
    CmsAdminColorWidget,
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
    CmsTinyMCEWidget,
)
from src.core.block_defaults import (
    INLINE_KEYS,
    MULTILINE_KEYS,
    STATIC_FALLBACKS,
    get_block_content_type,
    get_block_default,
    get_block_label,
    is_richtext_key,
    is_visibility_key,
)
from src.core.models import PageStyle, SiteBlock, SiteSettings
from src.core.models_cms import clear_site_blocks_cache
from src.core.site_content_registry import get_section

_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def _clean_color(raw: str, *, default: str) -> str:
    value = (raw or "").strip()
    if not value:
        return ""
    if not _HEX_RE.match(value):
        raise forms.ValidationError("Вкажіть колір у форматі #RRGGBB")
    if len(value) == 4:
        value = f"#{value[1] * 2}{value[2] * 2}{value[3] * 2}"
    if value.lower() == default.lower():
        return ""
    return value.lower()


def _image_preview_url(page: str, key: str, block: SiteBlock | None) -> tuple[str, bool]:
    if block is not None and block.image:
        try:
            return block.image.url, False
        except Exception:
            pass
    static_path = STATIC_FALLBACKS.get((page, key), "")
    if not static_path:
        return "", False
    from django.templatetags.static import static

    return static(static_path), True


def load_section_blocks(page: str, keys: list[str]) -> dict[str, SiteBlock]:
    result: dict[str, SiteBlock] = {}
    for key in keys:
        defaults = {
            "label": get_block_label(page, key),
            "content_type": get_block_content_type(page, key),
            "text_html": get_block_default(page, key),
        }
        block, _ = SiteBlock.objects.get_or_create(page=page, key=key, defaults=defaults)
        result[key] = block
    return result


class SitePageContentForm(forms.Form):
    def __init__(self, *args, section=None, blocks=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section
        self.blocks = blocks or {}

        if section and section.has_page_style:
            style = PageStyle.for_page(section.page_slug)
            self.fields["style_background"] = forms.CharField(
                required=False,
                label="Колір фону",
                initial=(style.background_color or "").strip() or PageStyle.DEFAULT_BACKGROUND,
                widget=CmsAdminColorWidget(default_color=PageStyle.DEFAULT_BACKGROUND),
            )
            self.fields["style_text"] = forms.CharField(
                required=False,
                label="Колір тексту",
                initial=(style.text_color or "").strip() or PageStyle.DEFAULT_TEXT,
                widget=CmsAdminColorWidget(default_color=PageStyle.DEFAULT_TEXT),
            )
            self.fields["style_accent"] = forms.CharField(
                required=False,
                label="Колір акценту",
                initial=(style.accent_color or "").strip() or PageStyle.DEFAULT_ACCENT,
                widget=CmsAdminColorWidget(default_color=PageStyle.DEFAULT_ACCENT),
            )
            style_hint = image_profile_for_key("style_background_image").hint
            self.fields["style_background_image"] = forms.ImageField(
                required=False,
                label="Фонове зображення",
                help_text=style_hint,
                widget=UnfoldAdminFileFieldWidget(),
            )
            self.fields["style_glass"] = forms.BooleanField(
                required=False,
                label="Ефект скла (glass)",
                initial=style.glass_enabled,
                widget=UnfoldBooleanWidget(),
            )
            self._page_style = style
        else:
            self._page_style = None

        if not section:
            return

        if section.visibility_key:
            block = self.blocks.get(section.visibility_key)
            initial = True
            if block is not None:
                initial = block.text_html not in {"0", "false", "False", ""}
            self.fields["section_visible"] = forms.BooleanField(
                required=False,
                initial=initial,
                label="Показувати секцію на сайті",
                widget=UnfoldBooleanWidget(),
            )

        for page, key in section.blocks:
            if section.visibility_key and key == section.visibility_key:
                continue
            block = self.blocks[key]
            ctype = get_block_content_type(page, key)
            label = block.label or get_block_label(page, key)
            help_text = help_for_key(key, page=page)

            if is_visibility_key(key):
                self.fields[f"block__{page}__{key}__visible"] = forms.BooleanField(
                    required=False,
                    initial=block.text_html not in {"0", "false", "False", ""},
                    label=label,
                    help_text=help_text,
                    widget=UnfoldBooleanWidget(),
                )
                continue

            if ctype == "image":
                profile = image_profile_for_key(key)
                self.fields[f"block__{page}__{key}__image"] = forms.ImageField(
                    required=False,
                    label=label,
                    help_text=help_text or profile.hint,
                    widget=UnfoldAdminFileFieldWidget(),
                )
                continue

            if ctype == "url":
                self.fields[f"block__{page}__{key}__link_url"] = forms.CharField(
                    required=False,
                    initial=block.link_url or block.text_html or get_block_default(page, key),
                    label=label,
                    help_text=help_text,
                    widget=CmsAdminTextInputWidget(max_chars=200),
                )
                continue

            limit = text_limit_for_key(key)
            max_chars = limit.max_chars if limit else None
            hard = bool(limit and not limit.soft)
            pair = (page, key)
            if is_richtext_key(page, key):
                widget = CmsTinyMCEWidget(
                    attrs={"rows": 14},
                    max_chars=max_chars,
                    hard_limit=False,
                )
            elif pair in INLINE_KEYS:
                widget = CmsAdminTextInputWidget(
                    max_chars=max_chars or 120,
                    hard_limit=hard if limit else True,
                )
            elif pair in MULTILINE_KEYS:
                widget = CmsAdminTextareaWidget(
                    attrs={"rows": 6},
                    max_chars=max_chars,
                    hard_limit=hard,
                )
            else:
                widget = CmsAdminTextareaWidget(
                    attrs={"rows": 2},
                    max_chars=max_chars or 200,
                    hard_limit=hard if limit else False,
                )
            self.fields[f"block__{page}__{key}__text_html"] = forms.CharField(
                required=False,
                initial=block.text_html,
                label=label,
                help_text=help_text,
                widget=widget,
                max_length=max_chars if (limit and not limit.soft) else None,
            )

    def clean_style_background(self):
        return _clean_color(self.cleaned_data.get("style_background", ""), default=PageStyle.DEFAULT_BACKGROUND)

    def clean_style_text(self):
        return _clean_color(self.cleaned_data.get("style_text", ""), default=PageStyle.DEFAULT_TEXT)

    def clean_style_accent(self):
        return _clean_color(self.cleaned_data.get("style_accent", ""), default=PageStyle.DEFAULT_ACCENT)

    def save(self):
        section = self.section
        if section.visibility_key:
            visible = self.cleaned_data.get("section_visible", True)
            block = self.blocks[section.visibility_key]
            block.text_html = "1" if visible else "0"
            block.content_type = SiteBlock.ContentType.TEXT
            block.save(update_fields=["text_html", "content_type"])

        for name, value in self.cleaned_data.items():
            if not name.startswith("block__"):
                continue
            parts = name.split("__")
            if len(parts) != 4:
                continue
            _, page, key, suffix = parts
            block = self.blocks[key]
            if suffix == "visible":
                block.text_html = "1" if value else "0"
                block.save(update_fields=["text_html"])
            elif suffix == "text_html":
                block.text_html = value or ""
                block.save(update_fields=["text_html"])
            elif suffix == "image":
                if value:
                    block.image = value
                    block.content_type = SiteBlock.ContentType.IMAGE
                    block.save(update_fields=["image", "content_type"])
            elif suffix == "link_url":
                block.link_url = value or ""
                block.content_type = SiteBlock.ContentType.URL
                block.text_html = value or ""
                block.save(update_fields=["link_url", "content_type", "text_html"])

        if self._page_style is not None:
            style = self._page_style
            style.background_color = self.cleaned_data.get("style_background", "")
            style.text_color = self.cleaned_data.get("style_text", "")
            style.accent_color = self.cleaned_data.get("style_accent", "")
            style.glass_enabled = bool(self.cleaned_data.get("style_glass", True))
            img = self.cleaned_data.get("style_background_image")
            if img:
                style.background_image = img
            style.save()

        clear_site_blocks_cache()


def site_content_section_view(request, page_slug: str, section_slug: str, model_admin=None):
    section = get_section(page_slug, section_slug)
    if section is None:
        messages.error(request, "Секцію не знайдено.")
        return redirect("admin:index")

    keys = [key for _, key in section.blocks]
    blocks = load_section_blocks(section.page_slug, keys) if keys else {}

    if request.method == "POST":
        form = SitePageContentForm(request.POST, request.FILES, section=section, blocks=blocks)
        if form.is_valid():
            form.save()
            messages.success(request, "Збережено.")
            return redirect(request.path)
    else:
        form = SitePageContentForm(section=section, blocks=blocks)

    field_groups = []
    if section.has_page_style:
        style_fields = []
        for fname in (
            "style_background",
            "style_text",
            "style_accent",
            "style_background_image",
            "style_glass",
        ):
            if fname in form.fields:
                style_fields.append({
                    "field": form[fname],
                    "preview_url": "",
                    "preview_fallback": False,
                    "image_hint": (
                        image_profile_for_key("style_background_image").hint
                        if fname == "style_background_image"
                        else ""
                    ),
                })
        field_groups.append({
            "title": "Оформлення сторінки",
            "description": "",
            "fields": style_fields,
            "keys": (),
            "tab": "content",
        })

    for group in section.field_groups:
        bound = []
        for key in group.keys:
            if section.visibility_key and key == section.visibility_key:
                if "section_visible" in form.fields:
                    bound.append({
                        "field": form["section_visible"],
                        "preview_url": "",
                        "preview_fallback": False,
                        "image_hint": "",
                    })
                continue
            page = section.page_slug
            ctype = get_block_content_type(page, key)
            if is_visibility_key(key):
                name = f"block__{page}__{key}__visible"
            elif ctype == "image":
                name = f"block__{page}__{key}__image"
            elif ctype == "url":
                name = f"block__{page}__{key}__link_url"
            else:
                name = f"block__{page}__{key}__text_html"
            if name not in form.fields:
                continue
            preview_url = ""
            preview_fallback = False
            image_hint = ""
            if ctype == "image":
                preview_url, preview_fallback = _image_preview_url(page, key, blocks.get(key))
                image_hint = image_profile_for_key(key).hint
            bound.append({
                "field": form[name],
                "preview_url": preview_url,
                "preview_fallback": preview_fallback,
                "image_hint": image_hint,
            })
        field_groups.append({
            "title": group.title,
            "description": group.description,
            "fields": bound,
            "keys": group.keys,
            "tab": getattr(group, "tab", "content") or "content",
        })

    style_preview = ""
    if section.has_page_style and form._page_style and form._page_style.background_image:
        try:
            style_preview = form._page_style.background_image.url
        except Exception:
            style_preview = ""

    has_seo_tab = any(g.get("tab") == "seo" for g in field_groups)
    context = {
        **(model_admin.admin_site.each_context(request) if model_admin else {}),
        "title": section.title,
        "section": section,
        "section_hint": help_for_section(section.page_slug, section.slug),
        "form": form,
        "field_groups": field_groups,
        "has_seo_tab": has_seo_tab,
        "blocks_map": blocks,
        "style_bg_preview": style_preview,
        "opts": SiteSettings._meta,
        "has_view_permission": True,
        "has_change_permission": True,
        "preview_url": section.preview_url,
        "media": form.media,
    }
    return render(request, "admin/core/site_content_page.html", context)
