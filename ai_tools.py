"""AI tools for the Live Chat module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListChatConversations(AssistantTool):
    name = "list_chat_conversations"
    description = "List live chat conversations."
    module_id = "live_chat"
    required_permission = "live_chat.view_chatconversation"
    parameters = {
        "type": "object",
        "properties": {"status": {"type": "string", "description": "open, assigned, closed"}, "limit": {"type": "integer"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from live_chat.models import ChatConversation
        qs = ChatConversation.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {"conversations": [{"id": str(c.id), "visitor_name": c.visitor_name, "visitor_email": c.visitor_email, "status": c.status, "started_at": c.started_at.isoformat() if c.started_at else None, "rating": c.rating} for c in qs.order_by('-started_at')[:limit]]}


@register_tool
class GetChatConversation(AssistantTool):
    name = "get_chat_conversation"
    description = "Get a chat conversation with its messages."
    module_id = "live_chat"
    required_permission = "live_chat.view_chatconversation"
    parameters = {"type": "object", "properties": {"conversation_id": {"type": "string"}}, "required": ["conversation_id"], "additionalProperties": False}

    def execute(self, args, request):
        from live_chat.models import ChatConversation, ChatMessage
        c = ChatConversation.objects.get(id=args['conversation_id'])
        messages = ChatMessage.objects.filter(conversation=c).order_by('created_at')
        return {
            "id": str(c.id), "visitor_name": c.visitor_name, "status": c.status,
            "messages": [{"sender_type": m.sender_type, "sender_name": m.sender_name, "message": m.message, "created_at": m.created_at.isoformat()} for m in messages],
        }


@register_tool
class AssignChatConversation(AssistantTool):
    name = "assign_chat_conversation"
    description = "Assign a chat conversation to an agent."
    module_id = "live_chat"
    required_permission = "live_chat.change_chatconversation"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "conversation_id": {"type": "string", "description": "Conversation ID"},
            "agent_id": {"type": "string", "description": "Agent UUID to assign to"},
        },
        "required": ["conversation_id", "agent_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from live_chat.models import ChatConversation
        c = ChatConversation.objects.get(id=args['conversation_id'])
        c.assigned_to = args['agent_id']
        c.status = 'assigned'
        c.save(update_fields=['assigned_to', 'status'])
        return {"id": str(c.id), "visitor_name": c.visitor_name, "status": "assigned"}


@register_tool
class CloseChatConversation(AssistantTool):
    name = "close_chat_conversation"
    description = "Close a chat conversation."
    module_id = "live_chat"
    required_permission = "live_chat.change_chatconversation"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"conversation_id": {"type": "string", "description": "Conversation ID"}},
        "required": ["conversation_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from django.utils import timezone
        from live_chat.models import ChatConversation
        c = ChatConversation.objects.get(id=args['conversation_id'])
        if c.status == 'closed':
            return {"error": "Conversation is already closed"}
        c.status = 'closed'
        c.ended_at = timezone.now()
        c.save(update_fields=['status', 'ended_at'])
        return {"id": str(c.id), "visitor_name": c.visitor_name, "status": "closed"}


@register_tool
class SendChatMessage(AssistantTool):
    name = "send_chat_message"
    description = "Send a message in a chat conversation as an agent."
    module_id = "live_chat"
    required_permission = "live_chat.change_chatconversation"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "conversation_id": {"type": "string", "description": "Conversation ID"},
            "message": {"type": "string", "description": "Message text"},
            "sender_name": {"type": "string", "description": "Agent name (default: AI Assistant)"},
        },
        "required": ["conversation_id", "message"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from live_chat.models import ChatConversation, ChatMessage
        c = ChatConversation.objects.get(id=args['conversation_id'])
        m = ChatMessage.objects.create(
            conversation=c,
            sender_type='agent',
            sender_name=args.get('sender_name', 'AI Assistant'),
            message=args['message'],
        )
        return {"id": str(m.id), "conversation_id": str(c.id), "sent": True}
