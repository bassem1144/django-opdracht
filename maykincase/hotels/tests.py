from django.test import TestCase
from django.urls import reverse
from .models import City, Hotel


class CityModelTest(TestCase):
    def test_create_city(self):
        city = City.objects.create(code='AMS', name='Amsterdam')
        self.assertEqual(city.code, 'AMS')
        self.assertEqual(city.name, 'Amsterdam')
        self.assertEqual(str(city), 'Amsterdam (AMS)')


class HotelModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(code='AMS', name='Amsterdam')
    
    def test_create_hotel(self):
        hotel = Hotel.objects.create(
            code='H001',
            name='Test Hotel',
            city=self.city
        )
        self.assertEqual(hotel.code, 'H001')
        self.assertEqual(hotel.name, 'Test Hotel')
        self.assertEqual(hotel.city, self.city)
        self.assertEqual(str(hotel), 'Test Hotel [H001]')


class HotelListViewTest(TestCase):
    def setUp(self):
        self.city1 = City.objects.create(code='AMS', name='Amsterdam')
        self.city2 = City.objects.create(code='BER', name='Berlin')
        Hotel.objects.create(code='H001', name='Hotel Amsterdam', city=self.city1)
        Hotel.objects.create(code='H002', name='Hotel Berlin', city=self.city2)
    
    def test_view_all_hotels(self):
        response = self.client.get(reverse('hotel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hotel Amsterdam')
        self.assertContains(response, 'Hotel Berlin')
    
    def test_filter_by_city(self):
        response = self.client.get(reverse('hotel_list'), {'city': 'AMS'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hotel Amsterdam')
        self.assertNotContains(response, 'Hotel Berlin')
    
    def test_empty_database(self):
        Hotel.objects.all().delete()
        City.objects.all().delete()
        response = self.client.get(reverse('hotel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Geen hotels gevonden')

