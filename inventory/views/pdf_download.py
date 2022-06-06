# importing the necessary libraries
from io import BytesIO
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from xhtml2pdf import pisa

from inventory.models import Orders


# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Creating a class based view
class OrderPDFView(LoginRequiredMixin, View):
    login_url = 'customauth:login'

    def get(self, request, *args, **kwargs):
        order = Orders.objects.filter(pk=self.kwargs['pk'])
        context = {
            'orders': order,
        }
        # getting the template
        pdf = html_to_pdf('inventory/order_pdf.html', context)
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


class OrderListPDFView(LoginRequiredMixin, View):
    login_url = 'customauth:login'

    def get(self, request, *args, **kwargs):
        date = request.GET.get('download_date')
        order = Orders.objects.filter(date=date)
        context = {
            'orders': order,
        }
        # getting the template
        pdf = html_to_pdf('inventory/order_pdf.html', context)
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
