# Live Chat Module

Real-time live chat with customers.

## Features

- Real-time chat conversations with website visitors
- Conversation lifecycle management: open, assigned, and closed statuses
- Assign conversations to specific team members
- Track visitor name and email for follow-up
- Message history with sender type differentiation (visitor vs agent)
- Customer satisfaction rating after conversation ends
- Conversation timestamps for start and end tracking

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Live Chat > Settings**

## Usage

Access via: **Menu > Live Chat**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/live_chat/dashboard/` | Chat overview and active conversation metrics |
| Conversations | `/m/live_chat/conversations/` | View and manage chat conversations |
| Settings | `/m/live_chat/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `ChatConversation` | Chat session with visitor info, status (open/assigned/closed), agent assignment, timestamps, and rating |
| `ChatMessage` | Individual message within a conversation with sender type, sender name, and message content |

## Permissions

| Permission | Description |
|------------|-------------|
| `live_chat.view_chatconversation` | View chat conversations |
| `live_chat.manage_chat` | Participate in and manage chat conversations |
| `live_chat.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
