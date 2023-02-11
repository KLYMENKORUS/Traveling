from django import forms
from django.core.exceptions import ValidationError
from cities.models import City
from routes.models import Route
from trains.models import Train


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(
                                           attrs={'class': 'form-control '
                                                           'js-example-basic-single'}),
                                       empty_label='Выбирете город')
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(
                                         attrs={'class': 'form-control '
                                                         'js-example-basic-single'}),
                                     empty_label='Выбирете город')
    cities = forms.ModelMultipleChoiceField(
        label='Через города', queryset=City.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple'})
    )
    traveling_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите время в пути'}))


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите название маршрута'}))
    from_city = forms.ModelChoiceField(queryset=City.objects.all(),
                                       widget=forms.HiddenInput()
                                       )
    to_city = forms.ModelChoiceField(queryset=City.objects.all(),
                                     widget=forms.HiddenInput()
                                     )
    trains = forms.ModelMultipleChoiceField(
        queryset=Train.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control d-none'})
    )
    travel_time = forms.IntegerField(widget=forms.HiddenInput())

    def clean_name(self):
        data = self.cleaned_data
        if Route.objects.filter(name=data.get('name')).exists():
            raise ValidationError('Маршрут с таким названием уже существует!')
        return data.get('name')

    class Meta:
        model = Route
        fields = ['name', 'from_city', 'to_city', 'trains', 'travel_time']

