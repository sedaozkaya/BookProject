from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from listings.forms import ListingForm
from listings.models import Favorite, Interested, Listing


def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            messages.success(request, 'İlan başarıyla oluşturuldu!')
            return redirect('listing_detail', pk=listing.pk)
        else:

            messages.error(request, 'Lütfen formdaki hataları düzeltin')
            print(form.errors)
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

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    return render(request, 'listing/favorites_list.html', {'favorites': favorites})

@login_required
def interested_list(request):
    interested_listings = Interested.objects.filter(user=request.user).select_related('listing')
    return render(request, 'listing/interested_list.html', {'interested_listings': interested_listings})

@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('my_listings')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'listing/edit_listing.html', {'form': form, 'listing': listing})



@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, user=request.user)

    if request.method == 'POST':
        listing.delete()
        return redirect('my_listings')

    return render(request, 'listing/confirm_delete.html', {'listing': listing})

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
    return render(request, 'user/home.html', context)

@login_required
def toggle_favorite(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    try:
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            listing=listing
        )

        if not created:
            favorite.delete()
            messages.success(request, 'İlan favorilerinizden çıkarıldı.')
        else:
            messages.success(request, 'İlan favorilerinize eklendi.')

    except Exception as e:
        messages.error(request, f'Bir hata oluştu: {str(e)}')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_interest(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    try:
        interest, created = Interested.objects.get_or_create(
            user=request.user,
            listing=listing
        )

        if not created:
            interest.delete()
            messages.success(request, 'İlan ilgi listenizden çıkarıldı.')
        else:
            messages.success(request, 'İlan ilgi listenize eklendi.')

    except Exception as e:
        messages.error(request, f'Bir hata oluştu: {str(e)}')

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def my_listings(request):
    listings = Listing.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/my_listings.html', {'listings': listings})


@login_required
def express_interest_and_message(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)


    Interested.objects.get_or_create(user=request.user, listing=listing)


    return redirect('start_conversation', listing_id=listing.id)

