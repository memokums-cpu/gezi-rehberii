import requests
from deep_translator import GoogleTranslator
import urllib.request
import urllib.parse
import g4f

# --- AYARLAR ---
STRAPI_URL = "https://gezi-rehberne-d.onrender.com"
STRAPI_TOKEN = "172eaf36a80ecb27e9e9b57b78c5a782adbc79f474f46ef902fbf1c40a80d5826e2aa2e468a24b5836a373e0afb8cac80096300059477825b9668932949053ba71d2df316245c95ea60c6127e9e3353a362c423632526e864c71ad6f9403c3f9246252ffdf0024e7e464bf70b4260c02ad79fd6b279e4f0ee93c714b7350e150" # DİKKAT: Kendi şifreni girmeyi unutma!

HEADERS = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json"
}


mekanlar = [
    {"ad": "Kolezyum", "sehir": "Roma", "sehir_bilgi": "", "puan": 5},
    {"ad": "Machu Picchu", "sehir": "Cusco", "sehir_bilgi": "", "puan": 5},
    {"ad": "Giza Piramitleri", "sehir": "Kahire", "sehir_bilgi": "", "puan": 5},
    {"ad": "Tac Mahal", "sehir": "Agra", "sehir_bilgi": "", "puan": 4},
    {"ad": "Çin Seddi", "sehir": "Pekin", "sehir_bilgi": "", "puan": 5},
    {"ad": "Petra Antik Kenti", "sehir": "Vadi Musa", "sehir_bilgi": "", "puan": 5},
    {"ad": "Chichen Itza", "sehir": "Yucatan", "sehir_bilgi": "", "puan": 4},
    {"ad": "Akropolis", "sehir": "Atina", "sehir_bilgi": "", "puan": 4},
    {"ad": "Angkor Wat", "sehir": "Siem Reap", "sehir_bilgi": "", "puan": 5},
    {"ad": "Stonehenge", "sehir": "Salisbury", "sehir_bilgi": "", "puan": 3}
]




import os
from groq import Groq


api_anahtari = "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"
client = Groq(api_key=api_anahtari)

def metin_uret(mekan_adi, sehir):
    print(f"\n[1/5] [Yapay Zeka] {mekan_adi} için Türkçe tanıtım metni yazılıyor...")
    prompt = f"Bana {sehir} şehrinde bulunan {mekan_adi} hakkında, turistik ve ilgi çekici Türkçe bir mekan açıklaması yaz. Sadece 2 cümlelik, akıcı bir tanıtım olsun."

    try:
        # Llama 3 modelini kullanarak metin üretiyoruz
        cevap = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",# Hızlı ve başarılı bir model
        )

        uretilen_metin = cevap.choices[0].message.content.strip()
        print(f"    -> Başarılı! Üretilen Metin: {uretilen_metin}")
        return uretilen_metin

    except Exception as e:
        print(f"    -> HATA: Groq API'sine ulaşılamadı ({e})")
        return f"{mekan_adi}, {sehir} ilinde mutlaka görülmesi gereken muazzam bir turistik mekandır."

# --- YAPAY ZEKA GÖRSEL ÜRETİCİ ---
# --- GÖRSEL ÜRETİCİ (GÜNCELLENDİ) ---
def gorsel_uret(mekan_adi):
    print(f"[2/5] [Görsel] {mekan_adi} için ücretsiz test görseli indiriliyor...")

    # AI yerine şimdilik test amaçlı, mekan adına göre bir görsel çekiyoruz
    import urllib.parse
    safe_mekan_adi = urllib.parse.quote_plus(mekan_adi)
    url = f"https://loremflickr.com/800/600/{safe_mekan_adi}"
    
    dosya_adi = f"{mekan_adi.replace(' ', '_').lower()}.jpg"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response, open(dosya_adi, 'wb') as out_file:
            out_file.write(response.read())
        print(f"       -> Başarılı! Görsel indirildi: {dosya_adi}")
        return dosya_adi
    except Exception as e:
        print(f"       -> HATA: Görsel üretilemedi ({e})")
        return None

# --- STRAPI MEDYA YÜKLEME ---
def strapiye_gorsel_yukle(dosya_yolu):
    if not dosya_yolu: return None
    print(f"[3/5] {dosya_yolu} Strapi'ye yükleniyor...")
    url = f"{STRAPI_URL}/api/upload"
    auth_header = {"Authorization": f"Bearer {STRAPI_TOKEN}"}
    
    try:
        with open(dosya_yolu, 'rb') as f:
            files = {'files': (dosya_yolu, f, 'image/jpeg')}
            cevap = requests.post(url, headers=auth_header, files=files)
            
        if cevap.ok:
            return cevap.json()[0]['id']
        else:
            return None
    except Exception:
        return None

