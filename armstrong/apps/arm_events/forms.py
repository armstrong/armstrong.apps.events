from django.forms import HiddenInput, ModelForm
from armstrong.apps.arm_events.models import RSVP

class RSVPCreateForm(ModelForm):
    class Meta:
        model = RSVP
        fields = ('event', 'name', 'email', 'guests')
        widgets = {
            'event': HiddenInput()
        }
