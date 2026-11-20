"""Сторінка VI Analysis і її списки."""

from src.core.i18n_seed.fill import fill_en, fill_ordered
from src.pages.models import AnalysisPage

_PRICE = [
    {
        'title': 'Onboarding',
        'when': 'one-off',
        'period': 'one-off',
        'text': 'An initial check of the counterparties you name, identification of the real owners, grouping into business groups, and monitoring and recommendations tuned to your business.',
        'description': 'An initial check of the counterparties you name, identification of the real owners, grouping into business groups, and monitoring and recommendations tuned to your business.',
        'price': '____ UAH per counterparty',
        'price_note': '____ UAH per counterparty',
    },
    {
        'title': 'Subscription',
        'when': 'monthly',
        'period': 'monthly',
        'text': 'Monitoring of the selected counterparties, alerts on material events, checks of new counterparties within the plan limit, and specialist consultations.',
        'description': 'Monitoring of the selected counterparties, alerts on material events, checks of new counterparties within the plan limit, and specialist consultations.',
        'price': 'according to the chosen plan',
        'price_note': 'according to the chosen plan',
    },
    {
        'title': 'Extra checks',
        'when': 'as needed',
        'period': 'as needed',
        'text': 'If in a month you add more new counterparties than the plan allows, each check above the limit is billed separately.',
        'description': 'If in a month you add more new counterparties than the plan allows, each check above the limit is billed separately.',
        'price': '____ UAH per counterparty',
        'price_note': '____ UAH per counterparty',
    },
    {
        'title': 'Protected space',
        'when': 'option',
        'period': 'option',
        'text': 'Creating and maintaining a protected information space — only if you ordered it.',
        'description': 'Creating and maintaining a protected information space — only if you ordered it.',
        'price': '____ UAH one-off + ____ UAH/month',
        'price_note': '____ UAH one-off + ____ UAH/month',
    },
]

_TARIFF_LINES = [
    [
        {'label': 'Counterparties on monitoring', 'value': 'up to 50'},
        {'label': 'New checks per month', 'value': 'up to 5'},
        {'label': 'Client contacts', 'value': 'up to 2'},
        {'label': 'Alerts on material events', 'value': 'online'},
        {'label': 'Summary report on your counterparties', 'value': 'once a quarter'},
        {'label': 'A dedicated analyst', 'value': '—'},
    ],
    [
        {'label': 'Counterparties on monitoring', 'value': 'up to 200'},
        {'label': 'New checks per month', 'value': 'up to 20'},
        {'label': 'Client contacts', 'value': 'up to 5'},
        {'label': 'Alerts on material events', 'value': 'online'},
        {'label': 'Summary report on your counterparties', 'value': 'monthly'},
        {'label': 'A dedicated analyst', 'value': '—'},
    ],
    [
        {'label': 'Counterparties on monitoring', 'value': 'up to 500'},
        {'label': 'New checks per month', 'value': 'up to 50'},
        {'label': 'Client contacts', 'value': 'up to 10'},
        {'label': 'Alerts on material events', 'value': 'online'},
        {'label': 'Summary report on your counterparties', 'value': 'monthly'},
        {'label': 'A dedicated analyst', 'value': '✓'},
    ],
]


