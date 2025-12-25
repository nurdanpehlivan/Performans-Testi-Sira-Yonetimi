from django.contrib import admin
from django.urls import path, include
# home_view için:
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Queue Management System!", status=200)

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    # KRİTİK: API uygulamasını dahil etme
path('api/', include('api.urls')),]