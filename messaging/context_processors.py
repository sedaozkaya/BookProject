
from messaging.models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        user = request.user
        conversations = user.buyer_conversations.all() | user.seller_conversations.all()
        unread_count = Message.objects.filter(
            conversation__in=conversations,
            is_read=False
        ).exclude(sender=user).count()
        return {'messages_count': unread_count}
    return {'messages_count': 0}
