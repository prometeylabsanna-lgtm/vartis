"""Англійський seed публічних текстів."""


def apply_english_copy() -> None:
    """Заливає EN, якщо поле порожнє, дорівнює дефолту або українському тексту."""
    from src.core.i18n_seed.analysis import seed_analysis
    from src.core.i18n_seed.articles_apply import seed_articles
    from src.core.i18n_seed.chrome import seed_chrome
    from src.core.i18n_seed.contacts import seed_contacts
    from src.core.i18n_seed.deep import seed_deep
    from src.core.i18n_seed.fill import under_ukrainian
    from src.core.i18n_seed.home_about import seed_about, seed_home
    from src.core.i18n_seed.services import seed_services

    with under_ukrainian():
        seed_chrome()
        seed_home()
        seed_about()
        seed_services()
        seed_analysis()
        seed_deep()
        seed_contacts()
        seed_articles()
