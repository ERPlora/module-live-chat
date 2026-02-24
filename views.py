"""
Live Chat Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import ChatConversation, ChatMessage

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('live_chat', 'dashboard')
@htmx_view('live_chat/pages/index.html', 'live_chat/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_chat_conversations': ChatConversation.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_chat_messages': ChatMessage.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# ChatConversation
# ======================================================================

CHAT_CONVERSATION_SORT_FIELDS = {
    'status': 'status',
    'rating': 'rating',
    'visitor_name': 'visitor_name',
    'visitor_email': 'visitor_email',
    'assigned_to': 'assigned_to',
    'ended_at': 'ended_at',
    'created_at': 'created_at',
}

def _build_chat_conversations_context(hub_id, per_page=10):
    qs = ChatConversation.objects.filter(hub_id=hub_id, is_deleted=False).order_by('status')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'chat_conversations': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'status',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_chat_conversations_list(request, hub_id, per_page=10):
    ctx = _build_chat_conversations_context(hub_id, per_page)
    return django_render(request, 'live_chat/partials/chat_conversations_list.html', ctx)

@login_required
@with_module_nav('live_chat', 'conversations')
@htmx_view('live_chat/pages/chat_conversations.html', 'live_chat/partials/chat_conversations_content.html')
def chat_conversations_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'status')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = ChatConversation.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(visitor_name__icontains=search_query) | Q(visitor_email__icontains=search_query) | Q(status__icontains=search_query))

    order_by = CHAT_CONVERSATION_SORT_FIELDS.get(sort_field, 'status')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['status', 'rating', 'visitor_name', 'visitor_email', 'assigned_to', 'ended_at']
        headers = ['Status', 'Rating', 'Visitor Name', 'Visitor Email', 'Assigned To', 'Ended At']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='chat_conversations.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='chat_conversations.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'live_chat/partials/chat_conversations_list.html', {
            'chat_conversations': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'chat_conversations': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def chat_conversation_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        visitor_name = request.POST.get('visitor_name', '').strip()
        visitor_email = request.POST.get('visitor_email', '').strip()
        status = request.POST.get('status', '').strip()
        assigned_to = request.POST.get('assigned_to', '').strip()
        ended_at = request.POST.get('ended_at') or None
        rating = int(request.POST.get('rating', 0) or 0)
        obj = ChatConversation(hub_id=hub_id)
        obj.visitor_name = visitor_name
        obj.visitor_email = visitor_email
        obj.status = status
        obj.assigned_to = assigned_to
        obj.ended_at = ended_at
        obj.rating = rating
        obj.save()
        return _render_chat_conversations_list(request, hub_id)
    return django_render(request, 'live_chat/partials/panel_chat_conversation_add.html', {})

@login_required
def chat_conversation_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ChatConversation, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.visitor_name = request.POST.get('visitor_name', '').strip()
        obj.visitor_email = request.POST.get('visitor_email', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.assigned_to = request.POST.get('assigned_to', '').strip()
        obj.ended_at = request.POST.get('ended_at') or None
        obj.rating = int(request.POST.get('rating', 0) or 0)
        obj.save()
        return _render_chat_conversations_list(request, hub_id)
    return django_render(request, 'live_chat/partials/panel_chat_conversation_edit.html', {'obj': obj})

@login_required
@require_POST
def chat_conversation_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ChatConversation, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_chat_conversations_list(request, hub_id)

@login_required
@require_POST
def chat_conversations_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = ChatConversation.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_chat_conversations_list(request, hub_id)


# ======================================================================
# ChatMessage
# ======================================================================

CHAT_MESSAGE_SORT_FIELDS = {
    'conversation': 'conversation',
    'sender_type': 'sender_type',
    'sender_name': 'sender_name',
    'message': 'message',
    'created_at': 'created_at',
}

def _build_chat_messages_context(hub_id, per_page=10):
    qs = ChatMessage.objects.filter(hub_id=hub_id, is_deleted=False).order_by('conversation')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'chat_messages': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'conversation',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_chat_messages_list(request, hub_id, per_page=10):
    ctx = _build_chat_messages_context(hub_id, per_page)
    return django_render(request, 'live_chat/partials/chat_messages_list.html', ctx)

@login_required
@with_module_nav('live_chat', 'conversations')
@htmx_view('live_chat/pages/chat_messages.html', 'live_chat/partials/chat_messages_content.html')
def chat_messages_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'conversation')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = ChatMessage.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(sender_type__icontains=search_query) | Q(sender_name__icontains=search_query) | Q(message__icontains=search_query))

    order_by = CHAT_MESSAGE_SORT_FIELDS.get(sort_field, 'conversation')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['conversation', 'sender_type', 'sender_name', 'message']
        headers = ['ChatConversation', 'Sender Type', 'Sender Name', 'Message']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='chat_messages.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='chat_messages.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'live_chat/partials/chat_messages_list.html', {
            'chat_messages': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'chat_messages': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def chat_message_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        sender_type = request.POST.get('sender_type', '').strip()
        sender_name = request.POST.get('sender_name', '').strip()
        message = request.POST.get('message', '').strip()
        obj = ChatMessage(hub_id=hub_id)
        obj.sender_type = sender_type
        obj.sender_name = sender_name
        obj.message = message
        obj.save()
        return _render_chat_messages_list(request, hub_id)
    return django_render(request, 'live_chat/partials/panel_chat_message_add.html', {})

@login_required
def chat_message_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ChatMessage, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.sender_type = request.POST.get('sender_type', '').strip()
        obj.sender_name = request.POST.get('sender_name', '').strip()
        obj.message = request.POST.get('message', '').strip()
        obj.save()
        return _render_chat_messages_list(request, hub_id)
    return django_render(request, 'live_chat/partials/panel_chat_message_edit.html', {'obj': obj})

@login_required
@require_POST
def chat_message_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ChatMessage, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_chat_messages_list(request, hub_id)

@login_required
@require_POST
def chat_messages_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = ChatMessage.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_chat_messages_list(request, hub_id)


@login_required
@with_module_nav('live_chat', 'settings')
@htmx_view('live_chat/pages/settings.html', 'live_chat/partials/settings_content.html')
def settings_view(request):
    return {}

