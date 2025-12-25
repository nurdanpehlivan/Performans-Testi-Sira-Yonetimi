import uuid
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class SecurityScanTest(TestCase):
    def test_multiple_file_scans(self):
        # Rastgele 3 farklı dosya ismiyle test yapalım
        for i in range(3):
            random_name = f"kullanici_dosyasi_{uuid.uuid4().hex[:5]}.jpg"
            file = SimpleUploadedFile(random_name, b"icerik", content_type="image/jpeg")
            
            response = self.client.post('/api/create-ticket/', {
                'service_type': 'GISE',
                'file': file
            })
            
            self.assertEqual(response.status_code, 201)
            # Bu döngü her döndüğünde loglarda farklı bir isim göreceksiniz