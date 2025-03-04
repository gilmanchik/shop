from django.db import models

from goods.models import Products
from users.models import User


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.product_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, verbose_name='Пользователь', blank=True, null=True, default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=32, verbose_name='Статус заказа', default='В обработке')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Products, on_delete=models.SET_DEFAULT, verbose_name='Продукт', default=None, null=True)
    name = models.CharField(max_length=32, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f'Товар {self.product} | Заказ № {self.order.pk}'
