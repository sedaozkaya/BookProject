from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail

from BookProject.settings import DEFAULT_FROM_EMAIL
from .models import PasswordResetCode
from .forms import PasswordResetRequestForm, PasswordResetCodeForm, SetNewPasswordForm
from django.contrib import messages
from .forms import ConfirmPasswordForm

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
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, "E-posta adresinize bir kod gönderildi.")

                return redirect('password_reset_verify')
            except User.DoesNotExist:
                messages.error(request, "Bu e-posta adresine ait bir kullanıcı bulunamadı.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})




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
                    created_at__gte=timezone.now() - timedelta(minutes=15)
                ).latest('created_at')


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


@login_required
def delete_account(request):
    user = request.user

    if request.method == 'POST':
        form = ConfirmPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if user.check_password(password):
                email = user.email
                username = user.username
                user.delete()

                send_mail(
                    subject='BookLoop Hesabınız Silindi',
                    message=f'Merhaba {username},\n\nBookLoop hesabınız başarıyla silinmiştir.',
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, 'Hesabınız silindi. E-posta ile bilgilendirme yapıldı.')
                return redirect('home')
            else:
                messages.error(request, 'Şifreniz yanlış.')
    else:
        form = ConfirmPasswordForm()

    return render(request, 'accounts/delete_account.html', {'form': form})