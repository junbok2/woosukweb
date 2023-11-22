
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Post, Notice

from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]

    username = forms.CharField(
        max_length=30,
        label="아이디",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        max_length=40,
        label="이름",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    phone_number = forms.CharField(
        max_length=20,
        label="휴대전화번호",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    university = forms.CharField(
        max_length=20,
        label="소속대학",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    major = forms.CharField(
        max_length=20,
        label="학과",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label="이메일",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    gender = forms.ChoiceField(
        label="성별",
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'phone_number', 'email', 'gender', 'university', 'major')
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

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'phone_number', 'email', 'wk_sex']