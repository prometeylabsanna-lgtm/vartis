"""Каталог послуг і чотири сторінки послуг. Глибока аналітика — окремо."""

from src.core.i18n_seed.fill import fill_en, fill_ordered
from src.core.i18n_urls import SERVICE_SLUG_EN
from src.pages.models import ServicePage, ServicesIndex

_ORDER = (
    'Describe the situation and we will contact you to clarify the task '
    'and propose a way of working. The fact of your enquiry stays confidential.'
)

_PAGES = {
    'konsaltynh': {
        'seo_title': 'Consulting on risk and decisions | VARTIS INTELLIGENCE',
        'seo_description': 'Expert consulting: situation analysis, risk assessment and preparation for important business decisions based on verified facts.',
        'h1': 'Consulting',
        'title': 'Consulting',
        'short': 'Expert support for important decisions',
        'hero_text': 'Expert support for business in analysing a situation, assessing risk and preparing an important decision',
        'cta_primary': 'Request a consultation',
        'cta_secondary': 'How we work',
        'scope_title': 'What consulting includes',
        'method_title': 'Method',
        'method_lead': 'From the request to a grounded decision',
        'method_step_prefix': 'Step',
        'advantages_title': 'What the client gains',
        'advantages_lead': 'What you get when you work with us',
        'order_title': 'Request\na consultation',
        'order_text': _ORDER,
        'related_title': 'Related services',
        'card_text': 'Expert support for business in analysing a situation, assessing risk and preparing an important decision',
        'tags': 'Situation analysis|Risk assessment|Decision preparation',
        'paragraphs': [
            'We help owners and executives understand a complex situation before a decision is made. We analyse the circumstances, assess the risks and prepare grounded recommendations on what to do next.',
            'Every enquiry is handled individually and in confidence — taking into account the company, the industry and the task.',
        ],
        'items': [
            'Analysis of the business situation and the circumstances',
            'Risk assessment before a deal or a decision',
            'Preparation for negotiations and reviews',
            'Analysis of how events may develop',
            'Recommendations on the next steps',
        ],
        'steps': [
            {'title': 'Briefing', 'text': 'We discuss the situation, the goals and the questions that need an answer'},
            {'title': 'Review of the circumstances', 'text': 'We study the information already available, the parties and the context'},
            {'title': 'Scenario assessment', 'text': 'We identify possible risks, consequences and courses of action'},
            {'title': 'Recommendations', 'text': 'We deliver the conclusions and stay with you while the decision is made'},
        ],
        'advantages': [
            {'title': 'Confidentiality', 'text': 'Protection of the information and of the fact of your enquiry'},
            {'title': 'An independent view', 'text': 'An assessment without a conflict of interest'},
            {'title': 'Grounded conclusions', 'text': 'Recommendations based on verified information'},
            {'title': 'Support', 'text': 'Professional support at every stage'},
        ],
    },
    'kompleksna-dopomoha-biznesu': {
        'seo_title': 'Business support and protection of interests | VARTIS INTELLIGENCE',
        'seo_description': 'Protection of the company’s interests: revealing threats, control of critical information and support for risky decisions.',
        'h1': 'Business support',
        'title': 'Business support',
        'short': 'Protection of interests and control of information',
        'hero_text': 'Solutions that protect the company’s interests, reveal threats and keep control of important information',
        'cta_primary': 'Get support',
        'cta_secondary': 'How we work',
        'scope_title': 'What business support includes',
        'scope_feature_title': 'One team that sees the whole situation and helps you act in sequence',
        'scope_feature_text': 'Every enquiry is handled individually and in confidence',
        'method_title': 'Method',
        'method_lead': 'Four stages from the audit to ongoing control',
        'method_step_prefix': 'Step',
        'advantages_title': 'What the client gains',
        'advantages_lead': '',
        'order_title': 'Get\nsupport',
        'order_text': _ORDER,
        'related_title': 'Related services',
        'card_text': 'Solutions that protect the company’s interests, reveal threats and keep control of important information',
        'tags': 'Protection of interests|Threat detection|Monitoring',
        'paragraphs': [
            'We combine analysis, information checks and corporate security in one way of working',
        ],
        'items': [
            'Revealing threats to the company’s interests',
            'Protection of commercially important information',
            'Checks of partners, counterparties and staff',
            'Support in a conflict or a crisis',
            'Regular risk monitoring',
        ],
        'steps': [
            {'title': 'Situation audit', 'text': 'We identify weak points, risks and the company’s priorities'},
            {'title': 'Action plan', 'text': 'We agree the measures, the timing and how we will work together'},
            {'title': 'Delivery', 'text': 'We carry out the checks, the analysis and the information-protection measures'},
            {'title': 'Control', 'text': 'We track changes in the circumstances and update the risk assessment'},
        ],
        'advantages': [
            {'title': 'Confidentiality', 'text': 'Protection of the information and of the fact of your enquiry'},
            {'title': 'Combined protection', 'text': 'Analysis, checks and security in one approach'},
            {'title': 'The full picture', 'text': 'We see risks across every line of the business'},
            {'title': 'A standing line', 'text': 'A fast response when the circumstances change'},
        ],
    },
    'zakhyst-vid-vytoku': {
        'seo_title': 'Protection against information leaks | VARTIS INTELLIGENCE',
        'seo_description': 'Premises surveys, a programme to protect confidential information, implementation control and scheduled inspections.',
        'h1': 'Protection against information leaks',
        'title': 'Protection against information leaks',
        'short': 'Protected rooms and negotiations',
        'hero_text': 'Your conversations, decisions and agreements should stay only with the people they are meant for.',
        'cta_primary': 'A confidential consultation',
        'cta_secondary': 'How we work',
        'scope_title': 'When this is needed',
        'method_title': 'How we work',
        'method_lead': 'Seven steps — from the first conversation to scheduled surveys',
        'method_step_prefix': 'Step',
        'advantages_title': 'Why clients choose us',
        'advantages_lead': 'Expertise, control and confidentiality at every stage',
        'order_title': 'A confidential\nconsultation',
        'order_text': _ORDER,
        'related_title': 'Related services',
        'card_text': 'Premises surveys, a protection programme, implementation control and scheduled inspections',
        'tags': 'Survey|Protection programme|Scheduled inspections',
        'paragraphs': [
            'Valuable information rarely disappears in a sophisticated attack. Far more often it leaves the executive’s office or the meeting room unnoticed — and becomes known to competitors, counterparties or other interested parties before you have made the decision.',
            'Everything about working with us is protected from the first contact — including the fact that you contacted us.',
        ],
        'items': [
            'The terms of your deals, prices or negotiating positions become known to the other side too quickly',
            'You have important negotiations, a deal, a reorganisation or a change of owners ahead',
            'The premises were recently renovated, you moved, or outside contractors worked there',
            'You received gifts or interior items from people who have an interest in your information',
            'You simply want to be sure that, inside your walls, only the people you invited can hear you',
        ],
        'steps': [
            {'title': 'A confidential consultation', 'text': 'You describe the situation and what protection you want. We recommend holding the first conversation outside the premises in question — in person or over a protected channel.'},
            {'title': 'A non-disclosure agreement', 'text': 'After we review the request we sign an NDA. It protects not only the information we will obtain, but the fact that you approached us.'},
            {'title': 'Survey and an expert opinion', 'text': 'A full survey of the site and the rooms. You receive an expert opinion listing the weaknesses we found and the risk assessment.'},
            {'title': 'A protection programme', 'text': 'We set the technical requirements for the protective measures, where they should sit, and the rules for staff and visitors. We recommend vetted suppliers and deal with them for you.'},
            {'title': 'Implementation control', 'text': 'We check that the measures meet the technical requirements and are placed and configured correctly. When the work is finished we run a control survey.'},
            {'title': 'Documentation', 'text': 'We prepare and hand over a passport of the protected room, so protection works as a system and does not depend on individual people.'},
            {'title': 'Scheduled surveys', 'text': 'We agree regular control surveys on a set schedule, and we run extra checks before important events.'},
        ],
        'advantages': [
            {'title': 'Expertise', 'text': 'We recommend only what your site actually needs, and only vetted suppliers.'},
            {'title': 'Control of the result', 'text': 'We check that every measure was implemented as required, and only then confirm that the room is ready.'},
            {'title': 'Scheduled surveys', 'text': 'Protection that does not fade over time — on an agreed schedule.'},
            {'title': 'Full confidentiality', 'text': 'The NDA is signed before any details are discussed.'},
        ],
    },
    'kryminalni-provadzhennia': {
        'seo_title': 'Information support in criminal proceedings | VARTIS INTELLIGENCE',
        'seo_description': 'Fact-checking, alternative explanations and an assessment of evidence for defence lawyers and law firms.',
        'h1': 'Information support in criminal proceedings',
        'title': 'Information support in criminal proceedings',
        'short': 'For defence lawyers and law firms',
        'hero_text': 'We help defence lawyers and victims’ representatives check facts, find alternative explanations and assess evidence — so the position in the case rests on verified information, not on assumptions.',
        'cta_primary': 'Discuss the request in confidence',
        'cta_secondary': 'How we work',
        'scope_title': 'Who we help',
        'method_title': 'From the first contact to the result',
        'method_lead': '5 steps',
        'method_step_prefix': 'Step',
        'advantages_title': 'Three lines of support',
        'advantages_lead': 'The questions that often decide the outcome of a case',
        'order_title': 'Let us discuss your\ncase in confidence',
        'order_text': _ORDER,
        'related_title': 'Related services',
        'card_text': 'Fact-checking, alternative explanations and an assessment of evidence for defence lawyers and law firms',
        'tags': 'Fact-checking|Alternative explanations|Evidence assessment',
        'paragraphs': [
            'We work with lawyers, not instead of them. Our client is a professional who is running the case and needs reliable information and analysis behind it.',
            'We do not replace defence counsel and we do not provide legal assistance in the case — the strategy and the procedural decisions belong to the lawyer. We work only with lawful sources and within the law of Ukraine.',
        ],
        'items': [
            'Law firms — we strengthen the defence team in complex, multi-episode proceedings',
            'Legal practices — we support criminal-law teams, including cases involving business and public officials',
            'Advocates — analytical support for counsel to individuals and companies, and for victims’ representatives',
        ],
        'steps': [
            {'title': 'We sign an NDA', 'text': 'You contact us and we send a non-disclosure agreement. Only after it is signed do we move to the substance.'},
            {'title': 'We learn the request', 'text': 'You describe the task and pass the materials we need. We assess how and to what extent we can help. This stage is free of charge.'},
            {'title': 'We fix the scope in a contract', 'text': 'The questions, the volume of work, the timing, the form of the result and the fee. Anything outside those limits needs a separate agreement.'},
            {'title': 'We do the work', 'text': 'We stay within the agreed limits and keep you informed. We discuss interim results so you can adjust the position in time.'},
            {'title': 'We deliver the result', 'text': 'You receive the result in the agreed form — clear, structured and ready to use in the work on the case.'},
        ],
        'advantages': [
            {'title': 'Fact-checking', 'text': 'We check whether the events, circumstances and data cited in the proceedings actually took place.'},
            {'title': 'Alternative versions', 'text': 'We look for other possible explanations of the facts the defence intends to challenge.'},
            {'title': 'Evidence assessment', 'text': 'A view on the admissibility and reliability of information obtained through measures that temporarily restrict a person’s rights.'},
        ],
    },
}


