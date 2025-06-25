from kivy_garden.mapview import MapView, MapMarker
from kivymd.uix.screen import MDScreen
import json
import os

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

class MapScreen(MDScreen):
    current_user = None

    def on_enter(self):
        self.update_markers()

    def update_markers(self):
        # Garante que o id map_box existe
        if "map_box" not in self.ids:
            print("ERRO: id 'map_box' não encontrado na tela do mapa!")
            return

        self.ids.map_box.clear_widgets()
        mapview = MapView(zoom=4, lat=-15.78, lon=-47.93)  # Centro do Brasil
        users = load_users()
        for username, user in users.items():
            lat = user.get("lat")
            lon = user.get("lon")
            if lat is not None and lon is not None:
                marker = MapMarker(lat=lat, lon=lon)
                mapview.add_marker(marker)
        self.ids.map_box.add_widget(mapview)
