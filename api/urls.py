from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.status_check, name='api_status'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
]