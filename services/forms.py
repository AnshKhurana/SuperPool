from django import forms
from pool.models import Service, TravelService, FoodService, ShoppingService, Category, ServiceMember
from django.forms import ValidationError

CAT_CHOICES= [
    ('food', 'Oranges'),
    ('travel', 'Cantaloupes'),
    ]


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class FoodCreationForm(forms.Form):

    # start_time = forms.DateTimeField(required=False, input_formats=['%d/%m/%Y %H:%M'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker1'
    #     }))

    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)
    slackness = forms.DurationField()
    description = forms.CharField(max_length=1000)  # this is a general description
    restaurant = forms.CharField(max_length=1000)

    def clean(self):
        super(FoodCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime>etime:
            raise ValidationError('Start time after end time')

    def save(self, u):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        vendor = self.cleaned_data['restaurant']
        f= FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=vendor, description=description, start_time=start_time, end_time=end_time, slackness=slackness, stype='Food')
        f.save()
        sm= ServiceMember(service=f, user=u)
        sm.save()


class newFoodCreationForm(forms.ModelForm):
    class Meta:
        model = FoodService
        fields = ("start_time", "end_time", "slackness", "description", "vendor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput()
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput()
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

    def clean(self):
        super(newFoodCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime>etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        vendor = self.cleaned_data['vendor']

        return {'start_time': start_time, 'end_time' : end_time, 'slackness': slackness, 'description': description, 'vendor': vendor}

        # f=FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=vendor, description=description, start_time=start_time, end_time=end_time, slackness=slackness, stype='Food')
        # f.save()
        # sm=ServiceMember(service=f, user=u)
        # sm.save()


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


