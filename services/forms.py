from django import forms
from pool.models import Service, TravelService, FoodService, ShoppingService, Category, ServiceMember, Group
from django.utils.dateparse import parse_duration
from django.forms import ValidationError
from dal import autocomplete

CAT_CHOICES = [
    ('food', 'Oranges'),
    ('travel', 'Cantaloupes'),
]


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class DurationInput(forms.widgets.TextInput):

    def _format_value(self, value):
        duration = parse_duration(value)

        seconds = duration.seconds

        days = seconds // 86400
        remaining_seconds = seconds % 86400
        minutes = remaining_seconds // 60
        seconds = seconds % 60
        minutes = minutes % 60

        return '{:02d} days:{:02d}:{:02d}'.format(days, minutes, seconds)


class newFoodCreationForm(forms.ModelForm):
    class Meta:
        model = FoodService
        fields = ("start_time", "end_time", "slackness", "description", "vendor")
        widgets = {
            'vendor': autocomplete.ModelSelect2(
                url='services/food-autocomplete',
                attrs={
                    'data-placeholder': 'Vendors ...',
                    'data-minimum-input-length': 1,
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput()
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput()
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["slackness"].widget = DurationInput()
        self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

    def clean(self):
        super(newFoodCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime > etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        vendor = self.cleaned_data['vendor']

        return {'start_time': start_time, 'end_time': end_time, 'slackness': slackness, 'description': description,
                'vendor': vendor}


class TravelCreationForm(forms.ModelForm):
    class Meta:
        model = TravelService
        fields = ("start_point", "end_point", "start_time", "end_time", "slackness", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput()
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput()
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["slackness"].widget = DurationInput()
        self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

    def clean(self):
        super(TravelCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime > etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_point = self.cleaned_data['start_point']
        end_point = self.cleaned_data['end_point']
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']

        return {'start_point': start_point, 'end_point': end_point, 'start_time': start_time, 'end_time': end_time,
                'slackness': slackness, 'description': description}


class ShoppingCreationForm(forms.ModelForm):
    class Meta:
        model = ShoppingService
        fields = ("start_time", "end_time", "slackness", "description", "vendor")
        widgets = {
            'vendor': autocomplete.ModelSelect2(
                url='services/shopping-autocomplete',
                attrs={
                    'data-placeholder': 'Vendors ...',
                    'data-minimum-input-length': 1,
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput()
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput()
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["slackness"].widget = DurationInput()
        self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

    def clean(self):
        super(ShoppingCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime > etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        vendor = self.cleaned_data['vendor']

        return {'start_time': start_time, 'end_time': end_time, 'slackness': slackness, 'description': description,
                'vendor': vendor}

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

# class FoodCreationForm(forms.Form):
#
#     # start_time = forms.DateTimeField(required=False, input_formats=['%d/%m/%Y %H:%M'],
#     #     widget=forms.DateTimeInput(attrs={
#     #         'class': 'form-control datetimepicker-input',
#     #         'data-target': '#datetimepicker1'
#     #     }))
#
#     start_time = forms.DateTimeField(required=False)
#     end_time = forms.DateTimeField(required=False)
#     slackness = forms.DurationField()
#     description = forms.CharField(max_length=1000)  # this is a general description
#     restaurant = forms.CharField(max_length=1000)
#
#     def clean(self):
#         super(FoodCreationForm, self).clean()
#         stime = self.cleaned_data.get('start_time')
#         etime = self.cleaned_data.get('end_time')
#         if (stime is not None) and (etime is not None) and stime>etime:
#             raise ValidationError('Start time after end time')
#
#     def save(self, u):
#         start_time = self.cleaned_data['start_time']
#         end_time = self.cleaned_data['end_time']
#         slackness = self.cleaned_data['slackness']
#         description = self.cleaned_data['description']
#         vendor = self.cleaned_data['restaurant']
#         f= FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=vendor, description=description, start_time=start_time, end_time=end_time, slackness=slackness, stype='Food')
#         f.save()
#         sm= ServiceMember(service=f, user=u)
#         sm.save()

class GroupSelectForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Group.objects.all()
    )
    def __init__(self, *args, **kwargs):
        currentuser = kwargs.pop('currentuser')
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.filter(members=currentuser).all()



