"""
Management command to import hotel and city data from CSV URLs.
Usage: python manage.py import_hotels
"""
import csv
from io import StringIO

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import requests

from hotels.models import City, Hotel


CITY_URL = "http://rebecca.maykinmedia.nl/djangocase/city.csv"
HOTEL_URL = "http://rebecca.maykinmedia.nl/djangocase/hotel.csv"


class Command(BaseCommand):
    help = 'Import hotel and city data from CSV endpoints'

    def handle(self, *args, **options):
        self.stdout.write("Starting import...")
        
        cities_stats = self.import_cities()
        hotels_stats = self.import_hotels()
        
        self.stdout.write(self.style.SUCCESS(
            f"\nImport complete!\n"
            f"Cities: {cities_stats['created']} created, {cities_stats['updated']} updated\n"
            f"Hotels: {hotels_stats['created']} created, {hotels_stats['updated']} updated"
        ))

    def fetch_csv(self, url):
        """Download CSV file from URL."""
        self.stdout.write(f"Fetching {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    @transaction.atomic
    def import_cities(self):
        """Import cities from CSV."""
        csv_content = self.fetch_csv(CITY_URL)
        reader = csv.reader(StringIO(csv_content), delimiter=';', quotechar='"')
        
        created = updated = 0
        
        for row in reader:
            if len(row) < 2 or not row[0].strip():
                continue
            
            city_code = row[0].strip()
            city_name = row[1].strip()
            
            _, is_new = City.objects.update_or_create(
                code=city_code,
                defaults={"name": city_name}
            )
            
            if is_new:
                created += 1
                self.stdout.write(f"  ✓ Created: {city_name} ({city_code})")
            else:
                updated += 1
        
        return {"created": created, "updated": updated}

    @transaction.atomic
    def import_hotels(self):
        """Import hotels from CSV."""
        csv_content = self.fetch_csv(HOTEL_URL)
        reader = csv.reader(StringIO(csv_content), delimiter=';', quotechar='"')
        
        created = updated = skipped = 0
        
        for row_num, row in enumerate(reader, start=1):
            # Skip invalid rows
            if len(row) < 3 or not row[0].strip() or not row[1].strip():
                skipped += 1
                continue
            
            city_code = row[0].strip()
            hotel_code = row[1].strip()
            hotel_name = row[2].strip()
            
            # Find the city
            try:
                city = City.objects.get(code=city_code)
            except City.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"  ✗ Row {row_num}: City '{city_code}' not found"
                ))
                skipped += 1
                continue
            
            # Create or update hotel
            _, is_new = Hotel.objects.update_or_create(
                code=hotel_code,
                defaults={"name": hotel_name, "city": city}
            )
            
            if is_new:
                created += 1
                if created <= 5:
                    self.stdout.write(f" Created: {hotel_name} ({hotel_code})")
            else:
                updated += 1
        
        if created > 5:
            self.stdout.write(f"  ... and {created - 5} more hotels")
        
        if skipped:
            self.stdout.write(self.style.WARNING(f" Skipped {skipped} rows"))
        
        return {"created": created, "updated": updated}
