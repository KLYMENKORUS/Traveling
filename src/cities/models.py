from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, help_text='Не боллее 100 символов',
                            unique=True, verbose_name='Название города')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
