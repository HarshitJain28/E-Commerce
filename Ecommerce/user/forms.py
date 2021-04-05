from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User
from django.db import transaction

class UserRegisterationForm(UserCreationForm):
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    state = forms.CharField(required=True)
    city = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number',
                  'address', 'city', 'state', 'zipcode', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        profile = Profile.objects.create(user=user)
        profile.phone_number = self.cleaned_data.get('phone_number')
        profile.address = self.cleaned_data.get('address')
        profile.state = self.cleaned_data.get('state')
        profile.city = self.cleaned_data.get('city')
        profile.zipcode = self.cleaned_data.get('zipcode')
        profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField()
    address = forms.CharField() 
    state = forms.CharField() 
    city = forms.CharField()

    class Meta:
        model = Profile
        fields = ['phone_number','address','state','city', 'zipcode']

