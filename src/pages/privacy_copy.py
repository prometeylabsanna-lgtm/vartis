"""Затверджений текст політики конфіденційності."""

from __future__ import annotations

from html import escape

from src.core.contact_defaults import resolve_public_contacts
from src.core.models import SiteSettings

PRIVACY_REVISION = '19 листопада 2026'
_STUB_MARKERS = (
    'Тимчасовий текст',
    '[дата]',
    '[Email]',
    '[Телефон]',
    '[Адреса офісу]',
)


def _contacts(contacts=None) -> dict[str, str]:
    if contacts:
        return contacts
    return resolve_public_contacts(SiteSettings.load())


def privacy_body_is_stub(body: str | None) -> bool:
    text = body or ''
    if not text.strip():
        return True
    return any(marker in text for marker in _STUB_MARKERS)


def fill_privacy_placeholders(body: str | None, contacts=None) -> str:
    text = body or ''
    data = _contacts(contacts)
    replacements = {
        '[Email]': data['email'],
        '[Телефон]': data['phone'],
        '[Адреса офісу]': data['address'],
    }
    for token, value in replacements.items():
        text = text.replace(token, escape(value))
    return text


def approved_privacy_body(contacts=None) -> str:
    data = _contacts(contacts)
    email = escape(data['email'])
    phone = escape(data['phone'])
    address = escape(data['address'])
    return (
        f'<p>Редакція від {PRIVACY_REVISION}.</p>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">01</span> Загальні положення</h2>'
        '<p>Ця Політика пояснює, як ТОВ «ВАРТІС ІНТЕЛІДЖЕНС» збирає, використовує та '
        'захищає персональні дані відвідувачів сайту. Надсилаючи форму на сайті, ви '
        'погоджуєтеся з умовами цієї Політики.</p></div>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">02</span> Які дані ми збираємо</h2>'
        '<p>Імʼя, номер телефону, адресу електронної пошти та текст повідомлення, які ви '
        'самостійно вказуєте у формі заявки. Також технічні дані: IP-адреса, тип браузера, '
        'сторінки, які ви переглядали.</p></div>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">03</span> Мета обробки</h2>'
        '<p>Дані використовуються лише для того, щоб звʼязатися з вами щодо вашого звернення, '
        'підготувати пропозицію та покращувати роботу сайту.</p></div>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">04</span> Передача третім особам</h2>'
        '<p>Ми не продаємо і не передаємо ваші дані третім особам, крім випадків, передбачених '
        'законодавством України, та сервісів, що забезпечують роботу сайту '
        '(хостинг, CRM, аналітика).</p></div>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">05</span> Зберігання та захист</h2>'
        '<p>Дані зберігаються не довше, ніж це потрібно для мети обробки. Ми застосовуємо '
        'організаційні та технічні заходи захисту, зокрема захищене зʼєднання (SSL).</p></div>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">06</span> Ваші права</h2>'
        '<p>Ви маєте право дізнатися, які дані про вас зберігаються, вимагати їх виправлення '
        'або видалення, а також відкликати згоду на обробку, написавши нам.</p></div>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">07</span> Файли cookie</h2>'
        '<p>Сайт використовує файли cookie для аналітики (Google Analytics 4). Ви можете '
        'прийняти їх у банері на сайті або вимкнути cookie в налаштуваннях браузера.</p></div>'
        '<div class="privacy-block">'
        '<h2><span class="privacy-block__num">08</span> Контакти</h2>'
        f'<p>З питань обробки персональних даних звертайтеся: {email}, {phone}, '
        f'{address}.</p></div>'
    )


def apply_approved_privacy(page, contacts=None) -> bool:
    if not privacy_body_is_stub(page.body):
        return False
    page.body = approved_privacy_body(contacts)
    page.save(update_fields=['body'])
    return True
