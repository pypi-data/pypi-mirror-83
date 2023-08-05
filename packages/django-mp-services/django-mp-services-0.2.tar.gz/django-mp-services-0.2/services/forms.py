
from django import forms
from django.utils.translation import ugettext_lazy as _

from basement.utils import get_date_from_request

from cap.fields import DatePickerField

from services.models import ServiceCategory


class ReportForm(forms.Form):

    date_from = DatePickerField(label=_('Date from'))

    date_to = DatePickerField(label=_('Date to'))

    def __init__(self, request):

        super().__init__(
            data={
                'date_from': get_date_from_request(request, 'date_from'),
                'date_to': get_date_from_request(request, 'date_to')
            }
        )

        self.is_valid()


class SearchServiceForm(forms.Form):

    code = forms.CharField(required=False)

    query = forms.CharField(required=False)

    category = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.all(),
        required=False,
        widget=forms.HiddenInput)

    def clean(self):

        cleaned_data = {}

        for k, v in self.cleaned_data.items():
            if v:
                cleaned_data[k] = v

        return cleaned_data
