from django import forms
from news.models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        exclude = ['concurrency_user', 'concurrency_key', 'concurrency_time']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.DateInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.DateInput(attrs={'type': 'time'}),
        }

    def clean(self):

        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)

        # Don't change the Error messages without also chaning their test equivalents
        if (start_time or end_time) and not (start_date and end_date):
            raise forms.ValidationError("time fields require date fields to be filled")

        if start_date > end_date:
            raise forms.ValidationError("start_date must occur before or at the same time as end_date")

        if start_date == end_date and start_time > end_time:
            raise forms.ValidationError("start_time must occur before end_time when start_date==end_date")


