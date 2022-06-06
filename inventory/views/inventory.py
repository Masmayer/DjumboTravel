import logging
from django.views.generic import ListView, View, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from customauth.models import User
from inventory.models import (
    Attendants, Orders, Notifications, Planes, OrderLine, PlaneStock, Base
)
from inventory.forms import OrderForm, OrderLineFormSet

logger = logging.getLogger(__name__)


class PlaneListView(LoginRequiredMixin, View):
    template_name = 'inventory/plane_list.html'
    login_url = 'customauth:login'

    def get(self, request, *args, **kwargs):
        try:
            planes = Attendants.objects.get(user_id=request.user).plane_id
        except Attendants.DoesNotExist:
            planes = Attendants.objects.none()
        context = {
            'planes': planes
        }
        return render(request, self.template_name, context)


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'inventory/order_list.html'
    login_url = 'customauth:login'
    model = Orders


class OrderView(LoginRequiredMixin, View):
    template_name = 'inventory/order.html'
    login_url = 'customauth:login'
    model = Orders

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class StockOrderView(LoginRequiredMixin, View):
    template_name = 'inventory/stock_order.html'
    login_url = 'customauth:login'
    model = Orders

    def get(self, request, *args, **kwargs):
        plane = Planes.objects.get(pk=self.kwargs['pk'])
        bases = Base.objects.all()
        context = {
            'plane': plane,
            'bases': bases,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        plane = Planes.objects.get(pk=self.kwargs['pk'])
        base_id = request.POST.get('base')
        date = request.POST.get('date')
        base = Base.objects.get(pk=base_id)
        order = Orders.objects.create(
            attendant_id=request.user.attendants,
            base=base,
            date=date,
        )
        for stock in plane.planestock.all():
            quantity = request.POST.get(f'{stock.id}_quantity')
            print(quantity)
            if quantity:
                total_quantity = int(stock.quantity) + int(quantity)
                if stock.maximum_quantity >= total_quantity:
                    OrderLine.objects.create(
                        product_id=stock.product_id,
                        order_id=order,
                        quantity=quantity,
                    )
                else:
                    messages.error(
                        request,
                        f'{stock.product_id} is exceeded the max stock'
                    )
                    Orders.objects.get(pk=order.pk).delete()
                    return redirect(reverse_lazy(
                        'inventory:order', kwargs={'pk': plane.pk}
                    ))
        for provider in base.providers_base.all():
            Notifications.objects.create(
                user_id=provider.user_id,
                order_id=order.pk,
                description=f'New Order added by {self.request.user.name}'
            )
        return redirect('inventory:order_details', pk=order.pk)


class OrderCreateView(LoginRequiredMixin, CreateView):
    """ Order create view """
    template_name = "inventory/order.html"
    login_url = 'customauth:login'
    model = Orders
    form_class = OrderForm
    formset_class = OrderLineFormSet

    def get_context_data(self, **kwargs):
        assert self.formset_class is not None, "No formset class specified"
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['line_formset'] = self.formset_class(
                self.request.POST, instance=self.object
            )
        else:
            context['line_formset'] = self.formset_class(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        line_formset = context['line_formset']
        if not line_formset.is_valid():
            return super().form_invalid(form)
        self.object = form.save()
        attendant = Attendants.objects.get(user_id=self.request.user)
        self.object.attendant_id = attendant
        self.object.save()
        line_formset.instance = self.object
        # line_formset.order_id = self.object
        line_formset.save()
        providers = User.objects.filter(user_type='provider')
        for provider in providers:
            Notifications.objects.create(
                user_id=provider,
                order_id=self.object.pk,
                description=f'New Order added by {self.request.user.name}'
            )
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, 'Order has been created successfully!'
        )
        logger.debug(f'Order was created for {self.object}')
        return reverse_lazy(
            "inventory:order_list"
        )

    def error_url(self):
        messages.success(
            self.request, 'Invalid Data, Please try again!'
        )
        logger.debug(f'Order was created for {self.object}')
        return reverse_lazy("inventory:order_list")


class OrderDetailView(LoginRequiredMixin, DetailView):
    """ Order details view """
    model = Orders
    template_name = 'inventory/order_details.html'
    login_url = 'customauth:login'


class FillOrderView(LoginRequiredMixin, View):
    """ Order details view """
    model = Orders
    template_name = 'inventory/fill_order.html'
    login_url = 'customauth:login'

    def get(self, request, *args, **kwargs):
        order = Orders.objects.get(pk=self.kwargs['pk'])
        context = {
            'object': order
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        order = Orders.objects.get(pk=self.kwargs['pk'])
        for product in order.orderline.all():
            quantity = request.POST.get(f'{product.id}_quantity')
            if quantity:
                total_quantity = int(product.fill_quantity) + int(quantity)
                if product.quantity >= total_quantity:
                    product.fill_quantity = int(product.fill_quantity) + int(quantity)  # noqa
                    product.save()
                    stock = PlaneStock.objects.get(
                        product_id=product.product_id,
                    )
                    stock.quantity += int(quantity)
                    stock.save()
                else:
                    messages.error(
                        self.request, 'Not enough quantity for this product!'
                    )
        order.providers = self.request.user.providers
        order.save()
        status = 'fill'
        for line in order.orderline.all():
            if line.quantity != line.fill_quantity:
                status = 'not filled'
                break
        if status == 'fill':
            Notifications.objects.create(
                user_id=order.attendant_id.user_id,
                description="Your order has been filled",
                order_id=order.pk,
            )
        context = {
            'object': order
        }
        return render(request, self.template_name, context)


class ChangePlaneStatusView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        plane = Planes.objects.get(pk=self.kwargs['pk'])
        if plane.status == 'air':
            plane.status = 'land'
        else:
            plane.status = 'air'
        plane.save()
        return redirect('inventory:plane_list')
