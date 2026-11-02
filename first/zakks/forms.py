from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Zakk, Comment

class ZakkForm(forms.ModelForm):
    class Meta:
        model = Zakk
        # Указываем, какие поля пользователь заполняет сам.
        # Юзера и дату Django подставит автоматически, поэтому берем только title и content.
        fields = ['title', 'content', 'theme']

        # Красиво оформляем поля (добавляем подсказки)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок'}),
            'content': forms.Textarea(attrs={'placeholder': 'Напишите свой закк!'})

        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль (минимум 8 символов)'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}),
        }



# Не нужна форма комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={
                'placeholder': 'Написать комментарий...',
                'rows': 2,
                'class': 'comment-input',
            }),
        }
        labels = {
            'text': '',
        }
