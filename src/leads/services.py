import json
import logging
import urllib.request

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_lead(lead):
    body = (
        f"Нова заявка з сайту Vartis\n"
        f"Ім'я: {lead.name}\n"
        f"Телефон: {lead.phone}\n"
        f"Email: {lead.email}\n"
        f"Сторінка: {lead.source_page}\n"
        f"Повідомлення: {lead.message}\n"
    )
    _send_email(body)
    _send_telegram(body)
    _send_crm(lead)


def _send_email(body):
    to = settings.LEAD_EMAIL_TO
    if not to:
        return
    try:
        send_mail(
            subject='Нова заявка — Vartis Intelligence',
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to],
            fail_silently=True,
        )
    except Exception:
        logger.exception('Lead email failed')


def _send_telegram(body):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        data = json.dumps({'chat_id': chat_id, 'text': body}).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        urllib.request.urlopen(req, timeout=8)
    except Exception:
        logger.exception('Lead telegram failed')


def _send_crm(lead):
    webhook = settings.CRM_WEBHOOK_URL
    if not webhook:
        return
    payload = {
        'name': lead.name,
        'phone': lead.phone,
        'email': lead.email,
        'message': lead.message,
        'source': lead.source_page,
        'status': 'Новий лід',
    }
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            webhook,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        urllib.request.urlopen(req, timeout=8)
    except Exception:
        logger.exception('Lead CRM webhook failed')
