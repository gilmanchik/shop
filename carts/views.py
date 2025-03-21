from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View

from goods.models import Products
from .mixins import CartMixin
from .models import Cart
from .utils import get_user_carts


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)

        cart = self.get_cart(request, products=product)
        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                products=product, quantity=1)
        response_data = {
            'message': 'Товар добавлен',
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


# def cart_add(request):
#     product_id = request.POST.get('product_id')
#     product = Products.objects.get(id=product_id)
#
#     if request.user.is_authenticated:
#         carts = Cart.objects.filter(user=request.user, products=product)
#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(user=request.user, products=product, quantity=1)
#     else:
#         carts = Cart.objects.filter(
#             session_key=request.session.session_key, products=product
#         )
#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(session_key=request.session.session_key, products=product, quantity=1)
#
#     user_cart = get_user_carts(request)
#     cart_items_html = render_to_string('carts/includes/included_cart.html', {'carts': user_cart}, request=request)
#     response_data = {
#         'message': 'Товар добавлен',
#         'cart_items_html': cart_items_html
#     }
#     return JsonResponse(response_data)

class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get('quantity')
        cart.save()

        quantity = cart.quantity

        response_data = {
            'message': 'Количество изменено',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


# def cart_change(request):
#     cart_id = request.POST.get('cart_id')
#     quantity = request.POST.get('quantity')
#
#     cart = Cart.objects.get(id=cart_id)
#
#     cart.quantity = quantity
#     cart.save()
#     update_quantity = cart.quantity
#
#     cart = get_user_carts(request)
#     cart_items_html = render_to_string('carts/includes/included_cart.html', {'carts': cart}, request=request)
#     response_data = {
#         'message': 'Количество изменено',
#         'cart_items_html': cart_items_html,
#         'quaantity': update_quantity
#     }
#     return JsonResponse(response_data)

class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            'message': 'Товар удален',
            'quantity_deleted': quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


# def cart_remove(request):
#     cart_id = request.POST.get('cart_id')
#     cart = Cart.objects.get(id=cart_id)
#     quantity = cart.quantity
#     cart.delete()
#
#     user_cart = get_user_carts(request)
#     cart_items_html = render_to_string('carts/includes/included_cart.html', {'carts': user_cart}, request=request)
#     response_data = {
#         'message': 'Товар удален',
#         'cart_items_html': cart_items_html,
#         'quantity_deleted': quantity
#     }
#     return JsonResponse(response_data)
