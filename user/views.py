from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Count, Q, Prefetch

from user.forms import UserUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User



class CustomUserCreationForm(UserCreationForm):


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
    return render(request, 'user/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'user/profile.html')

from django.db.models import Prefetch
from listings.models import Listing, Interested

@login_required
def my_listings(request):
    listings = Listing.objects.filter(user=request.user).prefetch_related(
        Prefetch('interested_set', queryset=Interested.objects.select_related('user'), to_attr='interested_users')
    )
    return render(request, 'user/my_listings.html', {'listings': listings})





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

    return render(request, 'user/edit_profile.html', {'form': form})

def top_donors(request):
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)
    one_month_ago = now - timedelta(days=30)


    all_time_donors = User.objects.annotate(
        free_count=Count('listing', filter=Q(listing__donation_type='free'))
    ).filter(free_count__gt=0).order_by('-free_count')[:10]


    weekly_donors = User.objects.annotate(
        free_count=Count('listing', filter=Q(
            listing__donation_type='free',
            listing__created_at__gte=one_week_ago
        ))
    ).filter(free_count__gt=0).order_by('-free_count')[:10]


    monthly_donors = User.objects.annotate(
        free_count=Count('listing', filter=Q(
            listing__donation_type='free',
            listing__created_at__gte=one_month_ago
        ))
    ).filter(free_count__gt=0).order_by('-free_count')[:10]

    context = {
        'all_time_donors': all_time_donors,
        'weekly_donors': weekly_donors,
        'monthly_donors': monthly_donors,
    }

    return render(request, 'user/top_donors.html', context)


def toggle_dark_mode(request):
    response = redirect(request.META.get('HTTP_REFERER', 'home'))
    current = request.COOKIES.get('dark_mode', 'false')
    response.set_cookie('dark_mode', 'false' if current == 'true' else 'true', max_age=60*60*24*365)
    return response




