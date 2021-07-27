from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import DeleteView

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
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
        self.object.is_deleted = True
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
        self.object.is_deleted = True
        self.object.save()
        prod_to_del = Product.objects.filter(category__pk=self.object.pk)
        for product in prod_to_del:
            product.is_deleted = True
            product.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
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
            objects_list = Product.objects.all().order_by('is_deleted', 'name')

        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            title = f'Товары категории {category.name}'
            objects_list = Product.objects \
                .filter(category__pk=pk) \
                .order_by('is_deleted', 'name')

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
        self.object.is_deleted = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name

        return context
