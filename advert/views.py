from django.contrib import messages
from django.db import models

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .forms import ListingForm, MessageForm
from django.contrib.auth.decorators import login_required
from .models import Listing, Favorite, Interested
from .forms import UserUpdateForm
from django.contrib.auth.models import User
from django.db.models import Count, Q

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib import messages
from django.db.models import Q







class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_listing(request):
    if request.method == 'POST':

        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'listing/create_listing.html', {'form': form})





@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    is_favorited = False
    is_interested = False

    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, listing=listing).exists()
        is_interested = Interested.objects.filter(user=request.user, listing=listing).exists()

    if request.method == 'POST':
        if 'favorite' in request.POST:
            if not is_favorited:
                Favorite.objects.create(user=request.user, listing=listing)
                messages.success(request, "İlan favorilere eklendi.")
            else:
                Favorite.objects.filter(user=request.user, listing=listing).delete()
                messages.success(request, "Favorilerden çıkarıldı.")
            return redirect('listing_detail', pk=pk)

        elif 'interested' in request.POST:
            if not is_interested:
                Interested.objects.create(user=request.user, listing=listing)
                messages.success(request, "İlgilenme bildirildi.")
            else:
                Interested.objects.filter(user=request.user, listing=listing).delete()
                messages.success(request, "İlgilenme iptal edildi.")
            return redirect('listing_detail', pk=pk)

    return render(request, 'listing/listing_detail.html', {
        'listing': listing,
        'is_favorited': is_favorited,
        'is_interested': is_interested,
    })




from django.shortcuts import render
from .models import Listing

def home(request):
    listings = Listing.objects.all()

    level = request.GET.get('level')
    listing_type = request.GET.get('listing_type')
    donation_type = request.GET.get('donation_type')
    related_course = request.GET.get('related_course')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if level:
        listings = listings.filter(level=level)
    if listing_type:
        listings = listings.filter(listing_type=listing_type)
    if donation_type:
        listings = listings.filter(donation_type=donation_type)
    if related_course:
        listings = listings.filter(related_course__icontains=related_course)
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)

    context = {
        'listings': listings
    }
    return render(request, 'home.html', context)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    return render(request, 'favorites_list.html', {'favorites': favorites})

@login_required
def interested_list(request):
    interested_listings = Interested.objects.filter(user=request.user).select_related('listing')
    return render(request, 'interested_list.html', {'interested_listings': interested_listings})
@login_required
def profile_view(request):
    return render(request, 'profile.html')
@login_required
def my_listings(request):
    listings = Listing.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_listings.html', {'listings': listings})

@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('my_listings')  # düzenlendikten sonra ilanlarım sayfasına dön
    else:
        form = ListingForm(instance=listing)

    return render(request, 'edit_listing.html', {'form': form, 'listing': listing})



@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, user=request.user)

    if request.method == 'POST':
        listing.delete()
        return redirect('my_listings')

    return render(request, 'confirm_delete.html', {'listing': listing})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiliniz güncellendi.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

def top_donors(request):
    donors = User.objects.annotate(
        free_count=Count('listing', filter=Q(listing__donation_type='free'))
    ).filter(free_count__gt=0).order_by('-free_count')[:10]

    return render(request, 'top_donors.html', {'donors': donors})



def toggle_dark_mode(request):
    response = redirect(request.META.get('HTTP_REFERER', 'home'))
    current = request.COOKIES.get('dark_mode', 'false')
    response.set_cookie('dark_mode', 'false' if current == 'true' else 'true', max_age=60*60*24*365)
    return response



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

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in [conversation.buyer, conversation.seller]:
        messages.error(request, "Bu konuşmaya erişim yetkiniz yok.")
        return redirect('home')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            return redirect('conversation_detail', conversation_id=conversation.id)

    messages_list = conversation.messages.all()
    return render(request, 'conversation_detail.html', {
        'conversation': conversation,
        'messages': messages_list
    })

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(
        models.Q(buyer=request.user) | models.Q(seller=request.user)
    ).order_by('-created_at')
    return render(request, 'conversation_list.html', {'conversations': conversations})

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

    # Sadece alıcı veya satıcı görebilsin
    if request.user != conversation.seller and request.user != conversation.buyer:
        return redirect('home')  # veya 403 sayfası

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





