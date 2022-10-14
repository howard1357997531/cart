from cProfile import label
from django import forms
from .models import Profile, Addressbook
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', ]


class AddressForm(forms.ModelForm):
    first_name = forms.CharField(label='名')
    last_name = forms.CharField(label='姓')
    phone = forms.CharField(label='電話')
    address = forms.CharField(label='地址')
    email = forms.EmailField(label='電子郵件')
    status = forms.BooleanField(label='激活', required=False)

    class Meta:
        model = Addressbook
        fields = '__all__'
        exclude = ['user', ]
