from django import forms
from django.urls import reverse_lazy

from pool.models import *
from django.utils.dateparse import parse_duration
from django.forms import ValidationError
from dal import autocomplete
from datetime import datetime, timedelta
from pytz import timezone

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


class FoodCreationForm(autocomplete.FutureModelForm):
    class Meta:
        model = FoodService
        fields = ("start_time", "end_time", "description", "vendor")
        # widgets = {
        #     'vendor': autocomplete.ModelSelect2(
        #         url='services:food-autocomplete',
        #         attrs={
        #             'data-placeholder': 'Vendors ...',
        #             'data-minimum-input-length': 1,
        #         },
        #     )
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput(
            attrs={'value': datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%dT%H:%M")})
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput(attrs={
            'value': (datetime.now().astimezone(timezone('Asia/Kolkata')) + timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M")})
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        # self.fields["slackness"].widget = DurationInput()
        # self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

        # self.fields["vendor"].widget = autocomplete.ListSelect2(
        #         url='services:food-autocomplete',
        #         attrs={
        #             'data-placeholder': 'Vendors ...',
        #             'data-minimum-input-length': 1,
        #         })

    def clean(self):
        super(FoodCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime > etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        # slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        vendor = self.cleaned_data['vendor']

        return {'start_time': start_time, 'end_time': end_time, 'description': description,
                'vendor': vendor}


class ShoppingCreationForm(autocomplete.FutureModelForm):
    class Meta:
        model = ShoppingService
        fields = ("start_time", "end_time", "description", "vendor")
        widgets = {
            'vendor': autocomplete.ModelSelect2(
                url='services:shopping-autocomplete',
                attrs={
                    'data-placeholder': 'Vendors ...',
                    'data-minimum-input-length': 1,
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput(
            attrs={'value': datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%dT%H:%M")})
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput(attrs={
            'value': (datetime.now().astimezone(timezone('Asia/Kolkata')) + timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M")})
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        # self.fields["slackness"].widget = DurationInput()
        # self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

    def clean(self):
        super(ShoppingCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime > etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        # slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        vendor = self.cleaned_data['vendor']

        return {'start_time': start_time, 'end_time': end_time, 'description': description,
                'vendor': vendor}


class TravelCreationForm(autocomplete.FutureModelForm):
    class Meta:
        model = TravelService
        fields = ("start_point", "end_point", "start_time", "end_time", "description", "transport")
        widgets = {
            'start_point': autocomplete.ModelSelect2(
                url='services:location-autocomplete',
                attrs={
                    'data-placeholder': 'start_loc ...',
                    'data-minimum-input-length': 1,
                },
            ),
            'end_point': autocomplete.ModelSelect2(
                url='location:location-autocomplete',
                attrs={
                    'data-placeholder': 'end_loc ...',
                    'data-minimum-input-length': 1,
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput(
            attrs={'value': datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%dT%H:%M")})
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput(attrs={
            'value': (datetime.now().astimezone(timezone('Asia/Kolkata')) + timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M")})
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        # self.fields["slackness"].widget = DurationInput()
        # self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

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
        # slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        transport = self.cleaned_data['transport']

        return {'start_point': start_point, 'end_point': end_point, 'start_time': start_time, 'end_time': end_time,
                'description': description, 'transport': transport}

        # f=FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=vendor, description=description, start_time=start_time, end_time=end_time, slackness=slackness, stype='Food')
        # f.save()
        # sm=ServiceMember(service=f, user=u)
        # sm.save()


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = EventService
        fields = ("start_time", "end_time", "description", "location", "event_type")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput()
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput()
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        # self.fields["slackness"].widget = DurationInput()
        # self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

    def clean(self):
        super(EventCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime > etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        location = self.cleaned_data['location']
        event_type = self.cleaned_data['event_type']
        return {'start_time': start_time, 'end_time': end_time,
                'slackness': slackness, 'description': description, 'location': location, 'event_type': event_type}

        # f=FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=vendor, description=description, start_time=start_time, end_time=end_time, slackness=slackness, stype='Food')
        # f.save()
        # sm=ServiceMember(service=f, user=u)
        # sm.save()


class OtherCreationForm(forms.ModelForm):
    class Meta:
        model = OtherService
        fields = ("start_time", "end_time", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget = DateTimeInput()
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        self.fields["end_time"].widget = DateTimeInput()
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        # self.fields["slackness"].widget = DurationInput()
        # self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

    def clean(self):
        super(OtherCreationForm, self).clean()
        stime = self.cleaned_data.get('start_time')
        etime = self.cleaned_data.get('end_time')
        if (stime is not None) and (etime is not None) and stime > etime:
            raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']

        return {'start_time': start_time, 'end_time': end_time,
                'slackness': slackness, 'description': description}

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


class GroupSelectForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Group.objects.all()
    )

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('currentuser')
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.filter(members=current_user.id).all()
