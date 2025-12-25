from django.db import models

class Ticket(models.Model):
    SERVICE_CHOICES = [
        ('GENEL', 'Genel İşlemler'),
        ('GISE', 'Gişe İşlemleri'),
        ('OZEL', 'Özel Müşteri'),
    ]
    number = models.IntegerField()
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='GENEL')
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255, null=True, blank=True) # S3/MinIO için