"""Tests for live_chat models."""
import pytest
from django.utils import timezone

from live_chat.models import ChatConversation, ChatMessage


@pytest.mark.django_db
class TestChatConversation:
    """ChatConversation model tests."""

    def test_create(self, chat_conversation):
        """Test ChatConversation creation."""
        assert chat_conversation.pk is not None
        assert chat_conversation.is_deleted is False

    def test_soft_delete(self, chat_conversation):
        """Test soft delete."""
        pk = chat_conversation.pk
        chat_conversation.is_deleted = True
        chat_conversation.deleted_at = timezone.now()
        chat_conversation.save()
        assert not ChatConversation.objects.filter(pk=pk).exists()
        assert ChatConversation.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, chat_conversation):
        """Test default queryset excludes deleted."""
        chat_conversation.is_deleted = True
        chat_conversation.deleted_at = timezone.now()
        chat_conversation.save()
        assert ChatConversation.objects.filter(hub_id=hub_id).count() == 0


@pytest.mark.django_db
class TestChatMessage:
    """ChatMessage model tests."""

    def test_create(self, chat_message):
        """Test ChatMessage creation."""
        assert chat_message.pk is not None
        assert chat_message.is_deleted is False

    def test_soft_delete(self, chat_message):
        """Test soft delete."""
        pk = chat_message.pk
        chat_message.is_deleted = True
        chat_message.deleted_at = timezone.now()
        chat_message.save()
        assert not ChatMessage.objects.filter(pk=pk).exists()
        assert ChatMessage.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, chat_message):
        """Test default queryset excludes deleted."""
        chat_message.is_deleted = True
        chat_message.deleted_at = timezone.now()
        chat_message.save()
        assert ChatMessage.objects.filter(hub_id=hub_id).count() == 0


