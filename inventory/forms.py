from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper

from inventory.models import Orders, OrderLine


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Orders
        fields = ['base', 'date']

        widgets = {
            'base': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Base'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }


class OrderLineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = OrderLine
        fields = ['product_id', 'quantity']

        widgets = {
            'product_id': forms.Select(attrs={
                'class': 'form-control',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity'
            })
        }


OrderLineFormSet = inlineformset_factory(
    Orders, OrderLine, form=OrderLineForm, min_num=1,
    extra=0, can_delete=True
)
