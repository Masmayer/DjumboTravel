from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from inventory.models import Planes, Orders, Attendants, Providers


class DashboardView(LoginRequiredMixin, View):
    """ Dashboard view """
    template_name = 'dashboard/dashboard.html'
    login_url = 'customauth:login'

    def get(self, request):
        context = {
            'plane': Planes.objects.all().count(),
            'planes': Planes.objects.all(),
            'order': Orders.objects.all().count(),
            'attendant': Attendants.objects.all().count(),
            'provider': Providers.objects.all().count(),
        }
        return render(request, self.template_name, context)
