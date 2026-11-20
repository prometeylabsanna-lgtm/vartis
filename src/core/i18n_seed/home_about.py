"""Головна та «Про компанію»."""

from src.core.i18n_seed.fill import fill_en, fill_ordered
from src.pages.models import (
    AboutPage,
    AboutPrinciple,
    AboutProcessStep,
    AboutStat,
    HomeAdvantage,
    HomeDirection,
    HomePage,
    HomeProcessStep,
    TeamMember,
)


def seed_home() -> None:
    page = HomePage.load()
    fill_en(
        page,
        seo_title='Counterparty screening and strategic intelligence | VARTIS INTELLIGENCE',
        seo_description=(
            'Counterparty screening, OSINT and strategic intelligence for business. '
            'We uncover hidden risks and help you make grounded decisions.'
        ),
        h1='Information that turns\nrisks into advantages',
        hero_title='Information that turns\nrisks into advantages',
        hero_text=(
            'Strategic intelligence, counterparty screening and business protection.\n'
            'We help you uncover hidden risks, verify information and make grounded decisions'
        ),
        hero_cta='Discuss a task',
        services_title='What we do',
        services_lead=(
            'End-to-end solutions for business — from verifying information '
            'to strategic analysis and risk management'
        ),
        advantages_title='Why clients work with us',
        advantages_lead='Information. Analysis. Security. Result.',
        mission_title='Strategic information\nfor confident decisions',
        mission_text=(
            'VARTIS INTELLIGENCE works at the intersection of strategic intelligence, OSINT, '
            'corporate security and risk analysis.\n\n'
            'We help businesses obtain and verify information, assess the circumstances '
            'and see the risks that can affect a decision'
        ),
        process_title='How we work',
        process_lead='From the request to a grounded decision',
        blog_title='Analysis and expert notes',
        blog_lead=(
            'Publications on counterparty screening, strategic intelligence, '
            'corporate security and risk management'
        ),
        blog_all_label='All articles →',
    )
    fill_ordered(page.advantages.all(), [
        {'title': 'Analytical approach', 'text': 'Decisions based on verified information'},
        {'title': 'Risk assessment', 'text': 'Spotting potential threats before an important decision'},
        {'title': 'Confidentiality', 'text': 'Protection of the information and of the fact of your enquiry'},
        {'title': 'Expert support', 'text': 'Professional analysis and a clear explanation of the findings'},
    ])
    fill_ordered(page.process_steps.all(), [
        {'title': 'We study the task', 'text': 'We clarify what information is needed and which questions must be answered'},
        {'title': 'We research', 'text': 'We collect, verify and analyse information against the agreed brief'},
        {'title': 'We form conclusions', 'text': 'We organise the results and separate established facts from possible risks'},
        {'title': 'We deliver the result', 'text': 'We provide the materials needed for further analysis and a decision'},
    ])
    fill_ordered(HomeDirection.objects.filter(page=page), [
        {
            'title': 'Express counterparty screening — VI Analysis',
            'text': 'Express counterparty screening, information gathering, risk assessment and recommendations for business',
        },
        {
            'title': 'Business support',
            'text': 'Solutions that protect the company’s interests, reveal threats and keep control of important information',
        },
        {
            'title': 'Consulting',
            'text': 'Expert support in analysing a situation, assessing risk and preparing an important decision',
        },
        {
            'title': 'Deep analytics',
            'text': 'Strategic intelligence: verified information on people, companies and markets — for decisions where a mistake is expensive',
        },
    ])


