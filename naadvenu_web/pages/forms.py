from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from .models import Student

class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'level': forms.Select(choices=Student.LEVEL_CHOICES),
            'account_status': forms.Select(choices=Student.ACCOUNT_STATUS_CHOICES),
        }
