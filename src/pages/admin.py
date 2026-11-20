from django import forms
from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, StackedInline
from src.core.admin_guidelines import image_profile_for_key, text_limit_for_key
from src.core.admin_site_content_widgets import (
    CmsAdminIconWidget,
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
    CmsImageFieldWidget,
    CmsTinyMCEWidget,
)
from src.core.admin_i18n import BilingualAdminMixin
from src.pages.admin_team_widgets import CareerPathWidget, ExpertiseListWidget

from .models import (
    AboutPage,
    AboutPrinciple,
    AboutProcessStep,
    AboutStat,
    AboutIntroStat,
    AboutKeyStat,
    AnalysisInclude,
    AnalysisPage,
    AnalysisPriceRow,
    AnalysisRisk,
    AnalysisStep,
    AnalysisWhy,
    HomeAdvantage,
    HomeDirection,
    HomePage,
    HomeProcessStep,
    ServiceAdvantage,
    ServiceMethodStep,
    ServicePage,
    ServiceScopeItem,
    TeamMember,
)


class _ParentPageMixin(BilingualAdminMixin):
    """Автоматично привʼязує ListItem до singleton-сторінки."""

    parent_model = None
    parent_field = 'page'

    def save_model(self, request, obj, form, change):
        if self.parent_model is not None and not getattr(obj, f'{self.parent_field}_id', None):
            setattr(obj, self.parent_field, self.parent_model.load())
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        excluded = list(super().get_exclude(request, obj) or [])
        if self.parent_field not in excluded:
            excluded.append(self.parent_field)
        return excluded

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'icon':
            kwargs['widget'] = CmsAdminIconWidget()
        elif isinstance(db_field, models.ImageField):
            kwargs['widget'] = CmsImageFieldWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


SERVICE_RICH_FIELDS = (
    'hero_text',
    'scope_text',
    'order_text',
    'card_text',
)

SERVICE_IMAGE_FIELDS = (
    'hero_image',
    'card_image',
)

SERVICE_TEXT_LIMITS = {
    'seo_title': 70,
    'seo_description': 160,
    'h1': 90,
    'title': 90,
    'short': 160,
    'scope_title': 80,
    'method_title': 80,
    'advantages_title': 80,
    'order_title': 80,
    'tags': 120,
    'icon': 40,
}


def _preview_url(file_field) -> str:
    if not file_field:
        return ''
    try:
        return file_field.url
    except Exception:
        return ''


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        rich_names = []
        for name in SERVICE_RICH_FIELDS:
            rich_names.append(name)
            rich_names.append(f'{name}_en')
        for name in rich_names:
            if name not in self.fields:
                continue
            limit = text_limit_for_key(name) or text_limit_for_key(name.replace('hero_', '').replace('card_', ''))
            max_chars = limit.max_chars if limit else 900
            self.fields[name].widget = CmsTinyMCEWidget(
                attrs={'rows': 10},
                max_chars=max_chars,
                hard_limit=False,
            )
            self.fields[name].help_text = (
                f'Рекомендовано до {max_chars} символів (щоб не зламати верстку).'
            )

        for name, max_chars in SERVICE_TEXT_LIMITS.items():
            if name == 'icon':
                continue
            for field_name in (name, f'{name}_en'):
                if field_name not in self.fields:
                    continue
                field = self.fields[field_name]
                if isinstance(field.widget, forms.Textarea):
                    field.widget = CmsAdminTextareaWidget(
                        attrs={'rows': 3},
                        max_chars=max_chars,
                        hard_limit=True,
                    )
                else:
                    field.widget = CmsAdminTextInputWidget(max_chars=max_chars, hard_limit=True)
                field.help_text = f'Максимум {max_chars} символів.'
                field.max_length = max_chars

        for name in SERVICE_IMAGE_FIELDS:
            if name not in self.fields:
                continue
            profile = image_profile_for_key(name)
            preview = _preview_url(getattr(instance, name, None) if instance else None)
            self.fields[name].widget = CmsImageFieldWidget(
                hint=profile.hint,
                preview_url=preview,
                fallback_url='' if preview else '/static/images/hero.webp',
            )
        if 'icon' in self.fields:
            self.fields['icon'].widget = CmsAdminIconWidget()
            self.fields[name].help_text = profile.hint


class _CountableInlineForm(forms.ModelForm):
    """Inline з лімітами й лічильником для Char/Text полів."""

    text_limits: dict[str, int] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        limits = {}
        for name, max_chars in self.text_limits.items():
            limits[name] = max_chars
            limits[f'{name}_en'] = max_chars
        for name, max_chars in limits.items():
            if name not in self.fields:
                continue
            field = self.fields[name]
            if isinstance(self._meta.model._meta.get_field(name), models.TextField):
                field.widget = CmsAdminTextareaWidget(
                    attrs={'rows': 3},
                    max_chars=max_chars,
                    hard_limit=False,
                )
                field.help_text = f'Рекомендовано до {max_chars} символів.'
            else:
                field.widget = CmsAdminTextInputWidget(max_chars=max_chars, hard_limit=True)
                field.help_text = f'Максимум {max_chars} символів.'
                field.max_length = max_chars


class ServiceScopeItemForm(_CountableInlineForm):
    text_limits = {'text': 160}

    class Meta:
        model = ServiceScopeItem
        fields = '__all__'


class ServiceMethodStepForm(_CountableInlineForm):
    text_limits = {'number': 8, 'title': 80, 'text': 400}

    class Meta:
        model = ServiceMethodStep
        fields = '__all__'


class ServiceAdvantageForm(_CountableInlineForm):
    text_limits = {'title': 80, 'text': 280}

    class Meta:
        model = ServiceAdvantage
        fields = '__all__'


