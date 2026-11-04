"""CMS widgets для Unfold admin."""

from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget
from django.forms import Media, Widget
from django.utils.html import format_html
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
    """Upload + превʼю поточного зображення + підказка розміру/ваги."""

    def __init__(self, attrs=None, *, hint: str = "", preview_url: str = ""):
        self.hint = hint or ""
        self.preview_url = preview_url or ""
        super().__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = {} if attrs is None else dict(attrs)
        # Щоб Unfold не малював друге превʼю поруч із нашим.
        if attrs.get("accept") == "image/*":
            attrs["accept"] = "image/png,image/jpeg,image/webp,image/svg+xml"
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        preview = ""
        url = self.preview_url
        if not url and value and hasattr(value, "url"):
            try:
                url = value.url
            except Exception:
                url = ""
        if url:
            preview = format_html(
                '<div class="site-content-editor__img-preview">'
                '<img src="{}" alt="" width="240" height="160" loading="lazy" decoding="async">'
                "</div>",
                url,
            )
        hint = ""
        if self.hint:
            hint = format_html(
                '<p class="site-content-editor__img-hint">{}</p>',
                self.hint,
            )
        return format_html("{}{}{}", preview, hint, html)


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
    def __init__(self, *, default_color: str = "#0b1626", attrs=None):
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
