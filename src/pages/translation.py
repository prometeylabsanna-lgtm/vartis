from modeltranslation.translator import TranslationOptions, register

from src.pages.models_about import (
    AboutPage,
    AboutPrinciple,
    AboutProcessStep,
    AboutStat,
    TeamMember,
)
from src.pages.models_analysis import AnalysisPage
from src.pages.models_analysis_items import (
    AnalysisInclude,
    AnalysisPaketStep,
    AnalysisPayTerm,
    AnalysisPricePart,
    AnalysisPriceRow,
    AnalysisRec,
    AnalysisRisk,
    AnalysisRiskLevel,
    AnalysisStep,
    AnalysisTariff,
    AnalysisTariffLine,
    AnalysisWhy,
)
from src.pages.models_contacts import ContactsPage, PrivacyPage
from src.pages.models_deep import (
    DeepAnalytics,
    DeepFaq,
    DeepGetItem,
    DeepPayStage,
    DeepQualityItem,
    DeepSnippet,
    DeepStep,
)
from src.pages.models_home import HomeAdvantage, HomeDirection, HomePage, HomeProcessStep
from src.pages.models_services import (
    ServiceAdvantage,
    ServiceMethodStep,
    ServicePage,
    ServiceScopeItem,
    ServiceScopeParagraph,
    ServicesIndex,
)


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'seo_title', 'seo_description', 'h1',
        'hero_title', 'hero_text', 'hero_cta',
        'services_title', 'services_lead',
        'advantages_title', 'advantages_lead',
        'mission_title', 'mission_text',
        'process_title', 'process_lead',
        'blog_title', 'blog_lead', 'blog_all_label',
    )


@register(HomeAdvantage)
class HomeAdvantageTR(TranslationOptions):
    fields = ('title', 'text')


@register(HomeProcessStep)
class HomeProcessStepTR(TranslationOptions):
    fields = ('title', 'text')


@register(HomeDirection)
class HomeDirectionTR(TranslationOptions):
    fields = ('title', 'text')


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = (
        'seo_title', 'seo_description', 'h1',
        'hero_title', 'hero_text', 'hero_cta', 'hero_cta_secondary',
        'intro_title', 'intro_text',
        'principles_title',
        'team_title', 'team_lead', 'expertise_label', 'career_label',
        'science_eyebrow', 'science_title', 'science_text', 'science_doi_label',
        'partners_eyebrow', 'partners_title', 'partners_text',
        'stats_title', 'process_title',
    )


@register(AboutPrinciple)
class AboutPrincipleTR(TranslationOptions):
    fields = ('title', 'text')


@register(TeamMember)
class TeamMemberTR(TranslationOptions):
    fields = ('name', 'role', 'regalia', 'bio', 'expertise', 'career_path')


@register(AboutStat)
class AboutStatTR(TranslationOptions):
    fields = ('label',)


@register(AboutProcessStep)
class AboutProcessStepTR(TranslationOptions):
    fields = ('title', 'text')


@register(ServicesIndex)
class ServicesIndexTR(TranslationOptions):
    fields = (
        'seo_title', 'seo_description', 'h1',
        'hero_title', 'hero_text', 'cta_primary', 'cta_secondary', 'card_more_label',
    )


@register(ServicePage)
class ServicePageTR(TranslationOptions):
    fields = (
        'seo_title', 'seo_description', 'h1',
        'title', 'short', 'hero_text',
        'cta_primary', 'cta_secondary',
        'scope_title', 'scope_text', 'scope_feature_title', 'scope_feature_text',
        'method_title', 'method_lead', 'method_step_prefix',
        'advantages_title', 'advantages_lead',
        'order_title', 'order_text',
        'related_title', 'card_text', 'tags',
    )


@register(ServiceScopeParagraph)
class ServiceScopeParagraphTR(TranslationOptions):
    fields = ('text',)


@register(ServiceScopeItem)
class ServiceScopeItemTR(TranslationOptions):
    fields = ('text',)


@register(ServiceMethodStep)
class ServiceMethodStepTR(TranslationOptions):
    fields = ('title', 'text')


@register(ServiceAdvantage)
class ServiceAdvantageTR(TranslationOptions):
    fields = ('title', 'text')


