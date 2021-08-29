from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem



class OrderList(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=2)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = self.request.user.basket.select_related() \
                .order_by("product__category")
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order,
                                                       OrderItem,
                                                       form=OrderItemForm,
                                                       extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    print(basket_items[num].product)
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        data['title'] = 'создание заказа'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            # Delete items in basket after order creating only
            Basket.objects.filter(user=self.request.user).delete()

        # удаляем пустой заказ
        print(self.object.get_summary()['total_cost'])
        if self.object.get_summary()['total_cost'] == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderRead(LoginRequiredMixin, DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'просмотр заказа'
        return context


class OrderItemsUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    class Meta:
        abstract = True

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
        print(self.object.get_summary()['total_cost'])
        if self.object.get_summary()['total_cost'] == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

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


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.AWAITING_PAYMENT
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))

def order_payment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.PAID
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


@receiver(pre_save , sender=OrderItem)
@receiver(pre_save , sender=Basket)
def product_quantity_update_save(instance, sender, **kwargs):
    if instance.pk:
        instance.product.quantity = F("quantity") - (instance.quantity - sender.get_item(instance.pk).quantity)
    else:
        instance.product.quantity = F("quantity") - instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()

def get_product_price(request, pk):
   if request.is_ajax():
       product = Product.objects.get(pk=int(pk))
       if product:
           return JsonResponse({'price': product.price})
       else:
           return JsonResponse({'price': 0})
