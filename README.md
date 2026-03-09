# Live Chat

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `live_chat` |
| **Version** | `1.0.0` |
| **Icon** | `chatbubble-ellipses-outline` |
| **Dependencies** | None |

## Models

### `ChatConversation`

ChatConversation(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, visitor_name, visitor_email, status, assigned_to, started_at, ended_at, rating)

| Field | Type | Details |
|-------|------|---------|
| `visitor_name` | CharField | max_length=255, optional |
| `visitor_email` | EmailField | max_length=254, optional |
| `status` | CharField | max_length=20, choices: open, assigned, closed |
| `assigned_to` | UUIDField | max_length=32, optional |
| `started_at` | DateTimeField | optional |
| `ended_at` | DateTimeField | optional |
| `rating` | PositiveIntegerField | optional |

### `ChatMessage`

ChatMessage(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, conversation, sender_type, sender_name, message)

| Field | Type | Details |
|-------|------|---------|
| `conversation` | ForeignKey | → `live_chat.ChatConversation`, on_delete=CASCADE |
| `sender_type` | CharField | max_length=10 |
| `sender_name` | CharField | max_length=255, optional |
| `message` | TextField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `ChatMessage` | `conversation` | `live_chat.ChatConversation` | CASCADE | No |

## URL Endpoints

Base path: `/m/live_chat/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `conversations/` | `conversations` | GET |
| `chat_conversations/` | `chat_conversations_list` | GET |
| `chat_conversations/add/` | `chat_conversation_add` | GET/POST |
| `chat_conversations/<uuid:pk>/edit/` | `chat_conversation_edit` | GET |
| `chat_conversations/<uuid:pk>/delete/` | `chat_conversation_delete` | GET/POST |
| `chat_conversations/bulk/` | `chat_conversations_bulk_action` | GET/POST |
| `chat_messages/` | `chat_messages_list` | GET |
| `chat_messages/add/` | `chat_message_add` | GET/POST |
| `chat_messages/<uuid:pk>/edit/` | `chat_message_edit` | GET |
| `chat_messages/<uuid:pk>/delete/` | `chat_message_delete` | GET/POST |
| `chat_messages/bulk/` | `chat_messages_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `live_chat.view_chatconversation` | View Chatconversation |
| `live_chat.manage_chat` | Manage Chat |
| `live_chat.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `manage_chat`, `view_chatconversation`
- **employee**: `view_chatconversation`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Conversations | `chatbubble-ellipses-outline` | `conversations` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_chat_conversations`

List live chat conversations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | open, assigned, closed |
| `limit` | integer | No |  |

### `get_chat_conversation`

Get a chat conversation with its messages.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `conversation_id` | string | Yes |  |

### `assign_chat_conversation`

Assign a chat conversation to an agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `conversation_id` | string | Yes | Conversation ID |
| `agent_id` | string | Yes | Agent UUID to assign to |

### `close_chat_conversation`

Close a chat conversation.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `conversation_id` | string | Yes | Conversation ID |

### `send_chat_message`

Send a message in a chat conversation as an agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `conversation_id` | string | Yes | Conversation ID |
| `message` | string | Yes | Message text |
| `sender_name` | string | No | Agent name (default: AI Assistant) |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  live_chat/
    css/
    js/
templates/
  live_chat/
    pages/
      chat_conversation_add.html
      chat_conversation_edit.html
      chat_conversations.html
      chat_message_add.html
      chat_message_edit.html
      chat_messages.html
      conversations.html
      dashboard.html
      index.html
      settings.html
    partials/
      chat_conversation_add_content.html
      chat_conversation_edit_content.html
      chat_conversations_content.html
      chat_conversations_list.html
      chat_message_add_content.html
      chat_message_edit_content.html
      chat_messages_content.html
      chat_messages_list.html
      conversations_content.html
      dashboard_content.html
      panel_chat_conversation_add.html
      panel_chat_conversation_edit.html
      panel_chat_message_add.html
      panel_chat_message_edit.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
