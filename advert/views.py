from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from .forms import ListingForm
from django.contrib.auth.decorators import login_required
from .models import Listing, Favorite, Interested




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

    return render(request, 'listing/listing_detail.html', {
        'listing': listing,
        'is_favorited': is_favorited
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



