import requests
import folium
from folium.plugins import AntPath
import time
import webbrowser  # Tarayıcıyı otomatik açmak için

# Haritayı başlat
m = folium.Map(location=[20, 0], zoom_start=2)

# Haritanın HTML dosyası
html_file = "live_flights_map.html"

# Tarayıcıda ilk seferde açıldı mı kontrol
browser_opened = False

# API'den canlı veri çekme ve haritayı güncelleme
while True:
    # OpenSky API'ye istek gönder
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("Canlı veri alındı!")

        # Haritayı her yenilemede sıfırla
        m = folium.Map(location=[20, 0], zoom_start=2)

        # İlk 5 uçuşu haritaya ekle
        for flight in data['states'][:5]:  # İlk 5 uçuş
            flight_code = flight[1]  # Uçuş kodu
            longitude = flight[5]    # Şu anki konum boylam
            latitude = flight[6]     # Şu anki konum enlem

            # Örnek olarak kalkış ve varış noktaları
            origin_longitude = longitude - 5
            origin_latitude = latitude - 5
            dest_longitude = longitude + 5
            dest_latitude = latitude + 5

            # Eğer enlem ve boylam bilgisi varsa, işleme devam
            if latitude and longitude:
                # Kalkış Noktası (Yeşil işaretçi)
                folium.Marker(
                    location=[origin_latitude, origin_longitude],
                    popup=f"Kalkış: {flight_code}",
                    icon=folium.Icon(color="green", icon="home")
                ).add_to(m)

                # Varış Noktası (Kırmızı işaretçi)
                folium.Marker(
                    location=[dest_latitude, dest_longitude],
                    popup=f"Varış: {flight_code}",
                    icon=folium.Icon(color="red", icon="flag")
                ).add_to(m)

                # Kalkıştan varışa bir çizgi (Patika)
                AntPath(
                    locations=[
                        [origin_latitude, origin_longitude],
                        [latitude, longitude],  # Şu anki konum
                        [dest_latitude, dest_longitude]
                    ],
                    color="blue",
                    weight=2.5,
                    opacity=0.7
                ).add_to(m)

        # Haritayı kaydet
        m.save(html_file)
        print(f"Harita güncellendi: {html_file}")

        # İlk kez çalıştırıldığında tarayıcıyı aç
        if not browser_opened:
            webbrowser.open(html_file)  # Varsayılan tarayıcıda açar
            browser_opened = True

        # Verileri 15 saniyede bir güncelle
        time.sleep(15)
    else:
        print(f"API isteği başarısız oldu! Hata kodu: {response.status_code}")
        break

