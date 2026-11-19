from django.db import models

ICON_HELP = 'Ключ з vartis_icons, наприклад HiconOutlineShieldTick.'


class SEOFields(models.Model):
    seo_title = models.CharField('SEO Title', max_length=200, blank=True)
    seo_description = models.TextField('SEO Description', blank=True)
    h1 = models.CharField('H1', max_length=200, blank=True)

    class Meta:
        abstract = True
