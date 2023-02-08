from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView
from .models import Train
from .forms import TrainForm
from django.db.models import Q


__all__ = (
    'TrainListView',
    'DetailTrainView',
    'CreateTrainView',
    'UpdateTrainView',
    'SearchTrainView',
    'TrainDeleteView'
)


class SearchTrainView(ListView):
    model = Train
    template_name = 'trains/list_trains.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search = Train.objects.filter(
            Q(name__icontains=query) |
            Q(from_city__name__icontains=query) |
            Q(to_city__name__icontains=query)
        )
        return search


class TrainListView(ListView):
    model = Train
    paginate_by = 3
    template_name = 'trains/list_trains.html'


class DetailTrainView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail_train.html'


class CreateTrainView(LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create_train.html'

    def get_success_url(self):
        return reverse_lazy('trains:detail_train', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        messages.info(self.request, f'Поезд № {instance.name} успешно добавлен!')
        return super().form_valid(form)


class UpdateTrainView(LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update_train.html'

    def get_success_url(self):
        return reverse_lazy('trains:detail_train', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        messages.info(self.request, f'Поезд № {instance.name} успешно обновлен!')
        return super().form_valid(form)


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    success_url = reverse_lazy('trains:list_trains')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f'Поезд {self.object.name} успешно удален!')
        return redirect(success_url)