def seed_analysis() -> None:
    page = AnalysisPage.load()
    fill_en(
        page,
        seo_title='VI Analysis — express counterparty screening by EDRPOU | VARTIS INTELLIGENCE',
        seo_description='An online counterparty check by name and EDRPOU code: a risk assessment and a recommendation on cooperation within minutes.',
        h1='VI Analysis',
        title='Express counterparty screening — VI Analysis',
        hero_title='VI Analysis',
        hero_text='Express counterparty screening, information gathering, risk assessment and recommendations for business',
        cta_primary='Order a check',
        cta_secondary='A retainer',
        steps_eyebrow='Our own service for a fast counterparty check',
        steps_title='Three steps from the company details to a decision',
        steps_leads=(
            'The company name and the EDRPOU code are enough. Within minutes you see which risks are attached '
            'to it and whether the deal is worth making — and on what terms.\n\n'
            'The service combines data collection, risk analysis and a conclusion in one process — '
            'without a manual search across dozens of registers.'
        ),
        risks_title='What VI Analysis checks',
        risks_lead='Risks are scored on three levels and three types. You immediately see both how serious the problem is and where it comes from.',
        risks_note_title='Inherited risks.',
        risks_note='If the company belongs to a business group, the report also takes into account the risks of related persons and companies.',
        recommendation_title='A recommendation on cooperation',
        recommendation_text=(
            'The recommendation module turns the risks it found into a specific course of action '
            'and shows which factors shaped it. You can accept or reject the recommendation — the decision stays yours.'
        ),
        rec_heading='Recommendations',
        rec_badge='Not recommended',
        rec_verdict='Decline to cooperate',
        rec_note='Other options do not apply — the “Not recommended” mode is in effect.',
        rec_flag='Signal: signs of a shell company',
        rec_accept='Accept',
        rec_reject='Reject',
        rec_date='Calculated: 04.08.2026',
        rec_caption='A sample recommendation in the system',
        result_title='What the client receives',
        result_text=(
            'From the risks it found, the recommendation module proposes how to cooperate: on standard terms, '
            'with extra conditions and controls, or with a recommendation to walk away. '
            'The client receives a risk assessment and recommendations for the decision.'
        ),
        result_method_prefix=(
            'The methodology is set out in the founders’ article by V. V. Abroskin and S. V. Tikhonov, '
            '“A digital ecosystem for counterparty screening…” (Law and Society, No. 1/2026, '
        ),
        result_method_suffix=').',
        result_doi_label='doi.org/10.32842/2078-3736/2026.1.1.28',
        paket_eyebrow='For companies that need continuous control of their partner base',
        paket_title='A retainer for regular clients',
        paket_subtitle='for regular clients',
        paket_lead=(
            'You run the business — we help you make sure your partners are reliable. '
            'You name the counterparties to check, and we do it professionally: from the first check to continuous monitoring of changes.'
        ),
        paket_text=(
            'You run the business — we help you make sure your partners are reliable. '
            'You name the counterparties to check, and we do it professionally: from the first check to continuous monitoring of changes.'
        ),
        include_title='What the package includes',
        include_lead='Every counterparty you name for a check goes through the full cycle and stays under watch for the term of the contract.',
        include_option_eyebrow='An optional add-on',
        include_option_title='A protected information space',
        include_option_text=(
            'The package can include a protected information space — a separate closed environment '
            'where check results are stored and your contacts exchange information with our specialists.'
        ),
        why_title='Why it pays off',
        price_title='What it costs',
        price_lead='The fee has four clear parts. You know in advance what you are paying for and can plan the budget.',
        tariffs_title='Subscription plans',
        price_note='More than 500 counterparties, or special requirements? We will prepare an individual proposal.',
        order_title='Order\na check',
        order_text=(
            'Describe the situation and we will contact you to clarify the task and propose a way of working. '
            'The fact of your enquiry stays confidential.'
        ),
        related_title='Related services',
        short='Information gathering, risks, recommendations',
        card_text='Express counterparty screening, information gathering, risk assessment and recommendations for business',
        tags='Information gathering|Risk assessment|Recommendations',
    )
    fill_ordered(page.steps.all(), [
        {
            'title': 'Information gathering',
            'text': 'The system immediately researches the counterparty by name and EDRPOU code and brings data from different sources together.',
            'bullets': 'identifies the real owners and organisers of the business\nhelps group companies by the business group they belong to',
        },
        {
            'title': 'Risk assessment',
            'text': 'Every fact that is found is checked for risk and given a severity level.',
            'bullets': 'categories: low, medium, high\nrisks inherited from the business group are shown separately — problems of related companies are not left out',
        },
        {
            'title': 'Recommendation',
            'text': 'From the risks it found, the system forms a view on whether cooperation makes sense and proposes the terms.',
            'bullets': 'a clear summary instead of raw data\nthe recommendation module can be tuned to the specifics of the business',
        },
    ])
    fill_ordered(page.risks.all(), [
        {'tag': 'Relations with the authorities', 'title': 'Legal and regulatory risks', 'text': 'Information on criminal proceedings, sanctions and enforcement proceedings.'},
        {'tag': 'Financial and commercial activity', 'title': 'Financial and commercial risks', 'text': 'Debt, whether the financial statements match the financial rules built into the system, signs of possible involvement in illicit goods, and other risk signals in the activity.'},
        {'tag': 'Other sources', 'title': 'Reputational and other risks', 'text': 'Media coverage, information from open sources and further signals that need to be checked.'},
    ])
    fill_ordered(page.risk_levels.all(), [
        {'level': 'High', 'meaning': 'Material red flags; cooperation is limited', 'action': 'Limit cooperation'},
        {'level': 'Medium', 'meaning': 'A deeper check is required', 'action': 'A deeper check'},
        {'level': 'Low', 'meaning': 'Minimal caveats', 'action': 'Standard monitoring'},
    ])
    fill_ordered(page.recs.all(), [
        {'title': 'Recommended', 'text': 'cooperation on standard terms'},
        {'title': 'With caution', 'text': 'cooperation with extra conditions and control'},
        {'title': 'Not recommended', 'text': 'the risks outweigh the benefit of the deal'},
    ])
    fill_ordered(page.paket_steps.all(), [
        {'title': 'You decide', 'text': 'You choose whom to check: key partners, new counterparties or individual companies. The name and the EDRPOU code are enough.'},
        {'title': 'We check', 'text': 'Each counterparty you select is checked in VI Analysis: risks, owners, business groups, a recommendation.'},
        {'title': 'We watch for changes', 'text': 'The selected counterparties stay on monitoring of the state registers. You add new ones when you need to — we check them quickly.'},
        {'title': 'We tell you in time', 'text': 'Your contacts learn about material changes online — from our specialists, not from the news.'},
    ])
    fill_ordered(page.includes.all(), [
        {'title': 'Integrity and relations with the authorities', 'text': 'We check for criminal and enforcement proceedings, sanctions and other red flags.'},
        {'title': 'Financial position and the history of links', 'text': 'We look at debts, the financial statements and who the company is linked to now and was linked to before.'},
        {'title': 'Obvious and hidden risks', 'text': 'We show not only the obvious problems, but the risks the company inherits from related persons and companies.'},
        {'title': 'The real owners and business groups', 'text': 'We establish who actually stands behind the company and group your counterparties into formal and de facto business groups.'},
        {'title': 'Recommendations on cooperation', 'text': 'For each counterparty, a clear conclusion at the time of the check: work on standard terms, with extra conditions and control, or walk away.'},
        {'title': 'Continuous register monitoring', 'text': 'We track changes in the state registers and tell you about material events: a new owner or director, new proceedings, signs of trouble.'},
    ])
    fill_ordered(page.why_items.all(), [
        {'title': 'Confidentiality — from the first step', 'text': 'We sign a non-disclosure agreement before the main contract — before you have named a single company. It stays in force for as long as the main contract does.'},
        {'title': 'No in-house screening team', 'text': 'You do not need to hire, train and keep integrity-screening specialists, or buy access to databases and registers. We carry those costs — you pay only for the result.'},
        {'title': 'An answer in minutes, not hours', 'text': 'Checks run in our VI Analysis fast-screening service: it brings data from different sources together, scores the risks and forms a recommendation.'},
        {'title': 'Your people on a direct line', 'text': 'When the contract is signed you name the contacts. They receive information from our specialists online — without intermediaries or extra internal correspondence.'},
    ])
    fill_ordered(page.price_parts.all(), _PRICE)
    fill_ordered(page.price_rows.all(), _PRICE)
    fill_ordered(page.tariffs.all(), [
        {'name': 'Start', 'subtitle': 'small business', 'price': '____ UAH', 'period': 'per month'},
        {'name': 'Business', 'subtitle': 'the most popular', 'price': '____ UAH', 'period': 'per month'},
        {'name': 'Corporate', 'subtitle': 'large companies and groups', 'price': '____ UAH', 'period': 'per month'},
    ])
    for tariff, lines in zip(page.tariffs.order_by('order', 'id'), _TARIFF_LINES):
        fill_ordered(tariff.lines.all(), lines)
    fill_ordered(page.pay_terms.all(), [
        {'title': 'Transparent.', 'text': 'You pay only for the components named in the contract. No hidden fees and no “urgency” surcharges.'},
        {'title': 'Monthly prepayment.', 'text': 'The subscription is paid at the start of the month; extra checks are billed in arrears, with the next invoice.'},
        {'title': 'A discount for a longer engagement.', 'text': 'Pay 6 months ahead — a discount of ___ %. Pay 12 months ahead — ___ %.'},
        {'title': 'Flexibility.', 'text': 'The plan can change from the next month if the number of counterparties under review has changed.'},
    ])
