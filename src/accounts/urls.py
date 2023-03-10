from django.urls import path
from .views import *


app_name = 'accounts'


urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', registration, name='registration')
]