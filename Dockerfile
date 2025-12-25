# Temel Python imajını kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimler dosyasını (requirements.txt) kopyala
COPY requirements.txt .

# Gerekli Python paketlerini kur
RUN pip install --no-cache-dir -r requirements.txt

# Tüm uygulama kodunu kopyala
COPY . .

# Uygulamayı çalıştırırken kullanacağı komutu belirle (şimdilik sadece başlangıç)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ********** KRİTİK EKLEME **********
# PYTHONPATH'e '/app' dizinini ekleyerek Django'nun sira_proje'yi bulmasını garanti ediyoruz.
ENV PYTHONPATH=/app:$PYTHONPATH
# **********************************

# Uygulamayı çalıştırırken kullanacağı komutu belirle
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]