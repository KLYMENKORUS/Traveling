from django.shortcuts import render
from .forms import RouteForm
from django.contrib import messages
from .utils import get_routes


__all__ = (
    'routes_list',
    'find_routes',
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

