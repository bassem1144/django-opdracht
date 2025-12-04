from django.contrib import admin
from .models import City, Hotel


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city']
    list_filter = ['city']
    search_fields = ['code', 'name', 'city__name']
