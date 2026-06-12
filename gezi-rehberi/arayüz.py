import streamlit as st
import requests

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Gezi Rehberi | Travel Guide", page_icon="🌍", layout="wide")

STRAPI_URL = "http://127.0.0.1:1337"

# --- YARDIMCI FONKSİYONLAR ---

@st.cache_data(ttl=60)
def sehirleri_getir():
    """Strapi'den şehirleri çeker, karmaşık sözlük (dict) yapılarına karşı korumalıdır."""
    try:
        cevap = requests.get(f"{STRAPI_URL}/api/cities")
        if cevap.status_code == 200:
            sehirler = cevap.json().get('data', [])
            isimler = []
            for s in sehirler:
                # Strapi v4 veya v5 yapılarını kontrol et
                veri = s.get('attributes', s)
                ad = veri.get('ad')
                
                # KRİTİK DÜZELTME: Eğer 'ad' verisi bize {'ad': 'Edirne'} gibi 
                # bir paket olarak geliyorsa, o paketi açıp içindeki saf metni alıyoruz.
                if isinstance(ad, dict):
                    ad = ad.get('ad')
                    
                # Eğer başarıyla saf bir metin elde ettiysek ve boş değilse listeye ekle
                if isinstance(ad, str) and ad.strip():
                    isimler.append(ad.strip())
                    
            # Mükerrer olanları sil ve alfabetik sırala
            return sorted(list(set(isimler)))
        return []
    except Exception:
        return []

@st.cache_data(ttl=60)
def verileri_getir(secilen_sehir, dil_kodu):
    """Seçilen şehre ve dile göre Place verilerini çeker."""
    try:
        # locale parametresi ile dili belirliyoruz (tr veya en)
        url = f"{STRAPI_URL}/api/places?populate=*&locale={dil_kodu}"
        
        # Eğer spesifik bir şehir seçildiyse filtre ekle
        if secilen_sehir != "Tüm Şehirler" and secilen_sehir != "All Cities":
            url += f"&filters[city][ad][$eq]={secilen_sehir}"
            
        cevap = requests.get(url)
        if cevap.status_code == 200:
            return cevap.json().get('data', [])
        return None
    except Exception:
        return None


# --- SOL MENÜ (SIDEBAR) KONTROLLERİ ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2060/2060284.png", width=100)
st.sidebar.title("Ayarlar / Settings")

# Dil Seçimi
dil_secimi = st.sidebar.radio("Dil / Language", ["Türkçe", "English"])
dil_kodu = "en" if dil_secimi == "English" else "tr"

st.sidebar.divider()

# Dinamik Arayüz Metinleri (Seçilen dile göre değişir)
ui = {
    "baslik": "🌍 Yapay Zeka Destekli Gezi Rehberi" if dil_kodu == "tr" else "🌍 AI Powered Travel Guide",
    "alt_baslik": "*Otonom olarak üretilmiş içerikler galerisi*" if dil_kodu == "tr" else "*Gallery of autonomously generated content*",
    "filtre_baslik": "🗺️ Şehir Filtresi" if dil_kodu == "tr" else "🗺️ City Filter",
    "tum_sehirler": "Tüm Şehirler" if dil_kodu == "tr" else "All Cities",
    "puan": "Puan" if dil_kodu == "tr" else "Rating",
    "detay_buton": "Detayları Gör" if dil_kodu == "tr" else "View Details",
    "hata": "🚨 Veriler çekilemedi! Strapi sunucusu çalışmıyor olabilir." if dil_kodu == "tr" else "🚨 Data could not be fetched! Strapi server might be down.",
    "bos": "Bu şehirde henüz mekan bulunmuyor." if dil_kodu == "tr" else "No places found in this city yet."
}

# Şehir Filtresi
sehir_listesi = [ui["tum_sehirler"]] + sehirleri_getir()
secilen_sehir = st.sidebar.selectbox(ui["filtre_baslik"], sehir_listesi)


# --- ANA EKRAN ---
st.title(ui["baslik"])
st.markdown(ui["alt_baslik"])
st.divider()

# Verileri Çek
mekanlar = verileri_getir(secilen_sehir, dil_kodu)

if mekanlar is None:
    st.error(ui["hata"])
elif len(mekanlar) == 0:
    st.warning(ui["bos"])
else:
    # 3'lü ızgara (Grid) sistemi
    kolonlar = st.columns(3)
    
    for index, mekan in enumerate(mekanlar):
        veri = mekan.get('attributes', mekan)
        
        ad = veri.get('ad', '...')
        aciklama = veri.get('Aciklama', '...')
        puan = veri.get('Puan', 0)
        
        # Resim URL'sini Güvenli Çıkarma
        resim_url = "https://via.placeholder.com/400x200?text=Gorsel+Yok"
        kapak_resmi = veri.get('KapakResmi')
        
        if kapak_resmi:
            if isinstance(kapak_resmi, dict) and 'url' in kapak_resmi:
                resim_url = STRAPI_URL + kapak_resmi['url'] # v5 yapısı
            elif isinstance(kapak_resmi, dict) and 'data' in kapak_resmi and kapak_resmi['data']:
                resim_url = STRAPI_URL + kapak_resmi['data']['attributes']['url'] # v4 yapısı

        # Kolonlara sırayla yerleştirme
        with kolonlar[index % 3]:
            with st.container(border=True): 
                # DİKKAT: use_column_width hatasını çözmek için use_container_width kullanıldı
                st.image(resim_url, use_container_width=True)
                st.subheader(ad)
                st.caption(f"⭐ **{ui['puan']}:** {puan} / 5")
                
                # Açıklama çok uzunsa kırp (İlk 150 karakter)
                if aciklama:
                    kisa_aciklama = aciklama[:150] + "..." if len(aciklama) > 150 else aciklama
                    st.write(kisa_aciklama)
                
                st.button(ui["detay_buton"], key=f"btn_{mekan.get('id', index)}")