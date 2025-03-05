from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from carts.models import Cart
from .forms import CreatedOrderForm
from .models import Order, OrderItem


def create_order(request):
    if request.method == 'POST':
        form = CreatedOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=request.user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get']
                        )

                        for cart_item in cart_items:
                            product = cart_item.products
                            name = cart_item.products.name
                            price = cart_item.products.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе'
                                                      f'В наличии {product.quantity}')
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity
                            )
                            product.quantity -= quantity
                            product.save()
                        cart_items.delete()
                        messages.success(request, 'Заказ оформлен')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }
        form = CreatedOrderForm(initial=initial)
    context = {
        'title': 'Оформление заказа',
        'form': form
    }
    return render(request, 'orders/create_order.html', context)
