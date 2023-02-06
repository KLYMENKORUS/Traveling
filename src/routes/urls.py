from django.urls import path
from .views import *


urlpatterns = [
    path('', routes_list, name='home'),
    path('find_routes/', find_routes, name='find_routes'),
    path('add_route/', add_route, name='add_route'),
    path('save_route/', save_route, name='save_route'),
    path('routes_list/', RouteListView.as_view(), name='list'),
    path('search/', RouteSearchView.as_view(), name='search_route'),
    path('detail/<int:pk>/', RouteDetailView.as_view(), name='detail_route'),
]
