"""
Forms.
"""
from django import forms
from django.forms import ModelForm
from .models import Customer
import re

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

    def clean(self):
        cleaned_data = super().clean()
        if not Customer.objects.filter(username=cleaned_data.get('username')):
            self.add_error('username', "Username doesn\'t exist.")

class CreateCustomerForm(ModelForm):
    """
    Class CreateCustomerForm.
    """
    def __init__(self, *args, **kwargs):
        super(CreateCustomerForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pattern_mail = re.compile("[^@]+@[^@]+\.[^@]+")
        pattern_phone = re.compile("(\d{3}\d{3}\d{4})")

        if not pattern_mail.match(cleaned_data.get('email')):
            self.add_error('email', "Email invalide.")

        if not pattern_phone.match(cleaned_data.get("telephone")):
            self.add_error('telephone', 'Phone number invalide.')

        if len(cleaned_data.get('username')) < 2:
            self.add_error('username', 'Username must contains at least 2 characters.')

        if len(cleaned_data.get('name')) < 2:
            self.add_error('name', 'The name must contain at least 2 characters.')

        if Customer.objects.filter(username=cleaned_data.get('username')).exists():
            self.add_error('username', "This username is already used.")

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
