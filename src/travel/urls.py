from django.contrib import admin
from django.urls import path, include
from routes.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include('cities.urls', namespace='cities')),
    path('trains/', include('trains.urls', namespace='trains')),
    path('', routes_list, name='home'),
    path('find_routes/', find_routes, name='find_routes')
]
