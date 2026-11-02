from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from src.leads.forms import LeadForm

from .models import Article

PER_PAGE = 6


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/list.html'
    context_object_name = 'articles'
    paginate_by = PER_PAGE

    def get_queryset(self):
        qs = Article.objects.filter(is_published=True)
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
        categories = (
            Article.objects.filter(is_published=True)
            .values_list('category', flat=True)
            .distinct()
            .order_by('category')
        )
        ctx.update({
            'featured': featured,
            'grid': grid,
            'current_cat': cat,
            'categories': categories,
            'lead_form': LeadForm(),
            'seo_title': 'Блог — VARTIS INTELLIGENCE',
            'seo_description': (
                'Аналітика та експертні матеріали про перевірку контрагентів, '
                'стратегічну розвідку, корпоративну безпеку та управління ризиками.'
            ),
            'h1': 'Блог',
            'hero_text': (
                'Аналітика та експертні матеріали про перевірку контрагентів, '
                'стратегічну розвідку, корпоративну безпеку та управління ризиками'
            ),
            'crumbs': [{'label': 'Блог', 'url': ''}],
        })
        if self.request.htmx:
            ctx['partial'] = True
        return ctx

    def get_template_names(self):
        if self.request.htmx:
            return ['blog/partials/feed.html']
        return [self.template_name]


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    slug_field = 'slug'

    def get_queryset(self):
        return Article.objects.filter(is_published=True).prefetch_related('blocks')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        article = ctx['article']
        ctx['related'] = (
            Article.objects.filter(is_published=True, category=article.category)
            .exclude(pk=article.pk)[:3]
        )
        ctx['lead_form'] = LeadForm()
        return ctx
