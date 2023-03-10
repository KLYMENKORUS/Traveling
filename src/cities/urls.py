from django.urls import path
from cities.views import *


app_name = 'cities'

urlpatterns = [
    path('', CityListView.as_view(), name='list_cities'),
    path('detail/<int:pk>/', DetailCityView.as_view(), name='detail_city'),
    path('add/', CreateCityView.as_view(), name='create_city'),
    path('update/<int:pk>/', UpdateCityView.as_view(), name='update_city'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete_city'),
    path('search/', SearchCities.as_view(), name='search_city')
]