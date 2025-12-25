# sira_yonetimi_proje/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sira_yonetimi_proje.settings')

application = get_wsgi_application()