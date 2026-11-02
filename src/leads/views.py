from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import LeadForm
from .services import notify_lead


@require_POST
def lead_submit(request):
    form = LeadForm(request.POST)
    source = request.POST.get('source_page', request.META.get('HTTP_REFERER', ''))[:200]
    template = 'leads/partials/form.html'
    if 'modal' in request.POST.get('form_variant', ''):
        template = 'leads/partials/modal_form.html'

    if form.is_valid():
        lead = form.save(commit=False)
        lead.source_page = source
        lead.save()
        notify_lead(lead)
        return render(request, 'leads/partials/thanks.html', {
            'variant': request.POST.get('form_variant', 'footer'),
        })

    return render(
        request,
        template,
        {
            'lead_form': form,
            'form_variant': request.POST.get('form_variant', 'footer'),
            'form_id': request.POST.get('form_id', 'lead-form'),
        },
        status=422,
    )
