from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Request, Correspondence
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('organization_title',)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('organization_title',)


class UserRegisterForm(forms.Form):

    tp_key = forms.CharField(max_length=6, label="Ключ ТП")
    first_name = forms.CharField(max_length=150, label="Имя")
    last_name = forms.CharField(max_length=150, label="Фамилия")
    email = forms.EmailField(label="Почта")
    username = forms.CharField(max_length=150, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput())


class RequestCreationForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['product', 'problem']


class MessageSendForm(forms.ModelForm):
    class Meta:
        model = Correspondence
        fields = ['answer']