# --- DİNAMİK ŞEHİR YÖNETİMİ ---
def sehir_id_al_veya_olustur(sehir_adi, sehir_bilgi):
    print(f"{sehir_adi} şehri veritabanında kontrol ediliyor...")
    # 'Ad' yerine 'ad' olarak güncellendi
    check_url = f"{STRAPI_URL}/api/cities?filters[ad][$eq]={sehir_adi}"
    cevap = requests.get(check_url, headers=HEADERS)
    
    if cevap.ok and cevap.json().get('data'):
        return cevap.json()['data'][0]['id']
        
    create_url = f"{STRAPI_URL}/api/cities"
    # Strapi paneline göre: ad, ulke ve KisaBilgi olarak değiştirildi
    payload = {"data": {"ad": sehir_adi, "ulke": "Türkiye", "KisaBilgi": sehir_bilgi}}
    
    cevap_create = requests.post(create_url, json=payload, headers=HEADERS)
    if cevap_create.ok:
        return cevap_create.json()['data']['id']
    else:
        print(f"      -> STRAPI HATASI (Şehir Oluşturma): {cevap_create.status_code} - {cevap_create.text}")
        return None

# --- VERİTABANINA BİRLEŞİK KAYIT FONKSİYONU ---
def icerigi_strapiye_kaydet(mekan, turkce_aciklama, ingilizce_aciklama, gorsel_id, sehir_id):
    print(f"[5/5] {mekan['ad']} tüm verileriyle veritabanına yazılıyor...")
    url = f"{STRAPI_URL}/api/places"
    
    # NOT: Place tablonuzda mekanın adını tutan alanın 'ad' olduğunu varsaydım.
    # Eğer Strapi panelinde o alanın adı farklıysa (örn: Mekan_Adi) aşağıdaki "ad" kısmını değiştir.
    data_payload = {
        "ad": mekan['ad'], 
        "Aciklama": turkce_aciklama, # Paneldeki gibi büyük A
        "Puan": mekan['puan'],       # Paneldeki gibi büyük P
        "city": sehir_id             # Paneldeki gibi küçük city
    }
    
    if gorsel_id:
        # 'Kapak_Resmi' yerine paneldeki gibi birleşik 'KapakResmi' yapıldı
        data_payload["KapakResmi"] = gorsel_id
        
    payload_tr = {"data": data_payload}
    cevap_tr = requests.post(url, json=payload_tr, headers=HEADERS)
    
    if cevap_tr.ok:
        document_id = cevap_tr.json()['data']['documentId']
        print(f"      -> MÜKEMMEL! Türkçe mekan kaydedildi. (Document ID: {document_id})")
        
        ing_url = f"{STRAPI_URL}/api/places/{document_id}?locale=en"
        payload_en = {
            "data": {
                "ad": mekan['ad'],
                "Aciklama": ingilizce_aciklama 
            }
        }
        cevap_en = requests.put(ing_url, json=payload_en, headers=HEADERS)
        if cevap_en.ok:
            print(f"      -> İngilizce çeviri başarıyla sisteme bağlandı!")
        else:
            print(f"      -> HATA: İngilizce çeviri eklenemedi: {cevap_en.text}")
    else:
        print(f"      -> HATA: Türkçe mekan kaydedilemedi! API Cevabı: {cevap_tr.text}")

# --- ANA MOTORU ÇALIŞTIRMA ---
print("\n" + "="*60)
print("🚀 %100 OTONOM İÇERİK VE GÖRSEL MOTORU BAŞLATILDI")
print("="*60)

for mekan in mekanlar:
    # 1. Metni AI ile Üret
    turkce_aciklama = metin_uret(mekan['ad'], mekan['sehir'])
    
    # 2. Üretilen Metni İngilizceye Çevir
    ingilizce_aciklama = GoogleTranslator(source='tr', target='en').translate(turkce_aciklama)
    
    # 3. Görseli AI ile Çiz
    gorsel_yolu = gorsel_uret(mekan['ad'])
    
    # 4. Şehri Kontrol Et / Oluştur
    sehir_id = sehir_id_al_veya_olustur(mekan['sehir'], mekan['sehir_bilgi'])
    
    if sehir_id:
        # 5. Görseli Yükle ve Veritabanına Yaz
        gorsel_id = strapiye_gorsel_yukle(gorsel_yolu)
        icerigi_strapiye_kaydet(mekan, turkce_aciklama, ingilizce_aciklama, gorsel_id, sehir_id)
    else:
        print(f"!!! KRİTİK HATA: Şehir ID alınamadığı için {mekan['ad']} atlanıyor.")
        
    print("-" * 60)

print("\n🏁 TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI!")