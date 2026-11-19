"""CMS widgets для Unfold admin."""

import json

from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget
from django.forms import Media, Widget
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES, UnfoldAdminFileFieldWidget

CMS_COUNTER_MEDIA = Media(
    js=("js/admin/cms_char_counter.js",),
    css={"all": ("css/admin/cms_char_counter.css",)},
)


def _apply_max_chars(attrs: dict, max_chars: int | None, *, hard: bool) -> dict:
    if not max_chars:
        return attrs
    attrs["data-max-chars"] = str(max_chars)
    if hard:
        attrs["maxlength"] = str(max_chars)
    return attrs


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None, *, max_chars: int | None = None, hard_limit: bool = True):
        attrs = dict(attrs or {})
        existing = attrs.get("class", "")
        merged = list(INPUT_CLASSES) + ["cms-countable"]
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs = _apply_max_chars(attrs, max_chars, hard=hard_limit)
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return super().media + CMS_COUNTER_MEDIA


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs=None, *, max_chars: int | None = None, hard_limit: bool = False):
        attrs = dict(attrs or {})
        rows = attrs.pop("rows", 4)
        existing = attrs.get("class", "")
        merged = list(TEXTAREA_CLASSES) + ["cms-countable"]
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs["rows"] = rows
        attrs = _apply_max_chars(attrs, max_chars, hard=hard_limit)
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return super().media + CMS_COUNTER_MEDIA


class CmsImageFieldWidget(UnfoldAdminFileFieldWidget):
    """Upload, велике превʼю і мініатюра поточного або запасного фото."""

    template_name = "unfold/widgets/cms_image_input.html"

    def __init__(self, attrs=None, *, hint: str = "", preview_url: str = "", fallback_url: str = ""):
        self.hint = hint or ""
        self.preview_url = preview_url or ""
        self.fallback_url = fallback_url or ""
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        uploaded = ""
        if value is not None and getattr(value, "name", ""):
            try:
                uploaded = value.url
            except Exception:
                uploaded = ""
        url = uploaded or self.preview_url or self.fallback_url
        widget = context["widget"]
        widget["preview_url"] = url
        widget["preview_fallback"] = bool(url and not uploaded)
        widget["hint"] = self.hint
        widget["attrs"]["accept"] = "image/*"
        return context


class CmsTinyMCEWidget(AdminTextareaWidget):
    def __init__(self, attrs=None, *, max_chars: int | None = None, hard_limit: bool = False):
        attrs = dict(attrs or {})
        rows = attrs.pop("rows", 14)
        existing = attrs.get("class", "")
        merged = list(TEXTAREA_CLASSES) + ["cms-tinymce", "cms-countable"]
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs["rows"] = rows
        attrs = _apply_max_chars(attrs, max_chars, hard=hard_limit)
        super().__init__(attrs=attrs)

    class Media:
        js = (
            "https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js",
            "js/admin/cms_tinymce.js",
            "js/admin/cms_char_counter.js",
        )
        css = {
            "all": (
                "css/admin/cms_tinymce.css",
                "css/admin/cms_char_counter.css",
            ),
        }


class CmsAdminColorWidget(Widget):
    def __init__(self, *, default_color: str = "#12263a", attrs=None):
        self.default_color = default_color
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        val = (value or "").strip() or self.default_color
        if not val.startswith("#"):
            val = self.default_color
        hex_class = " ".join([*INPUT_CLASSES, "cms-color-picker__hex"])
        return format_html(
            '<div class="cms-color-picker">'
            '<input type="color" class="cms-color-picker__swatch" value="{}" '
            'oninput="this.parentNode.querySelector(\'[name={}]\').value=this.value" />'
            '<input type="text" name="{}" value="{}" class="{}" '
            'oninput="var c=this.parentNode.querySelector(\'input[type=color]\');'
            'if(/^#[0-9a-fA-F]{{3,8}}$/.test(this.value))c.value=this.value" />'
            "</div>",
            val,
            name,
            name,
            val,
            hex_class,
        )


class CmsAdminImageWidget(CmsImageFieldWidget):
    pass


def _icon_markup(name: str) -> str:
    from src.core.templatetags.vartis_icons import ICONS

    data = ICONS.get(name or "")
    if not data:
        return ""
    return (
        f'<span class="cms-icon__pic"><svg width="28" height="28" viewBox="{data["viewBox"]}" '
        f'fill="none" aria-hidden="true">{data["body"]}</svg></span>'
    )


class CmsAdminIconWidget(CmsAdminTextInputWidget):
    """Поле ключа іконки з малюнком поруч."""

    def render(self, name, value, attrs=None, renderer=None):
        from src.core.templatetags.vartis_icons import ICONS

        picture = mark_safe(_icon_markup(value or ""))
        control = super().render(name, value, attrs, renderer)
        payload = mark_safe(
            '<script type="application/json" id="cms-icon-data">'
            + json.dumps(ICONS).replace("<", "\\u003c")
            + "</script>"
        )
        return format_html(
            '<div class="cms-icon" data-cms-icon>{}{}{}</div>',
            picture,
            control,
            payload,
        )
