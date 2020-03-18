from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm, UsernameField

from django import forms

from pool.models import FoodService, FoodVendor, Group, User


class FoodServiceForm(autocomplete.FutureModelForm):
    # vendor = forms.ModelChoiceField(
    #     required=True,
    #     queryset=FoodVendor.objects.all(),
    #     widget=autocomplete.ModelSelect2Multiple(url='food-autocomplete')
    # )

    class Meta:
        model = FoodService
        fields = '__all__'
        widgets = {
            'vendor': autocomplete.ModelSelect2(
                url='food-autocomplete',
                attrs={
                    'data-placeholder': 'Autocomplete ...',
                    'data-minimum-input-length': 1,
                },
            )
        }


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def save(self, commit=True):
        # user = super(UserCreationForm, self).save(commit=False)
        group = Group()
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        group.name = self.cleaned_data['name']
        print(group.name)
        member = User.objects.filter(name=self.cleaned_data['members'][0])
        print(member)
        if commit:
            group.save()
        for q in member:
            group.members.add(q)
        print('Saved')
        return group