def seed_services() -> None:
    fill_en(
        ServicesIndex.load(),
        seo_title='Services: counterparty screening, intelligence, security | VARTIS INTELLIGENCE',
        seo_description=(
            'The service catalogue: VI Analysis express screening, deep analytics, consulting, '
            'information-leak protection and support in criminal proceedings.'
        ),
        h1='Services',
        hero_title='Services',
        hero_text='End-to-end solutions for business — from verifying information to strategic analysis and risk management',
        cta_primary='Leave a request',
        cta_secondary='All directions',
        card_more_label='Learn more',
    )
    for slug, copy in _PAGES.items():
        page = ServicePage.objects.filter(slug=slug).first()
        if page is None:
            continue
        if not page.slug_en:
            page.slug_en = SERVICE_SLUG_EN[slug]
            page.save(update_fields=['slug_en'])
        paragraphs = copy['paragraphs']
        items = copy['items']
        steps = copy['steps']
        advantages = copy['advantages']
        scalars = {
            key: value for key, value in copy.items()
            if key not in ('paragraphs', 'items', 'steps', 'advantages')
        }
        fill_en(page, **scalars)
        fill_ordered(page.scope_paragraphs.all(), [{'text': text} for text in paragraphs])
        fill_ordered(page.scope_items.all(), [{'text': text} for text in items])
        fill_ordered(page.method_steps.all(), steps)
        fill_ordered(page.advantages.all(), advantages)
