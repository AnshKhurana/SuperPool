from django import forms

from pool.models import FoodService, Group
from accounts.models import User
import random


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

    def save(self, commit=True):
        # user = super(UserCreationForm, self).save(commit=False)
        group = Group()
        hash = random.getrandbits(32)
        group.name = self.cleaned_data['name']
        group.description = self.cleaned_data['description']
        group.hash = hash
        if commit:
            group.save()
        return group
