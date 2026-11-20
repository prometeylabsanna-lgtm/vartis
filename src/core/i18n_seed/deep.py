"""Глибока аналітика: послуга і панель DeepAnalytics."""

from src.core.i18n_seed.fill import fill_en, fill_ordered
from src.core.i18n_urls import SERVICE_SLUG_EN
from src.pages.models import DeepAnalytics, DeepSnippet, ServicePage
from src.pages.models_deep import DEEP_SLUG


def _snippets(page, kind, texts):
    rows = page.snippets.filter(kind=kind).order_by('order', 'id')
    fill_ordered(rows, [{'text': text} for text in texts])


def seed_deep() -> None:
    service = ServicePage.objects.filter(slug=DEEP_SLUG).first()
    if service is None:
        return
    if not service.slug_en:
        service.slug_en = SERVICE_SLUG_EN[DEEP_SLUG]
        service.save(update_fields=['slug_en'])
    fill_en(
        service,
        seo_title='Deep analytics and OSINT research | VARTIS INTELLIGENCE',
        seo_description=(
            'Strategic intelligence on people, companies and markets: facts kept separate from assumptions, '
            'payment in stages, a report with sources.'
        ),
        h1='Deep analytics',
        title='Deep analytics',
        short='Strategic intelligence for your task',
        hero_text=(
            'Strategic intelligence: verified information on people, companies and markets — '
            'for decisions where a mistake is expensive. You pay in stages and see the result at each one.'
        ),
        cta_primary='Discuss a task',
        cta_secondary='A sample report',
        related_title='Related services',
        card_text=(
            'Strategic intelligence: verified information on people, companies and markets — '
            'for decisions where a mistake is expensive'
        ),
        tags='Strategic intelligence|Facts kept separate from assumptions|Payment in stages',
        method_step_prefix='Step',
    )
    deep = DeepAnalytics.objects.filter(page=service).first()
    if deep is None:
        return
    fill_en(
        deep,
        h1='Deep analytics',
        hero_text=(
            'Strategic intelligence: verified information on people, companies and markets — '
            'for decisions where a mistake is expensive. You pay in stages and see the result at each one.'
        ),
        cta_primary='Discuss a task',
        cta_secondary='A sample report',
        strategy_eyebrow='Strategic intelligence',
        strategy_title='For decisions where a mistake is expensive',
        compare_express_eyebrow='Express check · VI Analysis',
        compare_express_title='A fast result for typical decisions',
        compare_express_text='Through our IT service: a company name and an EDRPOU code — risks and a recommendation within minutes.',
        compare_express_link='About VI Analysis →',
        compare_deep_eyebrow='Deep analytics',
        compare_deep_title='An individual strategic study',
        compare_deep_text='A detailed analysis of complex structures, business groups and links, the scope of which we agree with you.',
        nda_title='Protection from the first minute',
        nda_text=(
            'Before you tell us about the request, we sign a non-disclosure agreement. '
            'It covers every piece of information you pass to us, and even the fact that you contacted us. '
            'The person or company we research learns neither about the check nor about you.'
        ),
        nda_note='You can read the agreement in advance — before any commitment.',
        get_title='You know in advance what you will receive',
        get_lead=(
            'The result will not be a surprise. We agree the contents of the report before the work starts, '
            'and we show a draft before the final meeting.'
        ),
        example_title='What it looks like: an example from our work',
        example_lead=(
            'A study of trade in illicit goods in Ukraine. The client wanted to understand where and how '
            'counterfeit and smuggled goods of a defined segment are sold, which brands are counterfeited most often '
            'and where the goods reach the shops from. Below are anonymised fragments of the report.'
        ),
        ex_frag1='Fragment 1 · Executive overview — the numbers that matter',
        ex_frag3='Fragment 3 · Facts kept separate from assumptions',
        ex_frag3_lead=(
            'To find out where the goods reach the shops from, we studied sales in messengers. '
            'In three different sales channels we found six identical signs. The report shows clearly '
            'what was established and what follows from it:'
        ),
        ex_frag4='Fragment 4 · Honest about the limits of the conclusions',
        ex_frag4_lead=(
            'We state plainly what the data cannot support, so you do not decide on a false basis. '
            'Examples from the report:'
        ),
        facts_title='Established facts',
        conclusion_title='Conclusion and degree of confidence',
        assumption_label='Assumption:',
        why_not_label='Why this is not a fact:',
        ex_assumption='the three channels most likely share organisers and a single source of the goods.',
        ex_why_not=(
            'there is no direct confirmation of a common owner — the conclusion rests on matching signs, '
            'so it is marked as an assumption.'
        ),
        pay_title='You pay in stages — and only for what you have already seen',
        pay_lead=(
            'You do not pay the whole amount up front. The fee is split into three parts, '
            'and before each next payment you see what has already been done.'
        ),
        paid_label='Paid:',
        before_pay_label='Before the next payment:',
        guarantee_title='Your guarantee',
        quality_title='Why deep analytics is worth the fee',
        faq_title='Answers to the doubts we hear',
        order_title='Describe your\ntask',
        order_text='We will reply whether we can help, how long it will take and what it will cost. It commits you to nothing.',
        related_title='Related services',
    )
    fill_ordered(deep.steps.all(), [
        {'title': 'You ask the question', 'text': 'who or what to research, what to establish, and by when'},
        {'title': 'We study the request', 'text': 'we assess what can be established and from which sources'},
        {'title': 'We agree the timing and the fee', 'text': 'we fix everything in a contract before the work starts'},
        {'title': 'You receive the report', 'text': 'with conclusions, sources and an assessment of those sources'},
    ])
    fill_ordered(deep.get_items.all(), [
        {'title': 'A short overview for the executive', 'text': 'Two or three pages: the main conclusions, the risk assessment and the recommendations. It can be read in ten minutes and a decision can be made.'},
        {'title': 'The full report', 'text': 'How the information was collected and checked, which assumptions were confirmed and which were not, a list of sources with a reliability score, and the conclusions.'},
        {'title': 'Working files and visuals', 'text': 'Data tables, charts, maps. If needed, alternative models of how events may develop (“what happens if…”).'},
        {'title': 'The final meeting', 'text': 'The analysts who ran the study present the results and answer your questions.'},
    ])
    fill_ordered(deep.pay_stages.all(), [
        {'when': 'at the start', 'stage': 'Stage 1', 'title': 'Agreeing the brief', 'text': 'We study the sources that are available. Together we draw up the questions and the assumptions to test, agree the assessment criteria and fix the brief.', 'see': 'an approved brief: which questions will be answered and which information cannot be obtained.'},
        {'when': 'after the interim results', 'stage': 'Stage 2', 'title': 'Interim results', 'text': 'About halfway through we hold an interim meeting: we show everything already found and agree the direction from there.', 'see': 'the interim results and an agreed plan through to the end of the work.'},
        {'when': 'after the report is accepted', 'stage': 'Stage 3', 'title': 'The final report', 'text': 'We hand over a fully checked report with annexes, hold the final meeting and transfer the right to use the results.', 'see': 'a finished report, which you check against the brief.'},
    ])
    fill_ordered(deep.quality_items.all(), [
        {'title': 'Checking in several stages', 'text': 'Information passes several levels of review, and every source receives a reliability score. Errors in the data do not reach the conclusions.'},
        {'title': 'Facts kept separate from assumptions', 'text': 'The report always shows what was established for certain and what is a reasoned assumption, and what it rests on.'},
        {'title': 'Acceptance against clear criteria', 'text': 'The contract records the acceptance criteria. You judge the result by clear measures, not by whether you like it.'},
        {'title': 'Full non-disclosure', 'text': 'We sign a non-disclosure agreement before you pass us any of your information.'},
    ])
    fill_ordered(deep.faqs.all(), [
        {'question': 'What if the result is not what we hoped for?', 'answer': 'The point of deep analytics is to show how things actually are, not to confirm what you hoped. If the study shows that your assumption is wrong, it saves you from putting money into a losing matter. We answer for the method and for honest conclusions, not for a flattering picture.'},
        {'question': 'Why pay in advance if there is no result yet?', 'answer': 'From the first day, experienced analysts and technical resources work on your brief. Payment in stages, 40 / 40 / 20, splits the risk evenly: you pay the second and third parts only after you have seen the interim and final results.'},
        {'question': 'What if we need extra data along the way?', 'answer': 'The main questions are fixed in the brief. If the work shows a need for further research, we frame it as a separate stage — with a scope and a fee agreed in advance.'},
        {'question': 'How long does a study take, and what does it cost?', 'answer': 'It depends on how hard the questions are and how available the sources are. You name the timing you want; we study the request and agree — or explain why more time is needed. You know the fee before the contract is signed, and it does not change unless the brief changes.'},
    ])
    _snippets(deep, DeepSnippet.Kind.STRATEGY, [
        'You name a person, a company or a market you want studied, you ask the questions that need an answer, and you set the timing you want. We study the request, agree the timing (or explain why more time is needed) and name the fee.',
        'In the end you receive an ordered report: clear answers to your questions, a reliability score for every source, and a clear line between what is an established fact and what is only an assumption.',
    ])
    _snippets(deep, DeepSnippet.Kind.STAT, [
        'retail points selling illicit goods',
        'regions covered',
        'of points sell the goods below the expected price',
        'of all points are concentrated in five regions',
    ])
    _snippets(deep, DeepSnippet.Kind.NOTE, [
        'Almost a quarter of all points are in one region (539 points, 23.5%); together with the second-largest region, 39.6%.',
        'At every third point (30%) the goods are sold without an excise stamp.',
        'The spread of the most common brands hides strong regional differences: in some regions a completely different brand dominates.',
    ])
    _snippets(deep, DeepSnippet.Kind.FACT, [
        'All parcels come from one city and one post office.',
        'Orders from different days are dispatched at the same time — between 18:22 and 19:15.',
        'The senders on record are recently registered entrepreneurs.',
        'The advertising photos show the same warehouse shelves.',
        'The range and the prices are almost identical.',
    ])
    _snippets(deep, DeepSnippet.Kind.LIMIT, [
        '“The count by category is a count of points, not of packs or sales volume. One point can have several violations, so the shares do not add up to 100%.”',
        '“If only a few points were surveyed in a region, its percentage is not a basis for comparing it with other regions.”',
        '“Finding nothing in six cities does not mean the goods are absent there — too few points were surveyed.”',
    ])
    _snippets(deep, DeepSnippet.Kind.GUARANTEE, [
        'You know the limits of the study before the deep work begins.',
        'No surprises at the end. If the first data require a change of direction within the agreed brief, we make it at no extra charge.',
        'The last payment is due only after the report is accepted against the criteria written into the contract.',
    ])
