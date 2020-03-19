from django import forms
from pool.models import Service, TravelService, FoodService, ShoppingService, Category




CAT_CHOICES= [
    ('food', 'Oranges'),
    ('travel', 'Cantaloupes'),
    ]



class ServiceCreationForm(forms.Form):

    # class Meta:
    #     fields = ('name',)
    #     model = Category

    categories = forms.ModelChoiceField(queryset=Category.objects.values_list('name').order_by('name'))

    # choice = forms.CharField(label='Choose category', widget=forms.Select(choices=Category.objects.values_list('name').order_by('name')))
    choice = forms.CharField(label='Choose category',
                             widget=forms.Select(choices=CAT_CHOICES))

    def clean(self):
        cleaned_data = super(ServiceCreationForm, self).clean()
        categories = cleaned_data.get('categories')
        if not categories:
            raise forms.ValidationError('some error!')
    # self.fields['category'].widget.attrs.update({'placeholder': 'Choose Username'})

    # class Meta:
    #     model = Service
        # fields = ("username",
        #           "email",
        #           "phone_number",
        #           "address",
        #           "password1",
        #           "password2")


