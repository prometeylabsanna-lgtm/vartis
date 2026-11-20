from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.core'
    verbose_name = 'Ядро'

    def ready(self):
        self._bind_translation_proxies()

    @staticmethod
    def _bind_translation_proxies():
        """Прокси наслідують переклад батька і бачать колонки *_en у формі."""
        from django.apps import apps
        from django.db.models.signals import post_init
        from modeltranslation.translator import delete_mt_init as translator_delete_init
        from modeltranslation.translator import translator

        for model in translator.get_registered_models():
            for candidate in apps.get_models():
                if not candidate._meta.proxy or candidate._meta.concrete_model is not model:
                    continue
                opts = translator._get_options_for_model(candidate)
                opts.registered = True
                candidate._meta._expire_cache()
                # post_init батька не спрацьовує для проксі, тож _mt_init лишається
                # і запис у колонку поточної мови мовчки губиться.
                post_init.connect(
                    translator_delete_init,
                    sender=candidate,
                    dispatch_uid=f'mt-clear-init-{candidate._meta.label_lower}',
                )
