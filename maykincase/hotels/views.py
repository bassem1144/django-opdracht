from django.shortcuts import render
from .models import Hotel, City

# Display all hotels, optionally filtered by city
def hotel_list(request):
    # Get the selected city code from the query parameters (if not blank)
    selected_city = request.GET.get('city', '')

    # Get all cities in the database
    cities = City.objects.all().order_by('name')

    # Get all hotels and filter by city if selected
    hotels = Hotel.objects.select_related('city')
    if selected_city:
        hotels = hotels.filter(city__code=selected_city)
    
    return render(request, 'hotel_list.html', {
        'hotels': hotels,
        'cities': cities,
        'selected_city': selected_city
    })