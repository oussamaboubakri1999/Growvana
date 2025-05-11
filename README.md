# GrowVana

GrowVana is a smart dashboard and device management web application for monitoring and visualizing agricultural or environmental sensor data. It features modern, responsive dashboards, real-time charts, and user/device management for growers and researchers.

## Features
- User authentication and role-based access
- Dashboard with live charts (temperature, humidity, measurements)
- Device management and status updates
- Alert notifications
- Statistics and activity tracking
- Beautiful, responsive UI (Tailwind CSS, Chart.js)
- Django backend with REST API

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/oussamaboubakri1999/Growvana.git
   cd Growvana
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the app:**
   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Project Structure
- `dashboard/` - Main Django app for dashboard, devices, alerts, and statistics
- `static/` - Static files (JS, CSS)
- `templates/` - HTML templates
- `requirements.txt` - Python dependencies

## Dependencies
See `requirements.txt` for a full list. Key packages:
- Django
- djangorestframework
- django-allauth
- django-cors-headers
- djangorestframework-simplejwt
- Chart.js (via CDN)
- Tailwind CSS (via CDN)

## License
MIT
