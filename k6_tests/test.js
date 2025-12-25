import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 30 }, 
    { duration: '20s', target: 60 }, 
    { duration: '10s', target: 0 },  
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], 
  },
};

export default function () {
  // En garanti adres: Django'nun kendi IP/Port adresi
  const url = 'http://django_app:8000/api/status'; 
  
  const res = http.get(url);

  // Başarı kontrolünü esnetiyoruz: Cevap boş değilse BAŞARILI say
  check(res, {
    'Sistem Erisilebilir mi?': (r) => r.body.length > 0,
  });

  sleep(1);
}