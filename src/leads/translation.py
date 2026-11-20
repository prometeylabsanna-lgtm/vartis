from modeltranslation.translator import TranslationOptions, register

from src.leads.models import LeadModal


@register(LeadModal)
class LeadModalTR(TranslationOptions):
    fields = (
        'title',
        'lead',
        'name_label',
        'phone_label',
        'email_label',
        'message_label',
        'phone_placeholder',
        'email_placeholder',
        'message_placeholder',
        'consent_prefix',
        'submit_label',
        'thanks_title',
        'thanks_text',
        'error_required',
        'error_name',
        'error_phone',
        'error_email',
        'error_message',
        'error_consent',
    )
