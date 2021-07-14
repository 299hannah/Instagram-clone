from django import forms
from .models import Post, Profile
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'pub_date']
        widgets ={
            'tags':forms.CheckboxSelectMultiple(),
        }

class LoginForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture','profile_info']


class EditProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    nick_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=True)
    profile_info = forms.CharField(widget=forms.TextInput(), max_length=260, required=True)
    class Meta:
        model = Profile
        fields = ('picture', 'nick_name',  'profile_info')

    








