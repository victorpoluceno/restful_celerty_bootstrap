from django.forms import ModelForm
from rest_api.models import Url

class UrlForm(ModelForm):
    class Meta:
        model = Url
