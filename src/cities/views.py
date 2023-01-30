from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CityForm
from .models import City

__all__ = (
    'CityListView',
    'DetailCityView',
    'CreateCityView',
    'UpdateCityView',
    'delete_city'
)


class CityListView(ListView):
    model = City
    paginate_by = 3
    template_name = 'cities/list_cities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form
        return context


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


def delete_city(request, pk):
    city = get_object_or_404(City, id=pk)
    city.delete()
    messages.info(request, f'Город {city.name} успешно удален!')
    return redirect('cities:list_cities')



