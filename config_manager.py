import json
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        # Configuración por defecto completa
        self.config = {
            "language": "es",
            "theme": "dark",
            "custom_rules": {},
            "known_networks": {}
        }
        self.load_config()

    def load_config(self):
        """Carga la configuración y asegura que existan todas las claves necesarias"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"Error cargando config: {e}")

        # --- BLINDAJE ---
        # Si cargamos un config.json viejo que no tenía 'custom_rules',
        # lo creamos ahora para evitar el KeyError.
        if "custom_rules" not in self.config:
            self.config["custom_rules"] = {}

        # Si faltan otras claves futuras, las aseguramos aquí también
        if "theme" not in self.config:
            self.config["theme"] = "dark"

        if "known_networks" not in self.config:
            self.config["known_networks"] = {}

    def save_config(self):
        """Guarda la configuración actual en disco"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error guardando config: {e}")

    # --- Getters y Setters ---

    def get_language(self):
        return self.config.get("language", "es")

    def set_language(self, lang_code):
        self.config["language"] = lang_code
        self.save_config()

    def get_theme(self):
        return self.config.get("theme", "dark")

    def set_theme(self, theme_name):
        self.config["theme"] = theme_name
        self.save_config()

   # Modificamos para aceptar 'direction' (IN o OUT)
    def save_rule_description(self, port, protocol, description, direction="IN"):
        if not description: return
        # La clave ahora incluye la dirección: "IN:80/tcp" o "OUT:80/tcp"
        key = f"{direction}:{port}/{protocol}"

        if "custom_rules" not in self.config:
            self.config["custom_rules"] = {}

        self.config["custom_rules"][key] = description
        self.save_config()

    def get_rule_description(self, port, protocol, direction="IN"):
        key = f"{direction}:{port}/{protocol}"
        return self.config.get("custom_rules", {}).get(key, "")

    def delete_rule_description(self, port, protocol, direction="IN"):
        key = f"{direction}:{port}/{protocol}"
        if "custom_rules" in self.config and key in self.config["custom_rules"]:
            del self.config["custom_rules"][key]
            self.save_config()

    # --- GESTIÓN DE REDES CONOCIDAS ---
    def get_network_zone(self, network_name):
        """Devuelve 'public', 'home' o None si es nueva"""
        return self.config["known_networks"].get(network_name, None)

    def save_network_zone(self, network_name, zone):
        self.config["known_networks"][network_name] = zone
        self.save_config()
