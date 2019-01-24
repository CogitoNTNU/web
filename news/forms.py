import datetime

from django import forms

from news.helpers import generate_mazemap_embed

from news.models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        exclude = ['concurrency_user', 'concurrency_key', 'concurrency_time',
                   'datetime_created', 'location_url_embed']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'value': str(datetime.date.today())}),
            'start_time': forms.DateInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'value': str(datetime.date.today())}),
            'end_time': forms.DateInput(attrs={'type': 'time'}),
        }

    def clean(self):

        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)
        location_url = self.cleaned_data.get('location_url', None)
        location_off_campus = self.cleaned_data.get('location_off_campus', None)

        # Don't change the Error messages without also chaning their test equivalents
        if (start_time or start_date) and (end_time and not end_date):
            raise forms.ValidationError("time fields require date fields to be filled")

        if start_date > end_date:
            raise forms.ValidationError("start_date must occur before or at the same time as end_date")

        if start_date == end_date and start_time > end_time:
            raise forms.ValidationError("start_time must occur before end_time when start_date==end_date")

        if not location_off_campus and location_url \
                and generate_mazemap_embed(location_url) is None:
            raise forms.ValidationError("location url not recognized as valid Maze map link, check 'not mazemap' or fix link")

    def save(self, commit=True):
        event = super().save(commit=False)
        location_url = self.cleaned_data.get('location_url', None)
        location_off_campus = self.cleaned_data.get('location_off_campus', None)

        if not location_off_campus and location_url:
            event.location_url_embed = generate_mazemap_embed(location_url)
        elif (location_url is None or location_off_campus) \
                and event.location_url_embed is not None:
            event.location_url_embed = None
        if commit:
            event.save()
        return event
