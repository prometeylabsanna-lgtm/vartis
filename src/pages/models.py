"""Публічні моделі сторінок. Таблиці лишаються в app pages."""

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
from src.pages.models_base import SEOFields
from src.pages.models_contacts import ContactsPage, PrivacyPage
from src.pages.models_deep import (
    DEEP_SLUG,
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
    SERVICE_SLUGS,
    ServiceAdvantage,
    ServiceMethodStep,
    ServicePage,
    ServiceScopeItem,
    ServiceScopeParagraph,
    ServicesIndex,
)

__all__ = [
    'SEOFields',
    'SERVICE_SLUGS',
    'DEEP_SLUG',
    'HomePage',
    'HomeAdvantage',
    'HomeDirection',
    'HomeProcessStep',
    'AboutPage',
    'AboutPrinciple',
    'TeamMember',
    'AboutStat',
    'AboutProcessStep',
    'ServicesIndex',
    'ServicePage',
    'ServiceScopeParagraph',
    'ServiceScopeItem',
    'ServiceMethodStep',
    'ServiceAdvantage',
    'AnalysisPage',
    'AnalysisStep',
    'AnalysisRisk',
    'AnalysisRiskLevel',
    'AnalysisRec',
    'AnalysisInclude',
    'AnalysisPaketStep',
    'AnalysisWhy',
    'AnalysisPricePart',
    'AnalysisTariff',
    'AnalysisTariffLine',
    'AnalysisPayTerm',
    'AnalysisPriceRow',
    'DeepAnalytics',
    'DeepStep',
    'DeepGetItem',
    'DeepFaq',
    'DeepPayStage',
    'DeepQualityItem',
    'DeepSnippet',
    'ContactsPage',
    'PrivacyPage',
]
