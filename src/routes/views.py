from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from cities.models import City
from trains.models import Train
from .models import Route
from .forms import RouteForm, RouteModelForm
from django.contrib import messages
from .utils import get_routes


__all__ = (
    'routes_list',
    'find_routes',
    'add_route',
    'save_route',
    'RouteListView',
    'RouteSearchView',
    'RouteDetailView'
)


def routes_list(request):
    form = RouteForm()
    return render(request, 'routes/routes_list.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as v_e:
                messages.error(request, v_e)
                return render(request, 'routes/routes_list.html', {'form': form})
            return render(request, 'routes/routes_list.html', context)
        return render(request, 'routes/routes_list.html', {'form': form})

    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        context = {'form': form}
        return render(request, 'routes/routes_list.html', context)


def add_route(request):
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            total_time = int(data['travel_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_lst = [int(tr) for tr in trains if tr.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst).\
                select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).\
                in_bulk()

            form = RouteModelForm(
                initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'travel_time': total_time,
                    'trains': qs
                })
            context['form'] = form
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, 'Невозможно сохранить нечуществующий'
                                'маршрут')
        return redirect('home')


def save_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Маршрут успешно сохранен!')
            return redirect('home')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, 'Невозможно сохранить нечуществующий'
                                'маршрут')
        return redirect('home')


class RouteListView(ListView):
    model = Route
    paginate_by = 3
    template_name = 'routes/list.html'


class RouteSearchView(ListView):
    model = Route
    template_name = 'routes/list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search = Route.objects.filter(
            Q(name__icontains=query)
        )
        return search


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'
