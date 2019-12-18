"""
Forms.
"""
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

CRITERIA = [
    ('name', 'name'),
    ('email', 'email'),
    ('all', 'all')
]

class PizzaForm(forms.Form):
    """
    Class PizzaForm.
    """
    type = forms.CharField(label="", max_length=30, required=False)
    size = forms.ChoiceField(required=False, choices=SIZES)

    def __init__(self, pizza=None, *args, **kwargs):
        super(PizzaForm, self).__init__(*args, **kwargs)
        if pizza:
            self.fields['type'].initial = pizza.type
            self.fields['type'].widget.attrs['readonly'] = True
            if pizza.type == 'Margherita':
                self.fields['size'].choices = MARGHERITA_SIZES

class AuthenticationForm(forms.Form):
    """
    Class AuthenticationForm.
    """
    username = forms.CharField(label="", max_length=30, required=False)

class CreateCustomerForm(ModelForm):
    """
    Class CreateCustomerForm.
    """
    def __init__(self, *args, **kwargs):
        super(CreateCustomerForm, self).__init__(*args, **kwargs)

    class Meta:
        """
        Class Meta.
        """
        model = Customer
        fields = ['username', 'name', 'email', 'telephone']

class FilterOrderForm(forms.Form):
    """
    Class FilterOrderForm.
    """
    key_word = forms.CharField(label="", max_length=30, required=False)
    criteria = forms.ChoiceField(required=False, choices=CRITERIA)
