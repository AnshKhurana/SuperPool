from django import forms
from pool.models import Service, TravelService, FoodService, ShoppingService, Category

class ServiceCreationForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Category

    categories = forms.ModelChoiceField(queryset=Category.objects.values_list('name').order_by('name'))

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


