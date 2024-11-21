from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'name', 'role', 'is_active', 'is_staff', 'is_superuser')

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'name', 'role', 'is_active', 'is_staff', 'is_superuser')
