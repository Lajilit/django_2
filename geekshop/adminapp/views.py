from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import DeleteView

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem
from ordersapp.views import OrderItemsUpdate
from .forms import ShopUserAdminEditForm, ProductCategoryEditForm, \
    ProductEditForm, ShopUserAdminRegisterForm


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    context_object_name = 'objects'
    template_name = 'adminapp/shopuser_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи'

        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    form_class = ShopUserAdminRegisterForm
    template_name = 'adminapp/shopuser_form.html'
    success_url = reverse_lazy('admin_panel:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'создание нового пользователя'

        return context


# class PasswordChangeForm - изучить, как менять пароль пользователям


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/shopuser_form.html'
    success_url = reverse_lazy('admin_panel:users')
    form_class = ShopUserAdminEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = \
            f'редактирование данных пользователя {self.object.username}'

        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/shopuser_delete.html'
    success_url = reverse_lazy('admin_panel:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'удаление пользователя'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductCategoryListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    context_object_name = 'objects'
    template_name = 'adminapp/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории товаров'

        return context


class ProductCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('admin_panel:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'создание новой категории товаров'

        return context


class ProductCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_form.html'

    def get_success_url(self, **kwargs):
        pk = self.object.pk
        return reverse('admin_panel:category_update', args=[pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование категории товаров '

        return context


class ProductCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_panel:categories')

    def get_context_data(self, **kwargs):
        pk = self.object.pk
        context = super().get_context_data(**kwargs)
        context['title'] = 'удаление категории товаров'
        context['prod_to_del'] = Product.objects.filter(category__pk=pk)

        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        prod_to_del = Product.objects.filter(category__pk=self.object.pk)
        for product in prod_to_del:
            product.is_active = False
            product.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'adminapp/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        if pk == 0:
            title = 'Все товары'
            category = {
                'name': 'все',
                'pk': pk
            }
            objects_list = Product.objects.all().order_by('-is_active', 'name')

        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            title = f'Товары категории {category.name}'
            objects_list = Product.objects \
                .filter(category__pk=pk) \
                .order_by('-is_active', 'name')

        context['category'] = category
        context['object_list'] = objects_list
        context['title'] = title
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # category - it's the name of the field on your current form
        # self.args will be filled from URL. I'd suggest to use named parameters
        # so you can access e.g. self.kwargs['pk']
        initial['category'] = self.kwargs['pk']
        return initial

    def get_success_url(self, **kwargs):
        pk = self.object.category.pk
        return reverse('admin_panel:products', args=[pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        if pk == 0:
            category = {
                'name': 'все',
                'pk': pk
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
        context['title'] = 'создание нового товара'
        context['category'] = category

        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_form.html'

    def get_success_url(self, **kwargs):
        pk = self.object.category.pk
        return reverse('admin_panel:product_update', args=[pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.category.pk
        context['title'] = 'редактирование товара '
        context['category'] = get_object_or_404(ProductCategory, pk=pk)

        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self, **kwargs):
        pk = self.object.category.pk
        return reverse('admin_panel:products', args=[pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'удаление товара'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name

        return context


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'adminapp/order_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        if pk == 0:
            title = 'Все заказы'
            user = {
                'username': 'все',
                'pk': pk
            }
            objects_list = Order.objects.all().select_related().order_by('-is_active', '-id')

        else:
            user = get_object_or_404(ShopUser, pk=pk)
            title = f'Заказы пользователя {user.username}'
            objects_list = Order.objects \
                .filter(user__pk=pk) \
                .order_by('-is_active', 'id') \
                .select_related()

        context['user'] = user
        context['object_list'] = objects_list
        context['title'] = title
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'adminapp/order_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Заказ № {self.object.id} пользователя {self.object.user.username}'

        return context


class OrderItemsUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    template_name = 'adminapp/order_form.html'

    def get_success_url(self, **kwargs):
        return reverse('admin_panel:orders_list', args=[0])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST,
                                     instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        context['title'] = 'редактирование заказа'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_summary()['total_cost'] == 0:
            self.object.is_active = False
            self.object.status = Order.CANCEL
            self.object.save()

        return super().form_valid(form)



class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order

    template_name = 'adminapp/order_delete.html'

    def get_success_url(self, **kwargs):
        return reverse('admin_panel:orders_list', args=[0])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'удаление заказа'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.status = Order.CANCEL
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())



def order_collect(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.PROCEEDED
    order.save()
    user = order.user.pk

    return HttpResponseRedirect(reverse('admin_panel:orders_list', args=[user]))

def order_send(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.READY
    order.save()
    user = order.user.pk

    return HttpResponseRedirect(reverse('admin_panel:orders_list', args=[user]))