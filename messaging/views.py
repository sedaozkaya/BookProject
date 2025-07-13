from listings.models import Listing
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages

from messaging.models import Conversation, Message
from messaging.forms import MessageForm

@login_required
def start_conversation(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    seller = listing.user
    buyer = request.user

    if buyer == seller:
        django_messages.error(request, "Kendi ilanınız için mesajlaşma başlatamazsınız.")
        return redirect('listing_detail', listing_id=listing.id)

    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        buyer=buyer,
        seller=seller,
    )

    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)


    if request.user != conversation.buyer and request.user != conversation.seller:
        django_messages.error(request, "Bu konuşmaya erişim yetkiniz yok.")
        return redirect('home')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    chat_messages = conversation.messages.order_by('timestamp')

    context = {
        'conversation': conversation,
        'chat_messages': chat_messages,
        'form': form,
    }
    for msg in conversation.messages.exclude(sender=request.user):
        if not msg.is_read:
            msg.is_read = True
            msg.save()
    return render(request, 'messages/conversation_detail.html', context)

@login_required
def conversation_list(request):
    user = request.user
    conversations = (Conversation.objects.filter(buyer=user) | Conversation.objects.filter(seller=user)).distinct().order_by('-created_at')

    for conv in conversations:
        conv.unread_count = conv.messages.filter(is_read=False).exclude(sender=user).count()

    return render(request, 'messages/conversation_list.html', {
        'conversations': conversations,
        'user': user,
    })


@login_required
def my_conversations(request):
    user = request.user
    conversations = Conversation.objects.filter(seller=user) | Conversation.objects.filter(buyer=user)
    conversations = conversations.distinct().order_by('-created_at')


    for conv in conversations:
        conv.unread_count = Message.objects.filter(
            conversation=conv,
            is_read=False
        ).exclude(sender=user).count()

    context = {
        'conversations': conversations,
    }
    return render(request, 'messages/my_conversations.html', context)

