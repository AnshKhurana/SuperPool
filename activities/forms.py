from dal import autocomplete
from pool.models import *
from django.utils.dateparse import parse_duration
from django.forms import ValidationError
from dal import autocomplete
from datetime import datetime, timedelta
from pytz import timezone


class TravelActivityForm(autocomplete.FutureModelForm):
    class Meta:
        model = TravelService
        fields = ("start_point", "end_point", "description", "transport")
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
        # self.fields["start_time"].widget = DateTimeInput(
        #     attrs={'value': datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%dT%H:%M")})
        # self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        #
        # self.fields["end_time"].widget = DateTimeInput(attrs={
        #     'value': (datetime.now().astimezone(timezone('Asia/Kolkata')) + timedelta(days=1)).strftime(
        #         "%Y-%m-%dT%H:%M")})
        # self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

        # self.fields["slackness"].widget = DurationInput()
        # self.fields["slackness"].input_formats = ["%dT%H:%M", "%d %H:%M"]

    def clean(self):
        super(TravelActivityForm, self).clean()
        # stime = self.cleaned_data.get('start_time')
        # etime = self.cleaned_data.get('end_time')
        # if (stime is not None) and (etime is not None) and stime > etime:
        #     raise ValidationError('Start time after end time')

    def save(self, commit=False):
        start_point = self.cleaned_data['start_point']
        end_point = self.cleaned_data['end_point']
        # start_time = self.cleaned_data['start_time']
        # end_time = self.cleaned_data['end_time']
        # slackness = self.cleaned_data['slackness']
        description = self.cleaned_data['description']
        transport = self.cleaned_data['transport']

        return {'start_point': start_point, 'end_point': end_point, 'description': description, 'transport': transport}

        # f=FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=vendor, description=description, start_time=start_time, end_time=end_time, slackness=slackness, stype='Food')
        # f.save()
        # sm=ServiceMember(service=f, user=u)
        # sm.save()