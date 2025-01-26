import pandas as pd
import folium
import webbrowser

# Veri setini yükle
df = pd.read_csv("flights.csv")

# Harita oluştur
m = folium.Map(location=[41.0082, 28.9784], zoom_start=4)  # Haritanın başlangıç noktası

# Rotayı çiz
for _, row in df.iterrows():
    folium.Marker([row['departure_lat'], row['departure_lon']], popup=f"Departure: {row['departure_city']}").add_to(m)
    folium.Marker([row['arrival_lat'], row['arrival_lon']], popup=f"Arrival: {row['arrival_city']}").add_to(m)
    folium.PolyLine([[row['departure_lat'], row['departure_lon']], 
                     [row['arrival_lat'], row['arrival_lon']]], color="blue").add_to(m)

# Haritayı kaydet ve görüntüle
m.save("flight_routes.html")
print("Harita oluşturuldu: flight_routes.html")
webbrowser.open("flight_routes.html")

# denemeS
