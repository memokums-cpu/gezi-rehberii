import requests

# --- AYARLAR ---
STRAPI_URL = "http://127.0.0.1:1337"
# DİKKAT: Aşağıdaki tırnak içine kendi Sınırsız Strapi Token'ını yapıştır!
STRAPI_TOKEN = "aa268b71da8cd7d4192756a0168245ecb27ebfcc603beac2ea3e65e40ca127b6fe8778ddce0539ab06398a7977123e8adddad4866cd0a5281bd305e7708d25b5f211c630d0514efdb0bc49ffd3d084ba2a44a6fd96c655a43af8c47d26efe867bb8c84b0ff2b9f926faac335af0c0939f8652400bae85252b80c42c64d1c9dc1"

headers = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json"
}

# --- EKLENECEK ŞEHİRLER (SADECE TEMİZ METİNLER) ---
# Buraya dilediğin kadar şehir yazabilirsin.
sehirler = [
    "Edirne", 
    "İstanbul", 
    "İzmir", 
    "Antalya", 
    "Ankara",
    "Nevşehir",
    "Trabzon",
    "Paris",
    "Roma",
    "Tokyo"
]

print("🧹 Eski veriler yok sayılıyor, yeni şehirler sisteme kod ile basılıyor...\n")

for sehir in sehirler:
    # İşte Strapi'nin tam olarak beklediği DÜZ METİN veri paketi:
    payload = {
        "data": {
            "ad": sehir 
        }
    }
    
    cevap = requests.post(f"{STRAPI_URL}/api/cities", json=payload, headers=headers)
    
    if cevap.status_code in [200, 201]:
        print(f"✅ Şehir eklendi: {sehir}")
    else:
        print(f"❌ HATA ({sehir}): {cevap.text}")

print("\n🎉 Bütün şehirler veri tabanına başarıyla işlendi! Artık mekan koduna geçebilirsin.")