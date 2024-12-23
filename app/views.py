"""
Definition of views.
"""

from datetime import datetime
from itertools import product
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import ReviewForm
from .forms import BlogForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem, Product 

from django.views.decorators.http import require_POST
from django.urls import reverse

from django.db import models 
from .models import Blog, OrderItem
from .models import Comment, Order
from .forms import CommentForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Основная информация',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request, 
        'app/links.html',
        {
            'title': 'Полезные ссылки:',
            'year': datetime.now().year,
        }
     )

def review(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    data = None
    rating = {'1': 'Ужасно',
              '2': 'Плохо',
              '3': 'Нормально',
              '4': 'Неплохо',
              '5': 'Хорошо'
    }

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['rating'] = rating[ form.cleaned_data['rating'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = ReviewForm()

    return render(
        request,
        'app/review.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""

    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False  # запрещен вход в админ. раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации

            regform.save()  # сохраняем изменения после добавления полей

            return redirect('home')  # переадресация на главную страницу после авторизации
        else:
            return render(
                request,
                'app/registration.html',
                {
                    'regform': regform,
                    'year': datetime.now().year,
                }
            )
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных
        return render(
            request,
            'app/registration.html',
            {
                'regform': regform,
                'year': datetime.now().year,
            }
        )

def blog(request):
    """Renders the blog page"""
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Новости',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr): 
    """Renders the blogpost page"""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()

            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()  # Инициализация формы для GET-запросов

    return render(
        request, 
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
       request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',

            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )

def product_list(request):

    products = Product.objects.all()

    return render(request, 'app/products_list.html', {
        'products': products,
        'year': datetime.now().year,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('product_list')

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'app/cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})
 
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(user=request.user, total_price=total_price)
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

    cart_items.delete()
    return render(request, 'app/checkout_success.html')

@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_price = sum(order.total_price for order in orders)
    order_count = orders.count()  # Подсчет общего количества заказов
    return render(request, 'app/my_orders.html', {
        'orders': orders,
        'total_price': total_price,
        'order_count': order_count,  # Передача общего количества заказов в контекст
    })


@user_passes_test(lambda u: u.is_staff)
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    total_price = sum(order.total_price for order in orders)
    return render(request, 'app/all_orders.html', {
        'orders': orders,
        'total_price': total_price,
    })

@user_passes_test(lambda u: u.is_staff)
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect(reverse('all_orders'))
    return render(request, 'app/all_orders.html')
