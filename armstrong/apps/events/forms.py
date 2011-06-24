from django.forms import HiddenInput, ModelForm
from .models import RSVP


class RSVPCreateForm(ModelForm):
    class Meta:
        model = RSVP
        fields = ('event', 'name', 'email', 'guests')
        widgets = {
            'event': HiddenInput()
        }
