

from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="E-posta adresiniz")



class PasswordResetCodeForm(forms.Form):
    email = forms.EmailField(label="E-posta")
    code = forms.CharField(max_length=6, label="Doğrulama Kodu")



class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="Yeni Şifre")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Şifreyi Onayla")

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        return cleaned_data


# accounts/forms.py

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PasswordResetCodeForm(BootstrapFormMixin, forms.Form):
    email = forms.EmailField(label="E-posta")
    code = forms.CharField(max_length=6, label="Doğrulama Kodu")

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class SetNewPasswordForm(BootstrapFormMixin, forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="Yeni Şifre")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Şifreyi Onayla")

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        return cleaned_data
