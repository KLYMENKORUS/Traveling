from django.contrib import admin
from .models import Train


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['name', 'from_city', 'to_city', 'travel_time']
    list_filter = ['from_city', 'to_city']
    list_editable = ['travel_time']


