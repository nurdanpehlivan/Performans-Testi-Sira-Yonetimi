import boto3
import traceback
import clamd
from django.conf import settings
from django.http import JsonResponse
from .models import Ticket
from django.views.decorators.csrf import csrf_exempt

def status_check(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def create_ticket(request):
    if request.method == 'POST':
        service = request.POST.get('service_type', 'OGRENCI') # Varsayılan artık OGRENCI
        uploaded_file = request.FILES.get('file')
        
        # 1. DOSYA ZORUNLULUK KONTROLÜ
        if not uploaded_file:
            return JsonResponse({
                "status": "error",
                "message": "Seminer kaydı için katılım belgesi (PDF veya Görsel) yüklemek zorunludur!"
            }, status=400)

        # 2. FORMAT KONTROLÜ (PDF ve Görsel kısıtlaması)
        allowed_extensions = ('.pdf', '.png', '.jpg', '.jpeg')
        if not uploaded_file.name.lower().endswith(allowed_extensions):
            return JsonResponse({
                "status": "error",
                "message": "Geçersiz dosya formatı! Sadece PDF, PNG ve JPG yükleyebilirsiniz."
            }, status=400)

        last_ticket = Ticket.objects.order_by('-number').first()
        next_number = (last_ticket.number + 1) if last_ticket else 1
        file_url = ""

        try:
            # 3. ClamAV Bağlantısı ve Tarama
            cd = clamd.ClamdNetworkSocket(host='clamav_service', port=3310)
            scan_result = cd.instream(uploaded_file)
            uploaded_file.seek(0) # Dosya imlecini başa sar (S3 için önemli)

            # --- GÜVENLİK KONTROLÜ ---
            if scan_result['stream'][0] == 'OK':
                # Terminale temiz mesajı
                print(f"Güvenlik Onayı: {uploaded_file.name} temiz. Akreditasyon onaylandı.", flush=True)
                
                # 4. S3 / MinIO Yükleme (Seminer klasörüne)
                s3 = boto3.client('s3',
                    endpoint_url='http://172.17.0.1:9000',
                    aws_access_key_id='minio_admin',
                    aws_secret_access_key='minio_password',
                    region_name='us-east-1'
                )
                
                # Bucket ismini hikayeye uyduralım: 'seminer-kayitlari'
                # Not: Eğer MinIO'da bu isimde bucket yoksa 'bilet-evraklari' olarak bırakabilirsiniz.
                s3.upload_fileobj(uploaded_file, 'bilet-evraklari', uploaded_file.name)
                file_url = f"http://localhost:9000/bilet-evraklari/{uploaded_file.name}"
            
            else:
                # VİRÜS TESPİTİ
                virus_name = str(scan_result['stream'][1])
                error_msg = f"!!! GÜVENLİK İHLALİ !!!: {uploaded_file.name} dosyasında zararlı içerik ({virus_name}) tespit edildi! Kayıt reddedildi."
                print(error_msg, flush=True) 
                
                return JsonResponse({
                    "status": "error",
                    "message": "Yüklediğiniz belge güvenlik taramasından geçemedi (Zararlı içerik tespit edildi).",
                    "detail": virus_name
                }, status=400)

        except Exception as e:
            print("!!! KRİTİK HATA: TARAMA VEYA DEPOLAMA SERVİSİNE ULAŞILAMADI !!!")
            print(traceback.format_exc())
            return JsonResponse({
                "status": "error", 
                "message": "Sistem şu an güvenlik taraması yapamıyor, lütfen teknik birimle iletişime geçin."
            }, status=500)

        # 5. Veritabanı Kaydı (Sadece her şey temizse)
        ticket = Ticket.objects.create(
            number=next_number, 
            service_type=service,
            file_path=file_url
        )
        
        return JsonResponse({
            "status": "ok", 
            "message": "Seminer kaydınız başarıyla oluşturuldu.",
            "ticket_number": ticket.number,
            "service": ticket.service_type,
            "file_url": file_url
        }, status=201)
        
    return JsonResponse({"error": "Sadece POST metodu destekleniyor."}, status=405)