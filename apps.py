from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LiveChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'live_chat'
    label = 'live_chat'
    verbose_name = _('Live Chat')

    def ready(self):
        pass
