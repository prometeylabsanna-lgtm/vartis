from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import LeadForm, clean_form_id, clean_form_variant, clean_source_page
from .services import notify_lead
from .throttle import lead_submit_limited

_RATE_LIMIT_MESSAGE = 'Забагато спроб. Спробуйте через кілька хвилин.'


@require_POST
def lead_submit(request):
    variant = clean_form_variant(request.POST.get('form_variant', ''))
    form_id = clean_form_id(request.POST.get('form_id', ''))
    is_modal = variant == 'modal'
    template = 'leads/partials/modal_panel.html' if is_modal else 'leads/partials/form.html'
    context = {
        'form_variant': variant,
        'form_id': form_id,
    }

    if lead_submit_limited(request):
        form = LeadForm(request.POST)
        form.add_error(None, _RATE_LIMIT_MESSAGE)
        return render(request, template, {'lead_form': form, **context}, status=429)

    if (request.POST.get('honeypot') or '').strip():
        return render(request, 'leads/partials/thanks.html', {
            'variant': 'modal' if is_modal else variant,
        })

    form = LeadForm(request.POST)
    if form.is_valid():
        lead = form.save(commit=False)
        lead.source_page = clean_source_page(request.POST.get('source_page', ''))
        lead.save()
        notify_lead(lead)
        return render(request, 'leads/partials/thanks.html', {
            'variant': 'modal' if is_modal else variant,
        })

    return render(
        request,
        template,
        {'lead_form': form, **context},
        status=422,
    )
