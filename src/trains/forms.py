from django import forms
from cities.models import City
from .models import Train


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Номер Поезда', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите номер Поезда'}))
    travel_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите время в пути'}))
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(
                                           attrs={'class': 'form-control'}),
                                       empty_label='Выбирете город')
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(
                                         attrs={'class': 'form-control'}),
                                     empty_label='Выбирете город')

    class Meta:
        model = Train
        fields = '__all__'
