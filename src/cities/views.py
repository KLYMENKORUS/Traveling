from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CityForm
from .models import City
from django.db.models import Q


__all__ = (
    'CityListView',
    'DetailCityView',
    'CreateCityView',
    'UpdateCityView',
    'SearchCities',
    'CityDeleteView'
)


class SearchCities(ListView):
    model = City
    template_name = 'cities/list_cities.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search = City.objects.filter(
            Q(name__icontains=query)
        )
        return search


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


class CreateCityView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create_city.html'
    success_message = 'Город успешно добавлен!'

    def get_success_url(self):
        return reverse_lazy('cities:detail_city', kwargs={'pk': self.object.pk})


class UpdateCityView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update_city.html'
    success_message = 'Запись о городе обновлена'

    def get_success_url(self):
        return reverse_lazy('cities:detail_city', kwargs={'pk': self.object.pk})


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    success_url = reverse_lazy('cities:list_cities')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f'Город {self.object.name} успешно удален!')
        return redirect(success_url)


