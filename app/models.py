"""
Definition of models.
"""
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")

    description = models.TextField(verbose_name="Краткое содержание")

    content = models.TextField(verbose_name="Полное содержание")

    posted = models.DateTimeField(default = datetime.now, db_index=True, verbose_name="Опубликована")

    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")

    image = models.FileField(default = 'temp.jpg', verbose_name="Путь к картинке")

    # методы класса
    def get_absolute_url(self):  # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):  # метод возвращает название, используемое для представления отдельных записей в адм. разделе
        return self.title

    # метаданные - вложенный в класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts"  # имя таблицы для модели
        ordering = ["-posted"]  # порядок сортировки данных в модели ("-" означает убывание)
        verbose_name = "статья блога"  # имя, под которым модель будет отображаться в адм. разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога"  # тоже для всех статей блога

# Регистрация модели в админке
admin.site.register(Blog)

class Comment(models.Model):

    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name="Статья комментария")

    def __str__(self):

        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    class Meta:

        db_table = "Comment"

        ordering = ["-date"]

        verbose_name = "Комментарий к статье блога"

        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(default='', verbose_name="Описание услуги")
    image = models.FileField(default='temp.jpg', verbose_name="Путь к изображению")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")

    def get_absolute_url(self):
        return reverse("product", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Products"
        verbose_name ="услуги"
        verbose_name_plural = "услуга"
admin.site.register(Product)

class Cart(models.Model): # просто карзина
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model): # хранит конкретные товары
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
       return f'Заказ'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

admin.site.register(Order)

class OrderItem(models.Model): # хранит информацио о заказах пользователей 
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderQuerySet(models.QuerySet): # история покупок
    def by_client(self, client):
        return self.filter(client=client)

    def by_status(self, status):
        return self.filter(status=status)

    def recent_orders(self):
        return self.order_by('-order_date')

