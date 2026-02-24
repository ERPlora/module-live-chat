"""Tests for live_chat views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('live_chat:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('live_chat:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('live_chat:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestChatConversationViews:
    """ChatConversation view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('live_chat:chat_conversations_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('live_chat:chat_conversations_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('live_chat:chat_conversations_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('live_chat:chat_conversations_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('live_chat:chat_conversations_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('live_chat:chat_conversations_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('live_chat:chat_conversation_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('live_chat:chat_conversation_add')
        data = {
            'visitor_name': 'New Visitor Name',
            'visitor_email': 'test@example.com',
            'status': 'New Status',
            'assigned_to': 'test',
            'ended_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, chat_conversation):
        """Test edit form loads."""
        url = reverse('live_chat:chat_conversation_edit', args=[chat_conversation.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, chat_conversation):
        """Test editing via POST."""
        url = reverse('live_chat:chat_conversation_edit', args=[chat_conversation.pk])
        data = {
            'visitor_name': 'Updated Visitor Name',
            'visitor_email': 'test@example.com',
            'status': 'Updated Status',
            'assigned_to': 'test',
            'ended_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, chat_conversation):
        """Test soft delete via POST."""
        url = reverse('live_chat:chat_conversation_delete', args=[chat_conversation.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        chat_conversation.refresh_from_db()
        assert chat_conversation.is_deleted is True

    def test_bulk_delete(self, auth_client, chat_conversation):
        """Test bulk delete."""
        url = reverse('live_chat:chat_conversations_bulk_action')
        response = auth_client.post(url, {'ids': str(chat_conversation.pk), 'action': 'delete'})
        assert response.status_code == 200
        chat_conversation.refresh_from_db()
        assert chat_conversation.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('live_chat:chat_conversations_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestChatMessageViews:
    """ChatMessage view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('live_chat:chat_messages_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('live_chat:chat_messages_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('live_chat:chat_messages_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('live_chat:chat_messages_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('live_chat:chat_messages_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('live_chat:chat_messages_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('live_chat:chat_message_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('live_chat:chat_message_add')
        data = {
            'sender_type': 'New Sender Type',
            'sender_name': 'New Sender Name',
            'message': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, chat_message):
        """Test edit form loads."""
        url = reverse('live_chat:chat_message_edit', args=[chat_message.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, chat_message):
        """Test editing via POST."""
        url = reverse('live_chat:chat_message_edit', args=[chat_message.pk])
        data = {
            'sender_type': 'Updated Sender Type',
            'sender_name': 'Updated Sender Name',
            'message': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, chat_message):
        """Test soft delete via POST."""
        url = reverse('live_chat:chat_message_delete', args=[chat_message.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        chat_message.refresh_from_db()
        assert chat_message.is_deleted is True

    def test_bulk_delete(self, auth_client, chat_message):
        """Test bulk delete."""
        url = reverse('live_chat:chat_messages_bulk_action')
        response = auth_client.post(url, {'ids': str(chat_message.pk), 'action': 'delete'})
        assert response.status_code == 200
        chat_message.refresh_from_db()
        assert chat_message.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('live_chat:chat_messages_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('live_chat:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('live_chat:settings')
        response = client.get(url)
        assert response.status_code == 302