def seed_about() -> None:
    page = AboutPage.load()
    fill_en(
        page,
        seo_title='About the company — OSINT and corporate security | VARTIS INTELLIGENCE',
        seo_description=(
            'Vartis Intelligence: the team, principles and method behind strategic intelligence, '
            'counterparty screening and business protection.'
        ),
        h1='About the company',
        hero_title='About the company',
        hero_text='We help businesses decide on the basis of verified facts',
        hero_cta='Discuss a task',
        hero_cta_secondary='Our team',
        intro_title='Intelligence and security for your business',
        intro_text=(
            'We help businesses decide on the basis of verified facts. We research companies and people, '
            'business groups and corporate structures, the history of their relationships and hidden links. '
            'You receive a clear picture of the risks and practical recommendations on whether to proceed.\n\n'
            'We offer both fast answers from our own IT service and deep individual studies, '
            'the scope of which we define together with the client.'
        ),
        principles_title='Our principles',
        team_title='Founders',
        team_lead=(
            'We combine practical experience in law enforcement with a research approach to information analysis'
        ),
        expertise_label='Core expertise',
        career_label='Career path',
        science_eyebrow='Research basis',
        science_title='The VI Analysis service',
        science_text=(
            'The methodology of the express counterparty-screening service is set out in the founders’ article '
            'by V. V. Abroskin and S. V. Tikhonov, “A digital ecosystem for counterparty screening…” '
            '(Law and Society, No. 1/2026).'
        ),
        science_doi_label='doi.org/10.32842/2078-3736/2026.1.1.28',
        partners_eyebrow='International work',
        partners_title='For business with interests outside Ukraine',
        partners_text=(
            'Business interests do not stop at a border, and neither does our work. '
            'Vartis Intelligence partners with specialist firms that search for and analyse information '
            'for individuals and companies. They work only in ways permitted by the national law of EU member states.'
        ),
        stats_title='Key figures',
        process_title='How we work',
    )
    fill_ordered(AboutPrinciple.objects.filter(page=page), [
        {'title': 'Legality', 'text': 'We obtain data only lawfully — from open sources, state registers and other resources the law allows.'},
        {'title': 'Confidentiality', 'text': 'The fact of your enquiry, the request itself and the results stay known only to you.'},
        {'title': 'Expertise', 'text': 'We combine practical law-enforcement experience with a research approach to information analysis.'},
        {'title': 'A practical result', 'text': 'We do not only collect facts. We explain what they mean for your business and give specific recommendations.'},
    ])
    fill_ordered(AboutStat.objects.filter(page=page), [
        {'label': 'years of the founders’ experience'},
        {'label': 'years each founder spent in law enforcement'},
        {'label': 'checks carried out'},
        {'label': 'lines of work — from counterparty screening to international assignments'},
        {'label': 'clients'},
        {'label': 'a partner network of specialist firms in EU member states'},
        {'label': 'projects delivered'},
    ])
    fill_ordered(AboutProcessStep.objects.filter(page=page), [
        {'title': 'Request', 'text': 'You describe the task — in full confidentiality.'},
        {'title': 'Scope', 'text': 'Together we agree what must be established, by when, and in what form.'},
        {'title': 'Research', 'text': 'We collect and analyse information using only lawful methods.'},
        {'title': 'Conclusion', 'text': 'You receive a structured report with the risks we found and our recommendations.'},
        {'title': 'Support', 'text': 'If needed, we explain the results, answer questions and continue monitoring.'},
    ])
    members = list(TeamMember.objects.filter(page=page).order_by('order', 'id'))
    if len(members) >= 1:
        fill_en(
            members[0],
            name='Viacheslav Abroskin',
            role='Co-founder and director of VARTIS INTELLIGENCE LLC',
            regalia='PhD in Law · Attorney, partner at FOMIN PARTNERS · Police General of the 2nd rank, retired',
            bio=(
                'More than 25 years in law enforcement, and also in public administration, military service, '
                'legal practice, criminal analysis and corporate security. He served as First Deputy Head of '
                'the National Police of Ukraine — head of the criminal police — and initiated the creation of '
                'criminal-analysis units.'
            ),
            expertise=[
                'Criminal analysis and working with information',
                'Countering organised crime and detective work',
                'Corporate security and security-risk assessment',
                'Corporate law, protection of business interests and legal-risk management',
                'Public safety in a crisis',
            ],
            career_path=[
                {'t': 'Co-founder and director of VARTIS INTELLIGENCE LLC', 'y': 'Now'},
                {'t': 'Attorney, partner at FOMIN PARTNERS', 'y': 'Now'},
                {'t': 'Armed Forces of Ukraine, lieutenant colonel', 'y': '2022–2024'},
                {'t': 'Rector of Odesa State University of Internal Affairs', 'y': '2019–2021'},
                {'t': 'First Deputy Head of the National Police of Ukraine — head of the criminal police', 'y': '2017–2019'},
                {'t': 'Head of the National Police Directorate in Donetsk region', 'y': '2014–2017'},
                {'t': 'Criminal investigation units of the internal-affairs bodies', 'y': 'Since 1994'},
            ],
        )
    if len(members) >= 2:
        fill_en(
            members[1],
            name='Serhii Tikhonov',
            role='Co-founder of VARTIS INTELLIGENCE LLC',
            regalia='Doctor of Philosophy in Law · Police General of the 3rd rank, retired',
            bio=(
                'More than 25 years in law enforcement — from a field officer to the head of a central '
                'criminal-investigation unit at national level. Former head of the Department of Detective '
                'and Search Activity at the National Academy of Internal Affairs.'
            ),
            expertise=[
                'Searching for, verifying and analysing information',
                'Detective work and criminal investigation',
                'Forensics',
                'Legal regulation and reform of law enforcement',
                'Methodological support for practical work',
            ],
            career_path=[
                {'t': 'Co-founder of VARTIS INTELLIGENCE LLC', 'y': 'Now'},
                {'t': 'Head of the Department of Detective and Search Activity, National Academy of Internal Affairs', 'y': ''},
                {'t': 'Head of a central criminal-investigation unit', 'y': ''},
                {'t': 'Criminal investigation units', 'y': ''},
            ],
        )
