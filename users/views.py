from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    # success_url = reverse_lazy('main:index')
    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f'Добрый день {user.username}')

                return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page

        return reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             session_key = request.session.session_key
#
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f'Добрый день {username}')
#                 if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))
#                 return HttpResponseRedirect(reverse('main:home'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'users/login.html', context)

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)
        messages.success(self.request, f'Вы успешно зарегистрировались')
        return HttpResponseRedirect(self.success_url)


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             session_key = request.session.session_key
#
#             user = form.instance
#             auth.login(request, user)
#
#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)
#             messages.success(request, f'Поздравляем с регистрацией {user.username}')
#             return HttpResponseRedirect(reverse('main:home'))
#     else:
#         form = UserRegistrationForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'users/registration.html', context)


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль обновлен')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related('product')
            )
        ).order_by('-id')
        context['orders'] = self.set_get_cache(orders, f'orders_for_user{self.request.user.id}', 60)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Личный кабинет'
    #     orders = cache.get(f'order_for_user_{self.request.user.id}')
    #     if not orders:
    #         context['orders'] = Order.objects.filter(user=self.request.user).prefetch_related(
    #             Prefetch(
    #                 'orderitem_set',
    #                 queryset=OrderItem.objects.select_related('product')
    #             )
    #         ).order_by('-id')
    #         cache.set(f'orders_for_user{self.request.user.id}', orders, 10)
    #     # context['orders'] = orders
    #     return context


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Профиль успешно обновлен')
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = ProfileForm(instance=request.user)
#
#     orders = (
#         Order.objects.filter(user=request.user).prefetch_related(
#             Prefetch(
#                 'orderitem_set',
#                 queryset=OrderItem.objects.select_related('product')
#             )
#         )
#         .order_by('-id')
#     )
#     context = {
#         'title': 'Личный кабинет',
#         'form': form,
#         'orders': orders
#     }
#     return render(request, 'users/profile.html', context)

class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        return context

# def users_cart(request):
#     return render(request, 'users/users_cart.html')


@login_required
def logout(request):
    messages.success(request, f'До свидания {request.user.username}')
    auth.logout(request)
    return redirect(reverse('main:home'))
