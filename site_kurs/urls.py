"""
Definition of urls for site_kurs.
"""

from datetime import datetime
from os import name
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.urls import path

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('links/', views.links, name='links'),
    path('review/', views.review,  name='review'),
    path('registration/', views.registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('products/', views.product_list, name='product_list'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
     path('checkout/', views.checkout, name='checkout'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('all_orders/', views.all_orders, name='all_orders'),
      path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
      path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()