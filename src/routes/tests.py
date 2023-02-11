from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cities.models import City
from trains.models import Train
from routes import views as routes_views
from cities import views as cities_views
from routes.utils import get_graph, dfs_path
from routes.forms import RouteForm


class AllTestCase(TestCase):
    def setUp(self) -> None:
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')

        lst = [
            Train(name='tr1', from_city=self.city_A, to_city=self.city_B,
                  travel_time=9),
            Train(name='tr2', from_city=self.city_B, to_city=self.city_D,
                  travel_time=8),
            Train(name='tr3', from_city=self.city_A, to_city=self.city_C,
                  travel_time=7),
            Train(name='tr4', from_city=self.city_C, to_city=self.city_B,
                  travel_time=5),
            Train(name='tr5', from_city=self.city_B, to_city=self.city_E,
                  travel_time=4),
            Train(name='tr6', from_city=self.city_B, to_city=self.city_A,
                  travel_time=11),
            Train(name='tr7', from_city=self.city_A, to_city=self.city_C,
                  travel_time=10),
            Train(name='tr8', from_city=self.city_E, to_city=self.city_D,
                  travel_time=5),
            Train(name='tr9', from_city=self.city_D, to_city=self.city_E,
                  travel_time=4),
        ]
        Train.objects.bulk_create(lst)

    def test_model_city_duplicate(self):
        """Тестирование возникновения ошибки присоздании дубля города"""
        city = City(name='A')
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_model_train_duplicate(self):
        """Тестирование возникновения ошибки присоздании дубля поезда"""
        train_error_name = Train(name='tr1', from_city=self.city_A, to_city=self.city_B,
                                 travel_time=9)
        with self.assertRaises(ValidationError):
            train_error_name.full_clean()

    def test_model_train_time_duplicate(self):
        """Тестирование возникновения ошибки присоздании дубля поезда"""
        train_error_time = Train(name='tr1555', from_city=self.city_A, to_city=self.city_B,
                                 travel_time=9)
        with self.assertRaises(ValidationError):
            train_error_time.full_clean()

    def test_routes_list_views(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='routes/routes_list.html')
        self.assertEqual(response.resolver_match.func, routes_views.routes_list)

    def test_city_detail_views(self):
        response = self.client.get(reverse('cities:detail_city',
                                           kwargs={'pk': self.city_A.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='cities/detail_city.html')
        self.assertEqual(response.resolver_match.func.__name__,
                         cities_views.DetailCityView.as_view().__name__)

    def test_find_all_routes(self):
        qs = Train.objects.all()
        graph = get_graph(qs)
        all_routes = list(dfs_path(graph, self.city_A.id, self.city_E.id))
        self.assertEqual(len(all_routes), 4)

    def test_valid_routes_form(self):
        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_D.id,
            'cities': [self.city_B.id, self.city_C.id],
            'traveling_time': 8
        }
        form = RouteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_routes_form(self):
        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_D.id,
            'cities': [self.city_B.id, self.city_C.id],
            'traveling_time': 8.232
        }
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())

    def test_message_error_more_time(self):
        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_E.id,
            'cities': [self.city_C.id],
            'traveling_time': 8
        }
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Время в пути больше заданного!', 1, 200)

    def test_message_error_from_cities(self):
        data = {
            'from_city': self.city_B.id,
            'to_city': self.city_E.id,
            'cities': [self.city_C.id],
            'traveling_time': 98
        }
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Маршрут, через эти города не возможен!', 1, 200)
