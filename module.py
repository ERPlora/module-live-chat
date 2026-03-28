from django.utils.translation import gettext_lazy as _

MODULE_ID = 'live_chat'
MODULE_NAME = _('Live Chat')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'chatbubble-ellipses-outline'
MODULE_DESCRIPTION = _('Real-time live chat with customers')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'communication'
HAS_MODELS = True

MENU = {
    'label': _('Live Chat'),
    'icon': 'chatbubble-ellipses-outline',
    'order': 65,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Conversations'), 'icon': 'chatbubble-ellipses-outline', 'id': 'conversations'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'live_chat.view_chatconversation',
'live_chat.manage_chat',
'live_chat.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "manage_chat",
        "view_chatconversation",
    ],
    "employee": [
        "view_chatconversation",
    ],
}
