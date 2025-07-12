from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

from listings.models import Listing
from messaging.forms import MessageForm
from messaging.models import Conversation, Message
from django.contrib import messages
from django.db.models import Q

@login_required
def start_conversation(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    seller = listing.user
    buyer = request.user

    if buyer == seller:
        messages.error(request, "Kendi ilanınız için mesajlaşma başlatamazsınız.")
        return redirect('listing_detail', listing_id=listing.id)

    # Var olan conversation'ı al ya da yeni oluştur
    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        buyer=buyer,
        seller=seller,
    )

    return redirect('conversation_detail', conversation_id=conversation.id)

from django.contrib import messages as django_messages  # ⚠️ Çakışmayı önlemek için alias verdik

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in [conversation.buyer, conversation.seller]:
        django_messages.error(request, "Bu konuşmaya erişim yetkiniz yok.")
        return redirect('home')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=content  # ✅ doğru alan adı
            )
            return redirect('conversation_detail', conversation_id=conversation.id)

    message_list = conversation.messages.all()  # ✅ 'messages' yerine 'message_list' diyelim ki karışmasın

    return render(request, 'messages/conversation_detail.html', {
        'conversation': conversation,
        'messages': message_list,
    })


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(
        models.Q(buyer=request.user) | models.Q(seller=request.user)
    ).order_by('-created_at')
    return render(request, 'messages/conversation_list.html', {'conversations': conversations})

@login_required
def my_conversations(request):
    user = request.user
    conversations = Conversation.objects.filter(seller=user) | Conversation.objects.filter(buyer=user)

    conversations = conversations.distinct().order_by('-timestamp')

    context = {
        'conversations': conversations,
    }
    return render(request, 'messages/my_conversations.html', context)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)


    if request.user != conversation.seller and request.user != conversation.buyer:
        return redirect('home')  #

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


    messages = conversation.messages.order_by('timestamp')

    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form,
    }
    return render(request, 'messages/conversation_detail.html', context)
