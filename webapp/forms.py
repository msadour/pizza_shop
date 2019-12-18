from django import forms
from django.forms import ModelForm
from .models import Customer

SIZES = [
    ('Large', 'Large'),
    ('Medium', 'Medium'),
    ('Small', 'Small'),
]

MARGHERITA_SIZES = [
    ('Large', 'Large'),
    ('Medium', 'Medium')
]

class PizzaForm(forms.Form):
    type = forms.CharField(label="", max_length=30, required=False)
    size = forms.ChoiceField( required=False, choices=SIZES)

    def __init__(self, pizza, *args, **kwargs):
        super(PizzaForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = 'pizza'
        if pizza == 'margherita':
            self.fields['size'].attrs['choices'] = MARGHERITA_SIZES

class AuthenticationForm(forms.Form):
    username = forms.CharField(label="", max_length=30, required=False)

class CreateCustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateCustomerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Customer
        fields = ['username', 'name', 'email', 'telephone']
