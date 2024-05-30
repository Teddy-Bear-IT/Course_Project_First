from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import User, Feedback, ReviewUser, OrderStatus

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'id':'form3Example3',
        'class': "form-control form-control-lg",
        'placeholder': 'Ввведите ваш логин'
    }))

    password = forms.CharField(widget=forms.HiddenInput(attrs={
        'type': 'password',
        'id': 'form3Example4',
        'class': "form-control form-control-lg",
        'placeholder': 'Ввведите ваш пароль'
    }))
    class Meta:
        model = User
        fields = ('username','password')

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'id':'form3Example3',
        'class': "form-control form-control-lg",
        'placeholder': 'Введите ваш логин'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'id':'form3Example3',
        'class': "form-control form-control-lg",
        'placeholder': 'Введите вашу почту'
    }))
    password = forms.CharField(widget=forms.HiddenInput(attrs={
        'type': 'password',
        'id': 'form3Example4',
        'class': "form-control form-control-lg",
        'placeholder': 'Введите ваш пароль'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'id': 'form3Example5',
        'class': "form-control form-control-lg",
        'placeholder': 'Введите ваше имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'id': 'form3Example5',
        'class': "form-control form-control-lg",
        'placeholder': 'Введите вашу фамилию'
    }))
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email')

class FeedBackForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': "form-control mb-3",
        'placeholder': 'Введите вашу почту'
    }))

    user_request_data = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Опишите кратко запрос'
    }))

    class Meta:
        model = Feedback
        fields = ('email', 'user_request_data')

class ReviewForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': "form-control",
        'placeholder': 'Введите ваш отзыв'
    }))

    class Meta:
        model = ReviewUser
        fields = ('description',)

class OrderStatusForm(forms.ModelForm):
    choices = reversed(OrderStatus.objects.values_list('pk', 'name_status'))
    name_status = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    class Meta:
        model = ReviewUser
        fields = ('name_status',)