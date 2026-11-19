from django.urls import reverse
from django.views.generic import DetailView, ListView

from src.core.og_image import og_image_from_field
from src.core.seo import absolute_url
from src.leads.forms import LeadForm
from src.pages.cms import StyledPageMixin

from .models import Article, BlogPage

PER_PAGE = 5

# Порядок чіпів як у Blog.dc.html / articles.js (перша поява в стрічці)
CHIP_ORDER = (
    'Перевірка контрагентів',
    'Аналітика',
    'Корпоративна безпека',
    'Консалтинг',
)


def _ordered_categories():
    present = set(
        Article.objects.filter(is_published=True)
        .values_list('category', flat=True)
        .distinct()
    )
    ordered = [c for c in CHIP_ORDER if c in present]
    extras = sorted(present - set(CHIP_ORDER))
    return ordered + extras


class ArticleListView(StyledPageMixin, ListView):
    page_style_key = 'blog'
    model = Article
    template_name = 'blog/list.html'
    context_object_name = 'articles'
    paginate_by = PER_PAGE

    def get_queryset(self):
        qs = Article.objects.filter(is_published=True).prefetch_related('blocks')
        cat = self.request.GET.get('cat', '').strip()
        if cat:
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        cat = self.request.GET.get('cat', '').strip()
        page_obj = ctx['page_obj']
        objects = list(page_obj.object_list)
        featured = objects[0] if page_obj.number == 1 and objects else None
        grid = objects[1:] if featured else objects
        ctx.update({
            'featured': featured,
            'grid': grid,
            'current_cat': cat,
            'categories': _ordered_categories(),
            'lead_form': LeadForm(),
            'seo_title': BlogPage.load().seo_title,
            'seo_description': BlogPage.load().seo_description,
            'h1': BlogPage.load().h1,
            'hero_text': BlogPage.load().hero_text,
            'crumbs': [{'label': BlogPage.load().crumb, 'url': ''}],
            'canonical_url': absolute_url(self.request, reverse('blog:list')),
        })
        if cat or page_obj.number > 1:
            ctx['seo_robots'] = 'noindex, follow'
        if self.request.htmx:
            ctx['partial'] = True
        return ctx

    def get_template_names(self):
        if self.request.htmx:
            return ['blog/partials/feed.html']
        return [self.template_name]


class ArticleDetailView(StyledPageMixin, DetailView):
    page_style_key = 'blog'
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    slug_field = 'slug'

    def get_queryset(self):
        return Article.objects.filter(is_published=True).prefetch_related('blocks')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        article = ctx['article']
        same = list(
            Article.objects.filter(is_published=True, category=article.category)
            .exclude(pk=article.pk)[:3]
        )
        if len(same) < 3:
            extra = list(
                Article.objects.filter(is_published=True)
                .exclude(pk=article.pk)
                .exclude(pk__in=[a.pk for a in same])[: 3 - len(same)]
            )
            same.extend(extra)
        ctx['related'] = same
        ctx['lead_form'] = LeadForm()
        ctx['share_url'] = self.request.build_absolute_uri(article.get_absolute_url())
        ctx['crumbs'] = [
            {'label': BlogPage.load().crumb, 'url': reverse('blog:list')},
            {'label': article.category, 'url': ''},
        ]
        ctx['seo_title'] = article.seo_title or f'{article.title} — VARTIS INTELLIGENCE'
        ctx['seo_description'] = article.seo_description or article.excerpt
        if article.image:
            ctx['og_image'] = og_image_from_field(self.request, article.image)
        ctx['og_type'] = 'article'
        return ctx
