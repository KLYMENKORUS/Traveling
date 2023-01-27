from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CityForm
from .models import City

__all__ = (
    'list_cities',
    'DetailCityView',
    'CreateCityView',
    'UpdateCityView',
    'DeleteCityView'
)


def list_cities(request):
    form = CityForm()
    match request.method:
        case 'POST':
            form = CityForm(request.POST)
            if form.is_valid():
                form.save()

    qs = City.objects.all()
    context = {'object_list': qs, 'form': form}
    return render(request, 'cities/list_cities.html', context)


class DetailCityView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail_city.html'


class CreateCityView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create_city.html'
    success_message = 'Город успешно добавлен!'

    def get_success_url(self):
        return reverse_lazy('cities:detail_city', kwargs={'pk': self.object.pk})


class UpdateCityView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update_city.html'
    success_message = 'Запись о городе обновлена'

    def get_success_url(self):
        return reverse_lazy('cities:detail_city', kwargs={'pk': self.object.pk})


class DeleteCityView(SuccessMessageMixin, DeleteView):
    model = City
    template_name = 'cities/detail_city.html'
    success_message = 'Город удален из базы данных'
    success_url = reverse_lazy('cities:list_cities')


