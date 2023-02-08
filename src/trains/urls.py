from django.urls import path
from trains.views import *


app_name = 'trains'

urlpatterns = [
    path('', TrainListView.as_view(), name='list_trains'),
    path('detail/<int:pk>/', DetailTrainView.as_view(), name='detail_train'),
    path('add/', CreateTrainView.as_view(), name='create_train'),
    path('update/<int:pk>/', UpdateTrainView.as_view(), name='update_train'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete_train'),
    path('search/', SearchTrainView.as_view(), name='search_train')
]