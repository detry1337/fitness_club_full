from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member, Membership, Booking, Service
from django.utils import timezone

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone', 'birth_date']

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['name', 'price', 'duration_days', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['phone', 'birth_date', 'photo', 'membership']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }