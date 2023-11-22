
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Post, Notice

from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="이메일",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    username = forms.CharField(
        max_length=30,
        label="닉네임",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    name = forms.CharField(
        max_length=40,
        label="이름",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    major = forms.CharField(
        max_length=120,
        label="전공",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    university = forms.CharField(
        max_length=120,
        label="대학교",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'major', 'university', 'password1', 'password2')
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="이메일",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

#게시판 입력 폼
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']