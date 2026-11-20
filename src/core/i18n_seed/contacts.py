"""Контакти та політика конфіденційності."""

from src.core.i18n_seed.fill import fill_en
from src.pages.models import ContactsPage, PrivacyPage

_PRIVACY = (
    '<p>Version of 19 November 2026.</p>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">01</span> General</h2>'
    '<p>This Policy explains how VARTIS INTELLIGENCE LLC collects, uses and protects the personal data '
    'of people who visit the site. By sending a form on the site, you agree to this Policy.</p></div>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">02</span> What we collect</h2>'
    '<p>The name, phone number, email address and message that you enter yourself in the request form. '
    'Also technical data: IP address, browser type and the pages you viewed.</p></div>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">03</span> Why we process it</h2>'
    '<p>The data is used only to contact you about your enquiry, to prepare a proposal and to improve the site.</p></div>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">04</span> Sharing with third parties</h2>'
    '<p>We do not sell or pass your data to third parties, except where the law of Ukraine requires it '
    'and except for services that run the site (hosting, CRM, analytics).</p></div>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">05</span> Storage and protection</h2>'
    '<p>Data is kept no longer than the purpose requires. We apply organisational and technical safeguards, '
    'including an encrypted connection (SSL).</p></div>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">06</span> Your rights</h2>'
    '<p>You may ask which data we hold about you, require it to be corrected or deleted, '
    'and withdraw consent to processing by writing to us.</p></div>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">07</span> Cookies</h2>'
    '<p>The site uses cookies for analytics (Google Analytics 4). You can accept them in the banner on the site '
    'or turn cookies off in your browser settings.</p></div>'
    '<div class="privacy-block"><h2><span class="privacy-block__num">08</span> Contacts</h2>'
    '<p>For questions about personal data: info@vartis.in.ua, +380 75 535 99 18, '
    '04070, Kyiv, Ihorivska Street, 11B (Ihorivskyi Business Center).</p></div>'
)


def seed_contacts() -> None:
    fill_en(
        ContactsPage.load(),
        seo_title='Contacts — leave a request | VARTIS INTELLIGENCE',
        seo_description=(
            'Contact Vartis Intelligence: a consultation on counterparty screening, '
            'strategic intelligence and corporate security. In confidence.'
        ),
        h1='Contacts',
        hero_title='Contacts',
        hero_text=(
            'A first consultation helps decide which solution fits you. '
            'The fact of your enquiry, the request itself and the results stay known only to you'
        ),
        cta_primary='Leave a request',
        cta_secondary='How to reach us',
        info_title='Let us discuss your task',
        phone_label='Phone',
        email_label='Email',
        facebook_label='Facebook',
        whatsapp_label='WhatsApp',
        signal_label='Signal',
        telegram_label='Telegram',
        phone_hint='Tap to call',
        email_hint='Opens your mail app',
        whatsapp_hint='Opens a chat on the phone number',
        signal_hint='Opens a chat on the phone number',
        telegram_hint='Opens the company chat',
        write_label='Write',
        office_label='Office address',
        office_note='We recommend holding the first conversation about information protection outside the premises in question.',
        office_cta='Leave a request',
    )
    fill_en(
        PrivacyPage.load(),
        seo_title='Privacy policy | VARTIS INTELLIGENCE',
        seo_description='How Vartis Intelligence processes and protects the personal data you leave on the site.',
        h1='Privacy policy',
        hero_title='Privacy policy',
        hero_text='How we process and protect the personal data you leave on the site',
        body=_PRIVACY,
    )
