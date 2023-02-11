from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Название маршрута')
    owner_route = models.ForeignKey(User, on_delete=models.CASCADE,
                                    verbose_name='Автор Маршрута')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Общее время в пути')
    from_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                  related_name='route_from_city_set',
                                  verbose_name='Из какого города')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                related_name='route_to_city_set',
                                verbose_name='В какой город')
    trains = models.ManyToManyField('trains.Train', verbose_name='Список поездов')

    def __str__(self):
        return f'Маршрут {self.name} из города {self.from_city} в {self.to_city}'

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Измените город прибытия/отправления!')
        qs = Route.objects.filter(from_city=self.from_city,
                                  to_city=self.to_city,
                                  travel_time=self.travel_time).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Измените время пути!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['travel_time']