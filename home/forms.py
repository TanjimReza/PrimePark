import email
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(ModelForm):
    class Meta: 
        model = Users
        fields = '__all__'
class SpotForm(ModelForm):
    class Meta: 
        model = Spot
        fields = '__all__'
        