from django.contrib import admin
from django.urls import path
from hotels import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hotel_list, name='hotel_list'),
]
