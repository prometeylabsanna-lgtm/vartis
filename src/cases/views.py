from django.urls import reverse
from django.views.generic import DetailView, ListView

from src.core.seo import absolute_url, media_or_static_absolute
from src.core.seo_copy import SEO
from src.leads.forms import LeadForm

from .models import CaseStudy


class CaseListView(ListView):
    model = CaseStudy
    template_name = 'cases/list.html'
    context_object_name = 'cases'

    def get_queryset(self):
        qs = CaseStudy.objects.filter(is_published=True)
        cat = self.request.GET.get('cat', '').strip()
        if cat:
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cat = self.request.GET.get('cat', '').strip()
        categories = (
            CaseStudy.objects.filter(is_published=True)
            .values_list('category', flat=True)
            .distinct()
            .order_by('category')
        )
        ctx.update({
            'current_cat': cat,
            'categories': categories,
            'lead_form': LeadForm(),
            'seo_title': SEO['cases']['title'],
            'seo_description': SEO['cases']['description'],
            'h1': 'Кейси',
            'crumbs': [{'label': 'Кейси', 'url': ''}],
            'canonical_url': absolute_url(self.request, reverse('cases:list')),
        })
        if cat:
            ctx['seo_robots'] = 'noindex, follow'
        return ctx

    def get_template_names(self):
        if self.request.htmx:
            return ['cases/partials/grid.html']
        return [self.template_name]


class CaseDetailView(DetailView):
    model = CaseStudy
    template_name = 'cases/detail.html'
    context_object_name = 'case'
    slug_field = 'slug'

    def get_queryset(self):
        return CaseStudy.objects.filter(is_published=True).prefetch_related('stats', 'blocks')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        case = ctx['case']
        ctx['lead_form'] = LeadForm()
        ctx['seo_title'] = case.seo_title or f'{case.title} — VARTIS INTELLIGENCE'
        ctx['seo_description'] = case.seo_description or case.excerpt
        ctx['crumbs'] = [
            {'label': 'Кейси', 'url': reverse('cases:list')},
            {'label': case.title, 'url': ''},
        ]
        if case.image:
            ctx['og_image'] = media_or_static_absolute(self.request, case.image.url)
        return ctx
