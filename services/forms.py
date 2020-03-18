from django import forms
from pool.models import Service, TravelService, FoodService, ShoppingService, Category

class ServiceCreationForm(forms.Form):

    categories = forms.ModelChoiceField(queryset=Category.objects.values_list('name').order_by('name'))

    # self.fields['category'].widget.attrs.update({'placeholder': 'Choose Username'})

    class Meta:
        model = Service
        # fields = ("username",
        #           "email",
        #           "phone_number",
        #           "address",
        #           "password1",
        #           "password2")


