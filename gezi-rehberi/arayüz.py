import streamlit as st
import requests

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Gezi Rehberi | Travel Guide", page_icon="🌍", layout="wide")

STRAPI_URL = "http://127.0.0.1:1337"

# --- YARDIMCI FONKSİYONLAR ---

@st.cache_data(ttl=5)
def verileri_getir(dil_kodu):
    """Seçilen dile göre tüm Place verilerini Strapi'den çeker."""
    try:
        url = f"{STRAPI_URL}/api/places"
        params = {
            "populate": "*",
            "locale": dil_kodu
        }
        cevap = requests.get(url, params=params)
        if cevap.status_code == 200:
            return cevap.json().get('data', [])
        return None
    except Exception as e:
        return None

# --- SOL MENÜ (SIDEBAR) KONTROLLERİ ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2060/2060284.png", width=100)
st.sidebar.title("Ayarlar / Settings")

dil_secimi = st.sidebar.radio("Dil / Language", ["Türkçe", "English"])
dil_kodu = "en" if dil_secimi == "English" else "tr"

st.sidebar.divider()

ui = {
    "baslik": "🌍 Yapay Zeka Destekli Gezi Rehberi" if dil_kodu == "tr" else "🌍 AI Powered Travel Guide",
    "alt_baslik": "*Otonom olarak üretilmiş içerikler galerisi*" if dil_kodu == "tr" else "*Gallery of autonomously generated content*",
    "filtre_mekan": "🏛️ Mekan Filtresi" if dil_kodu == "tr" else "🏛️ Place Filter",
    "tum_mekanlar": "Tüm Mekanlar" if dil_kodu == "tr" else "All Places",
    "puan": "Puan" if dil_kodu == "tr" else "Rating",
    "detay_buton": "Detayları Gör" if dil_kodu == "tr" else "View Details",
    "hata": "🚨 Veriler çekilemedi! Strapi sunucusu çalışmıyor olabilir." if dil_kodu == "tr" else "🚨 Data could not be fetched! Strapi server might be down.",
    "bos": "Seçilen filtrede mekan bulunmuyor." if dil_kodu == "tr" else "No places found in this filter."
}

# --- VERİLERİ (GÜNCEL LİSTE - 8 MEKAN) ---
if dil_kodu == "tr":
    mekanlar_listesi = [
        {"id": 1, "attributes": {"ad": "Efes Antik Kenti", "Aciklama": "İzmir'in Selçuk ilçesinde bulunan büyüleyici tarihi antik kent.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1585464159976-13d6a457497d?q=80&w=400"}}}}},
        {"id": 2, "attributes": {"ad": "Kapadokya", "Aciklama": "Peri bacaları ve sıcak hava balonlarıyla ünlü masalsı bölge.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?q=80&w=400"}}}}},
       
        {"id": 4, "attributes": {"ad": "Ayasofya", "Aciklama": "İstanbul'un tarihi ve mimari simgesi, büyüleyici atmosfer.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1541432901042-0d8502573212?q=80&w=400"}}}}},
        {"id": 5, "attributes": {"ad": "Tac Mahal", "Aciklama": "Hindistan'ın Agra şehrinde bulunan anıt mezar, aşkın sembolü.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1564507592333-c64657158f01?q=80&w=400"}}}}},
        {"id": 6, "attributes": {"ad": "Petra", "Aciklama": "Ürdün'de kayalara oyulmuş antik şehir.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1574229672530-901ad9823467?q=80&w=400"}}}}},
        {"id": 7, "attributes": {"ad": "Çin Seddi", "Aciklama": "Dünyanın en uzun savunma duvarı, tarihi harika.", "Puan": 4, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?q=80&w=400"}}}}},
        {"id": 8, "attributes": {"ad": "Angkor Wat", "Aciklama": "Kamboçya'da yer alan devasa tapınak kompleksi.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?q=80&w=400"}}}}},
        {"id": 9, "attributes": {"ad": "Eyfel Kulesi", "Aciklama": "Paris'in simgesi, dünyanın en çok ziyaret edilen yapılarından.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?q=80&w=400"}}}}},
        {"id": 10, "attributes": {"ad": "Machu Picchu", "Aciklama": "And Dağları'nda yer alan antik İnka şehri.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1587595431973-160d0d94add1?q=80&w=400"}}}}},
        {"id": 11, "attributes": {"ad": "Giza Piramitleri", "Aciklama": "Antik dünyanın yedi harikasından biri, Mısır.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1503174971373-b1f69850b8e3?q=80&w=400"}}}}}
    ]
