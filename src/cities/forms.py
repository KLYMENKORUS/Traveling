from django import forms
from django.core.exceptions import ValidationError

from .models import City


class CityForm(forms.ModelForm):
    name = forms.CharField(label='Город', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите город'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        if City.objects.filter(name=name).exists():
            raise ValidationError('Город с таким названием уже существует!')

    class Meta:
        model = City
        fields = ['name']
