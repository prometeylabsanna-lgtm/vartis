"""CMS widgets для Unfold admin."""

from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget
from django.forms import Widget
from django.utils.html import format_html
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None):
        attrs = dict(attrs or {})
        existing = attrs.get("class", "")
        merged = list(INPUT_CLASSES)
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        super().__init__(attrs=attrs)


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs=None):
        attrs = dict(attrs or {})
        rows = attrs.pop("rows", 4)
        existing = attrs.get("class", "")
        merged = list(TEXTAREA_CLASSES)
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs["rows"] = rows
        super().__init__(attrs=attrs)


class CmsTinyMCEWidget(AdminTextareaWidget):
    def __init__(self, attrs=None):
        attrs = dict(attrs or {})
        rows = attrs.pop("rows", 14)
        existing = attrs.get("class", "")
        merged = list(TEXTAREA_CLASSES) + ["cms-tinymce"]
        if existing:
            merged = list(dict.fromkeys([*merged, *existing.split()]))
        attrs["class"] = " ".join(merged)
        attrs["rows"] = rows
        super().__init__(attrs=attrs)

    class Media:
        js = (
            "https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js",
            "js/admin/cms_tinymce.js",
        )
        css = {"all": ("css/admin/cms_tinymce.css",)}


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