@register(AnalysisPage)
class AnalysisPageTR(TranslationOptions):
    fields = (
        'seo_title', 'seo_description', 'h1',
        'title', 'hero_title', 'hero_text', 'cta_primary', 'cta_secondary',
        'steps_eyebrow', 'steps_leads', 'steps_title',
        'risks_title', 'risks_lead', 'risks_note_title', 'risks_note',
        'recommendation_title', 'recommendation_text',
        'rec_heading', 'rec_badge', 'rec_verdict', 'rec_note', 'rec_flag',
        'rec_accept', 'rec_reject', 'rec_date', 'rec_caption',
        'result_title', 'result_text', 'result_method_prefix', 'result_method_suffix',
        'result_doi_label',
        'paket_eyebrow', 'paket_title', 'paket_subtitle', 'paket_lead', 'paket_text',
        'include_title', 'include_lead',
        'include_option_eyebrow', 'include_option_title', 'include_option_text',
        'why_title', 'price_title', 'price_lead', 'tariffs_title', 'price_note',
        'order_title', 'order_text', 'related_title', 'short', 'card_text', 'tags',
    )


@register(AnalysisStep)
class AnalysisStepTR(TranslationOptions):
    fields = ('title', 'text', 'bullets')


@register(AnalysisRisk)
class AnalysisRiskTR(TranslationOptions):
    fields = ('tag', 'title', 'text')


@register(AnalysisRiskLevel)
class AnalysisRiskLevelTR(TranslationOptions):
    fields = ('level', 'meaning', 'action')


@register(AnalysisRec)
class AnalysisRecTR(TranslationOptions):
    fields = ('title', 'text')


@register(AnalysisInclude)
class AnalysisIncludeTR(TranslationOptions):
    fields = ('title', 'text')


@register(AnalysisPaketStep)
class AnalysisPaketStepTR(TranslationOptions):
    fields = ('title', 'text')


@register(AnalysisWhy)
class AnalysisWhyTR(TranslationOptions):
    fields = ('title', 'text')


@register(AnalysisPricePart)
class AnalysisPricePartTR(TranslationOptions):
    fields = ('title', 'when', 'text', 'price')


@register(AnalysisTariff)
class AnalysisTariffTR(TranslationOptions):
    fields = ('name', 'subtitle', 'price', 'period')


@register(AnalysisTariffLine)
class AnalysisTariffLineTR(TranslationOptions):
    fields = ('label', 'value')


@register(AnalysisPayTerm)
class AnalysisPayTermTR(TranslationOptions):
    fields = ('title', 'text')


@register(AnalysisPriceRow)
class AnalysisPriceRowTR(TranslationOptions):
    fields = ('title', 'period', 'description', 'price_note')


@register(DeepAnalytics)
class DeepAnalyticsTR(TranslationOptions):
    fields = (
        'h1', 'hero_text', 'cta_primary', 'cta_secondary',
        'strategy_eyebrow', 'strategy_title',
        'compare_express_eyebrow', 'compare_express_title', 'compare_express_text',
        'compare_express_link',
        'compare_deep_eyebrow', 'compare_deep_title', 'compare_deep_text',
        'nda_title', 'nda_text', 'nda_note',
        'get_title', 'get_lead',
        'example_title', 'example_lead',
        'ex_frag1', 'ex_frag3', 'ex_frag3_lead', 'ex_frag4', 'ex_frag4_lead',
        'facts_title', 'conclusion_title', 'assumption_label', 'why_not_label',
        'ex_assumption', 'ex_why_not',
        'pay_title', 'pay_lead', 'paid_label', 'before_pay_label',
        'guarantee_title', 'quality_title', 'faq_title',
        'order_title', 'order_text', 'related_title',
    )


@register(DeepStep)
class DeepStepTR(TranslationOptions):
    fields = ('title', 'text')


@register(DeepGetItem)
class DeepGetItemTR(TranslationOptions):
    fields = ('title', 'text')


@register(DeepFaq)
class DeepFaqTR(TranslationOptions):
    fields = ('question', 'answer')


@register(DeepPayStage)
class DeepPayStageTR(TranslationOptions):
    fields = ('when', 'stage', 'title', 'text', 'see')


@register(DeepQualityItem)
class DeepQualityItemTR(TranslationOptions):
    fields = ('title', 'text')


@register(DeepSnippet)
class DeepSnippetTR(TranslationOptions):
    fields = ('text',)


@register(ContactsPage)
class ContactsPageTR(TranslationOptions):
    fields = (
        'seo_title', 'seo_description', 'h1',
        'hero_title', 'hero_text', 'cta_primary', 'cta_secondary',
        'info_title', 'phone_label', 'email_label', 'facebook_label',
        'whatsapp_label', 'signal_label', 'telegram_label',
        'phone_hint', 'email_hint', 'whatsapp_hint', 'signal_hint', 'telegram_hint',
        'write_label', 'office_label', 'office_note', 'office_cta',
    )


@register(PrivacyPage)
class PrivacyPageTR(TranslationOptions):
    fields = (
        'seo_title', 'seo_description', 'h1',
        'hero_title', 'hero_text', 'body',
    )
