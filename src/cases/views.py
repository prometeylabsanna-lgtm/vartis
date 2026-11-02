from django.views.generic import DetailView, ListView

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
            'seo_title': 'Кейси — VARTIS INTELLIGENCE',
            'seo_description': 'Реалізовавані проєкти та демонстраційні приклади.',
            'h1': 'Кейси',
        })
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
        ctx['lead_form'] = LeadForm()
        return ctx
