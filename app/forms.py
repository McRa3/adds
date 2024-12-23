"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from django.db import models
from .models import Comment, Product
from .models import Blog

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Введите имя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Введите пароль'}))

class ReviewForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100)
    rating = forms.ChoiceField(label='Оцените качество обслуживания',
                                choices=(('1', 'Ужасно'),
                                ('2', 'Плохо'),
                                ('3', 'Нормально'),
                                ('4', 'Хорошо'),
                                ('5', 'Отлично')), initial=3)
    notice = forms.BooleanField(label='Получать новости на e-mail?',
                                required=False)
    email = forms.EmailField(label='Ваш e-mail', min_length=7, required=False)
    message = forms.CharField(label='Ваш комментарий',
                              widget=forms.Textarea(attrs={'rows':12,'cols':20}), required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image',] 
        labels = {
            'title': "Название",
            'description': "Описание",
            'price': "Цена",
            'image': "Картинка",
        }