else:
    mekanlar_listesi = [
        {"id": 1, "attributes": {"ad": "Ephesus Ancient City", "Aciklama": "Historical ancient city located in Selcuk, Izmir.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1585464159976-13d6a457497d?q=80&w=400"}}}}},
        {"id": 2, "attributes": {"ad": "Cappadocia", "Aciklama": "Fairy tale region famous for fairy chimneys and hot air balloons.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?q=80&w=400"}}}}},
        
        {"id": 4, "attributes": {"ad": "Hagia Sophia", "Aciklama": "Iconic historical and architectural symbol of Istanbul.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1541432901042-0d8502573212?q=80&w=400"}}}}},
        {"id": 5, "attributes": {"ad": "Taj Mahal", "Aciklama": "Famous monument in Agra, India, symbol of eternal love.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1564507592333-c64657158f01?q=80&w=400"}}}}},
        {"id": 6, "attributes": {"ad": "Petra", "Aciklama": "Ancient city carved into rock in Jordan.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1574229672530-901ad9823467?q=80&w=400"}}}}},
        {"id": 7, "attributes": {"ad": "Great Wall of China", "Aciklama": "The longest defensive wall in the world, a historical wonder.", "Puan": 4, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?q=80&w=400"}}}}},
        {"id": 8, "attributes": {"ad": "Angkor Wat", "Aciklama": "Massive temple complex located in Cambodia.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?q=80&w=400"}}}}},
        {"id": 9, "attributes": {"ad": "Eiffel Tower", "Aciklama": "Icon of Paris, one of the most visited structures in the world.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?q=80&w=400"}}}}},
        {"id": 10, "attributes": {"ad": "Machu Picchu", "Aciklama": "Ancient Incan city set high in the Andes Mountains.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1587595431973-160d0d94add1?q=80&w=400"}}}}},
        {"id": 11, "attributes": {"ad": "Pyramids of Giza", "Aciklama": "One of the seven wonders of the ancient world, Egypt.", "Puan": 5, "KapakResmi": {"data": {"attributes": {"url": "https://images.unsplash.com/photo-1503174971373-b1f69850b8e3?q=80&w=400"}}}}}]
mekanlar = mekanlar_listesi

mevcut_mekan_isimleri = []
for m in mekanlar_listesi:
    veri = m.get('attributes', m)
    ad_temp = veri.get('ad', '')
    if ad_temp and isinstance(ad_temp, str):
        mevcut_mekan_isimleri.append(ad_temp.strip())
mevcut_mekan_isimleri = sorted(list(set(mevcut_mekan_isimleri)))

secilen_mekan = st.sidebar.selectbox(ui["filtre_mekan"], [ui["tum_mekanlar"]] + mevcut_mekan_isimleri)

if secilen_mekan != ui["tum_mekanlar"]:
    mekanlar_listesi = [
        m for m in mekanlar_listesi 
        if m.get('attributes', m).get('ad', '').strip() == secilen_mekan
    ]

st.title(ui["baslik"])
st.markdown(ui["alt_baslik"])
st.divider()

if mekanlar is None:
    st.error(ui["hata"])
elif len(mekanlar_listesi) == 0:
    st.warning(ui["bos"])
else:
    kolonlar = st.columns(3)
    
    for index, mekan in enumerate(mekanlar_listesi):
        veri = mekan.get('attributes', mekan)
        ad = veri.get('ad', '...')
        aciklama = veri.get('Aciklama', '...')
        puan = veri.get('Puan', 0)
        
        # --- GÜNCEL GÖRSEL İŞLEME MANTIĞI ---
        try:
            # Önce yolu alıyoruz
            temp_url = veri['KapakResmi']['data']['attributes']['url']
            
            # Eğer 'http' ile başlıyorsa tam linktir (Unsplash), değilse Strapi yoludur
            if temp_url.startswith('http'):
                resim_url = temp_url
            else:
                resim_url = STRAPI_URL + temp_url
        except:
            resim_url = "https://via.placeholder.com/400x200?text=Gorsel+Yok"
        # -----------------------------------
        
        with kolonlar[index % 3]:
            with st.container(border=True): 
                # HATA AYIKLAMA: Görselin üstüne linki yazdırıyoruz (Bir kerelik)
                # st.write(f"Yüklenmeye çalışılan: {resim_url}") 
                
                st.image(resim_url, use_container_width=True)
                st.subheader(ad)
                st.caption(f"⭐ **{ui['puan']}:** {puan} / 5")
                
                if aciklama:
                    kisa_aciklama = aciklama[:150] + "..." if len(aciklama) > 150 else aciklama
                    st.write(kisa_aciklama)
                
                st.button(ui["detay_buton"], key=f"btn_{mekan.get('id', index)}")