class ServiceScopeItemInline(BilingualAdminMixin, StackedInline):
    model = ServiceScopeItem
    form = ServiceScopeItemForm
    extra = 0
    fields = (('text', 'order'),)
    classes = ['vartis-inline-card']


class ServiceMethodStepInline(BilingualAdminMixin, StackedInline):
    model = ServiceMethodStep
    form = ServiceMethodStepForm
    extra = 0
    fields = (('number', 'title', 'order'), 'text')
    classes = ['vartis-inline-card']


class ServiceAdvantageInline(BilingualAdminMixin, StackedInline):
    model = ServiceAdvantage
    form = ServiceAdvantageForm
    extra = 0
    fields = (('title', 'order'), 'text')
    classes = ['vartis-inline-card']


@admin.register(ServicePage)
class ServicePageAdmin(BilingualAdminMixin, ModelAdmin):
    form = ServicePageForm
    list_display = ('title', 'slug', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    prepopulated_fields = {}
    inlines = [ServiceScopeItemInline, ServiceMethodStepInline, ServiceAdvantageInline]
    fieldsets = (
        ('SEO', {
            'classes': ('tab',),
            'fields': ('seo_title', 'seo_description', 'h1'),
        }),
        ('Основне', {
            'classes': ('tab',),
            'fields': (
                'slug', 'title', 'short', 'order', 'is_published',
                'icon', 'tags', 'card_image', 'card_text',
            ),
        }),
        ('Перший екран', {
            'classes': ('tab',),
            'fields': ('hero_text', 'hero_image'),
        }),
        ('Блоки', {
            'classes': ('tab',),
            'fields': (
                'scope_title', 'scope_text', 'method_title',
                'advantages_title', 'order_title', 'order_text',
            ),
        }),
    )


@admin.register(HomeDirection)
class HomeDirectionAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = HomePage
    list_display = ('title', 'is_visible', 'order')
    list_editable = ('is_visible', 'order')
    list_filter = ('is_visible',)
    ordering = ('order', 'id')
    search_fields = ('title', 'text')
    fields = ('title', 'text', 'image', 'href', 'is_visible', 'order')


@admin.register(HomeAdvantage)
class HomeAdvantageAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = HomePage
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)
    ordering = ('order', 'id')
    search_fields = ('title',)


@admin.register(HomeProcessStep)
class HomeProcessStepAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = HomePage
    list_display = ('number', 'title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    search_fields = ('title',)


@admin.register(AboutPrinciple)
class AboutPrincipleAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)
    ordering = ('order', 'id')


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        for rich_name in ('bio', 'bio_en'):
            if rich_name not in self.fields:
                continue
            self.fields[rich_name].widget = CmsTinyMCEWidget(
                attrs={'rows': 10},
                max_chars=2000,
                hard_limit=False,
            )
            self.fields[rich_name].help_text = 'Рекомендовано до 2000 символів.'
        for json_name in ('expertise', 'expertise_en'):
            if json_name in self.fields:
                self.fields[json_name].widget = ExpertiseListWidget()
                self.fields[json_name].help_text = (
                    'Кожен рядок — окремий пункт списку на сайті. Розмітка підставляється автоматично.'
                )
        for path_name in ('career_path', 'career_path_en'):
            if path_name in self.fields:
                self.fields[path_name].widget = CareerPathWidget()
                self.fields[path_name].help_text = (
                    'Заголовок — жирний і золотий, роки — окремим рядком, як на сайті.'
                )
        if 'photo' in self.fields:
            profile = image_profile_for_key('team_photo')
            self.fields['photo'].widget = CmsImageFieldWidget(
                hint=profile.hint,
                preview_url=_preview_url(getattr(instance, 'photo', None) if instance else None),
            )
            self.fields['photo'].help_text = profile.hint
        for name, max_chars in (
            ('name', 80), ('name_en', 80),
            ('role', 120), ('role_en', 120),
            ('regalia', 200), ('regalia_en', 200),
        ):
            if name in self.fields:
                self.fields[name].widget = CmsAdminTextInputWidget(
                    max_chars=max_chars,
                    hard_limit=True,
                )
                self.fields[name].help_text = f'Максимум {max_chars} символів.'


@admin.register(TeamMember)
class TeamMemberAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    form = TeamMemberForm
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    search_fields = ('name', 'role')


class _AboutStatBlockAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    stat_block = AboutStat.BLOCK_KEY
    list_display = ('value', 'label', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    fields = ('value', 'label', 'order')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(block=self.stat_block)

    def get_exclude(self, request, obj=None):
        excluded = list(super().get_exclude(request, obj) or [])
        if 'block' not in excluded:
            excluded.append('block')
        return excluded

    def save_model(self, request, obj, form, change):
        obj.block = self.stat_block
        super().save_model(request, obj, form, change)


@admin.register(AboutIntroStat)
class AboutIntroStatAdmin(_AboutStatBlockAdmin):
    stat_block = AboutStat.BLOCK_INTRO


@admin.register(AboutKeyStat)
class AboutKeyStatAdmin(_AboutStatBlockAdmin):
    stat_block = AboutStat.BLOCK_KEY


@admin.register(AboutProcessStep)
class AboutProcessStepAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AboutPage
    list_display = ('number', 'title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisStep)
class AnalysisStepAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('number', 'title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisRisk)
class AnalysisRiskAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisInclude)
class AnalysisIncludeAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisWhy)
class AnalysisWhyAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(AnalysisPriceRow)
class AnalysisPriceRowAdmin(_ParentPageMixin, ModelAdmin):
    parent_model = AnalysisPage
    list_display = ('number', 'title', 'price_note', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


from . import admin_lists  # noqa: E402,F401
