# Django Hotel Management - Maykin Case

Django application for importing CVS data of hotels and cities and displaying them with filtering options and managing them via the Django admin interface.

## Requirements

- Python 3.10+
- Django 5.2+

## Setup Instructions

1. **Navigate to the project directory**

   ```bash
   cd maykincase
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

4. **Import hotel and city data**

   ```bash
   python manage.py import_hotels
   ```

5. **Create admin user (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Running Tests

```bash
python manage.py test
```
