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

    # Yetki kontrolü
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
    return render(request, 'messages/conversation_detail.html', context)

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(
        buyer=request.user
    ) | Conversation.objects.filter(
        seller=request.user
    )
    conversations = conversations.distinct().order_by('-created_at')
    return render(request, 'messages/conversation_list.html', {'conversations': conversations})

@login_required
def my_conversations(request):
    user = request.user
    conversations = Conversation.objects.filter(seller=user) | Conversation.objects.filter(buyer=user)
    conversations = conversations.distinct().order_by('-created_at')

    context = {
        'conversations': conversations,
    }
    return render(request, 'messages/my_conversations.html', context)
