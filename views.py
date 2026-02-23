"""
Live Chat Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('live_chat', 'dashboard')
@htmx_view('live_chat/pages/dashboard.html', 'live_chat/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('live_chat', 'conversations')
@htmx_view('live_chat/pages/conversations.html', 'live_chat/partials/conversations_content.html')
def conversations(request):
    """Conversations view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('live_chat', 'settings')
@htmx_view('live_chat/pages/settings.html', 'live_chat/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

