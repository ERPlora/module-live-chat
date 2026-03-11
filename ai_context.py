"""
AI context for the Live Chat module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Live Chat

### Models

**ChatConversation**
- `visitor_name` (CharField, blank) — name provided by the visitor
- `visitor_email` (EmailField, blank) — email provided by the visitor
- `status` (CharField) — choices: open, assigned, closed
- `assigned_to` (UUIDField, nullable) — UUID of the staff member handling the chat
- `started_at` (DateTimeField, auto) — when the conversation began
- `ended_at` (DateTimeField, nullable) — when the conversation was closed
- `rating` (PositiveIntegerField, nullable) — customer satisfaction rating (typically 1-5)

**ChatMessage**
- `conversation` (FK → ChatConversation, CASCADE) — the conversation this message belongs to
- `sender_type` (CharField, default 'visitor') — 'visitor' or 'agent'
- `sender_name` (CharField, blank) — display name of the sender
- `message` (TextField) — message content

### Key flows

1. **New chat**: Visitor opens chat → create ChatConversation with status='open', optional name/email.
2. **Assign**: Staff member picks up the chat → set `status='assigned'` and `assigned_to` to the staff UUID.
3. **Exchange messages**: Create ChatMessage records with `sender_type='visitor'` or `sender_type='agent'`.
4. **Close**: Set `status='closed'` and `ended_at` to current timestamp. Optionally collect `rating`.
5. **List open chats**: Filter ChatConversation by `status='open'` or `status='assigned'`.

### Relationships
- ChatMessage.conversation → ChatConversation (FK, CASCADE)
- No FK to customers module — visitor identity is stored as plain text fields
- `assigned_to` is a UUID reference to an accounts.LocalUser (not a FK)
"""
