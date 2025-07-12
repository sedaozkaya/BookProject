

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import PasswordResetCode
from .forms import PasswordResetRequestForm, PasswordResetCodeForm, SetNewPasswordForm
from django.contrib import messages

def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                reset_code = PasswordResetCode.objects.create(user=user)

                send_mail(
                    subject='Şifre Sıfırlama Kodu',
                    message=f'Şifre sıfırlama kodunuz: {reset_code.code}',
                    from_email='bookloop.destek@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, "E-posta adresinize bir kod gönderildi.")
                # Kod girme sayfasına yönlendirme yapılabilir
                return redirect('password_reset_verify')
            except User.DoesNotExist:
                messages.error(request, "Bu e-posta adresine ait bir kullanıcı bulunamadı.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})


# accounts/views.py (ek olarak)

from django.utils import timezone
from datetime import timedelta

def password_reset_verify_view(request):
    if request.method == 'POST':
        form = PasswordResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(email=email)
                reset_entry = PasswordResetCode.objects.filter(
                    user=user,
                    code=code,
                    created_at__gte=timezone.now() - timedelta(minutes=15)  # 15 dk geçerlilik süresi
                ).latest('created_at')

                # Kod doğruysa, session'a kullanıcıyı geçici olarak kaydedelim
                request.session['password_reset_user_id'] = user.id
                return redirect('password_reset_confirm')

            except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
                messages.error(request, "Kod geçersiz veya süresi dolmuş.")
    else:
        form = PasswordResetCodeForm()
    return render(request, 'accounts/password_reset_verify.html', {'form': form})




def password_reset_confirm_view(request):
    user_id = request.session.get('password_reset_user_id')
    if not user_id:
        return redirect('password_reset_request')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()

            del request.session['password_reset_user_id']
            messages.success(request, "Şifreniz başarıyla güncellendi.")
            return redirect('login')
    else:
        form = SetNewPasswordForm()
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


