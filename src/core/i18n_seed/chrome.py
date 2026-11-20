"""Шапка, футер, інтерфейс, заявка, блог і 404."""

from src.blog.models import BlogPage
from src.core.i18n_seed.fill import fill_en
from src.core.models import SiteSettings
from src.core.models_interface import InterfaceCopy
from src.leads.models import LeadModal


def seed_chrome() -> None:
    fill_en(
        SiteSettings.load(),
        company_name='VARTIS INTELLIGENCE LLC',
        tagline='Strategic intelligence, OSINT, corporate security and risk analysis',
        address='04070, Kyiv, Ihorivska Street, 11B (Ihorivskyi Business Center)',
        default_seo_title='Counterparty screening and strategic intelligence | VARTIS INTELLIGENCE',
        default_seo_description=(
            'Counterparty screening, OSINT and strategic intelligence for business. '
            'We uncover hidden risks and help you make grounded decisions.'
        ),
        footer_cta_title='Leave a request',
        footer_cta_text=(
            'Describe the situation and we will contact you to clarify the task. '
            'The fact of your enquiry stays confidential.'
        ),
        nav_about='About',
        nav_services='Services',
        nav_cases='Cases',
        nav_blog='Blog',
        nav_contacts='Contacts',
        header_cta='Leave a request',
        mobile_lead='Strategic intelligence, counterparty screening and business protection',
        mobile_cta_secondary='Discuss a task',
        footer_col_company='Company',
        footer_col_services='Services',
        footer_phone_label='Tel',
        footer_email_label='Email',
        footer_address_label='Address',
        footer_whatsapp_label='WhatsApp',
        footer_signal_label='Signal',
        footer_telegram_label='Telegram',
        footer_write_label='Write',
        privacy_link_label='Privacy policy',
    )
    fill_en(
        InterfaceCopy.load(),
        lang_switch_aria='Language',
        cookie_title='Cookies',
        cookie_body=(
            'We use cookies for visit analytics and to run the site. '
            'By clicking “Accept”, you agree to their use. Details are in the'
        ),
        cookie_more_label='Learn more',
        cookie_accept_label='Accept',
        cookie_settings_label='Cookie settings',
        cookie_again_label='Show the cookie banner again',
        developed_label='Built by',
        back_to_top='Top',
        back_to_top_aria='Back to top',
        crumb_home='Home',
        crumbs_aria='Breadcrumbs',
        logo_home_aria='VARTIS INTELLIGENCE — home',
        nav_main_aria='Main navigation',
        services_list_aria='Services list',
        menu_open_aria='Open menu',
        footer_nav_aria='Footer navigation',
        footer_services_aria='Footer services',
        mobile_nav_aria='Mobile navigation',
        photo_lightbox_aria='Photo view',
        photo_close_aria='Close',
        modal_close_aria='Close',
        form_aria='Request form',
        pagination_aria='Pages',
        feed_filter_aria='Topic filter',
        dir_prev_aria='Previous services',
        dir_next_aria='Next services',
        profile_services_aria='Related services',
        map_title='Office location map',
        article_section_aria='Article text',
        feed_section_aria='Article feed',
        catalog_aria='Service catalogue',
        privacy_section_aria='Privacy policy text',
        share_label='Share',
        copy_link_label='Copy link',
        copied_label='Copied',
        new_badge='New',
        cover_alt_prefix='Cover:',
        service_alt_prefix='Service illustration:',
        direction_alt_prefix='Direction photo:',
        err404_meta_title='Page not found — VARTIS INTELLIGENCE',
        err404_title='Page not found',
        err404_text=(
            'The address may have been typed incorrectly, or the page has moved. '
            'Return to the homepage or choose a section in the menu.'
        ),
        err404_primary='Back to homepage',
        err404_secondary='Our services',
    )
    fill_en(
        LeadModal.load(),
        title='Leave a request',
        lead=(
            'Describe the situation and we will contact you to clarify the task. '
            'The fact of your enquiry stays confidential.'
        ),
        name_label='Name',
        phone_label='Phone',
        email_label='Email',
        message_label='Briefly about the task',
        phone_placeholder='+380 XX XXX XX XX',
        email_placeholder='user@domain.com',
        message_placeholder='What should we look into?',
        consent_prefix='I agree to the processing of personal data under the',
        submit_label='Send request',
        thanks_title='Thank you for your request',
        thanks_text=(
            'We have received your enquiry and will contact you shortly. '
            'The fact of your enquiry stays confidential.'
        ),
        error_required='This field is required',
        error_name='The name may contain only letters, spaces, hyphens or apostrophes',
        error_phone='Enter a number as +380XXXXXXXXX or 0XXXXXXXXX',
        error_email='Enter a valid email address',
        error_message='The message must be no longer than 2000 characters',
        error_consent='Consent to data processing is required',
    )
    fill_en(
        BlogPage.load(),
        seo_title='Blog on counterparty screening and OSINT | VARTIS INTELLIGENCE',
        seo_description=(
            'Expert notes on counterparty screening, strategic intelligence, '
            'corporate security and risk management.'
        ),
        h1='Blog',
        hero_text=(
            'Analysis and expert notes on counterparty screening, strategic intelligence, '
            'corporate security and risk management'
        ),
        crumb='Blog',
        cta_primary='Leave a request',
        cta_secondary='To the articles',
        all_label='All',
        feed_title='All publications',
        empty_text='There are no publications in this topic yet.',
        read_label='Read the article',
        detail_cta='Discuss a task',
        detail_read='Read',
        help_title='Need help with a similar task?',
        help_cta='Discuss a task',
        related_title='Read also',
        all_articles_label='All articles →',
        read_minutes_template='{n} min read',
    )
