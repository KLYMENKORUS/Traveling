from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from .models import Train
from .forms import TrainForm

__all__ = (
    'TrainListView',
    'DetailTrainView',
    'CreateTrainView',
    'UpdateTrainView',
    'delete_train'
)


class TrainListView(ListView):
    model = Train
    paginate_by = 3
    template_name = 'trains/list_trains.html'


class DetailTrainView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail_train.html'


class CreateTrainView(CreateView):
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


class UpdateTrainView(UpdateView):
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


def delete_train(request, pk):
    train = get_object_or_404(Train, id=pk)
    train.delete()
    messages.success(request, f'Город {train.name} успешно удален!')
    return redirect('trains:list_trains')



