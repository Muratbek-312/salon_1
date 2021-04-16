from django import forms
from django.contrib.auth import get_user_model

from .utils import send_activation_mail
from profiles.models import CustomerProfile, MasterProfile

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput, label='Пароль')
    password_confirmation = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput, label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ('email', 'nik_name', 'password', 'password_confirmation', 'status')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже есть')
        return email

    def clean_name(self):
        nik_name = self.cleaned_data.get('nik_name')
        if User.objects.filter(nik_name=nik_name).exists():
            raise forms.ValidationError('Пользователь с таким email уже есть')
        return nik_name

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirmation = data.pop('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError('Пароли не совпадают')
        return data

    def save(self, commit=True):
        user = User.objects.create(**self.cleaned_data)
        if user.status == "CS":
            CustomerProfile.objects.create(user=user, email=user.email)
        else:
            MasterProfile.objects.create(user=user, email=user.email)
        send_activation_mail(user)
        return user
