from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

CHAT_STATUS = [
    ('open', _('Open')),
    ('assigned', _('Assigned')),
    ('closed', _('Closed')),
]

class ChatConversation(HubBaseModel):
    visitor_name = models.CharField(max_length=255, blank=True, verbose_name=_('Visitor Name'))
    visitor_email = models.EmailField(blank=True, verbose_name=_('Visitor Email'))
    status = models.CharField(max_length=20, default='open', choices=CHAT_STATUS, verbose_name=_('Status'))
    assigned_to = models.UUIDField(null=True, blank=True, verbose_name=_('Assigned To'))
    started_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Started At'))
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Ended At'))
    rating = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Rating'))

    class Meta(HubBaseModel.Meta):
        db_table = 'live_chat_chatconversation'

    def __str__(self):
        return str(self.id)


class ChatMessage(HubBaseModel):
    conversation = models.ForeignKey('ChatConversation', on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, default='visitor', verbose_name=_('Sender Type'))
    sender_name = models.CharField(max_length=255, blank=True, verbose_name=_('Sender Name'))
    message = models.TextField(verbose_name=_('Message'))

    class Meta(HubBaseModel.Meta):
        db_table = 'live_chat_chatmessage'

    def __str__(self):
        return str(self.id)

