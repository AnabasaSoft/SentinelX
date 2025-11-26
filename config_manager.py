import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # 1. Definimos la ruta estándar: /home/usuario/.config/SentinelX
        self.config_dir = Path.home() / ".config" / "SentinelX"
        self.config_file = self.config_dir / "config.json"

        # 2. Configuración por defecto
        self.config = {
            "language": "es",
            "theme": "dark",
            "custom_rules": {},
            "known_networks": {}
        }

        # 3. Inicializamos (Creamos carpeta y cargamos)
        self.init_storage()
        self.load_config()

    def init_storage(self):
        """Crea la carpeta en .config si no existe"""
        try:
            if not self.config_dir.exists():
                print(f"Creando directorio de configuración: {self.config_dir}")
                os.makedirs(self.config_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creando directorio config: {e}")

    def load_config(self):
        """Carga el JSON desde la ruta de usuario"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"Error cargando config: {e}")

        # --- BLINDAJE ---
        # Aseguramos que existan las claves críticas si el archivo es viejo
        if "custom_rules" not in self.config:
            self.config["custom_rules"] = {}
        if "known_networks" not in self.config:
            self.config["known_networks"] = {}
        if "theme" not in self.config:
            self.config["theme"] = "dark"

    def save_config(self):
        """Guarda en /home/usuario/.config/SentinelX/config.json"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error guardando config: {e}")

    # --- Getters y Setters (Sin cambios) ---

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

    # --- Gestión de Reglas ---

    def save_rule_description(self, port, protocol, description, direction="IN"):
        if not description: return
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

    # --- Gestión de Redes ---

    def get_network_zone(self, network_name):
        return self.config.get("known_networks", {}).get(network_name, None)

    def save_network_zone(self, network_name, zone):
        if "known_networks" not in self.config:
            self.config["known_networks"] = {}
        self.config["known_networks"][network_name] = zone
        self.save_config()

    # --- Gestión de Estado Polkit ---
    def get_polkit_installed(self):
        """Devuelve True si ya marcamos la regla como instalada"""
        return self.config.get("polkit_installed", False)

    def set_polkit_installed(self, installed=True):
        self.config["polkit_installed"] = installed
        self.save_config()

    def get_polkit_version(self):
        """Devuelve la versión de la regla instalada. 0 si no existe."""
        return self.config.get("polkit_version", 0)

    def set_polkit_version(self, version):
        """Guarda la versión actual"""
        self.config["polkit_version"] = version
        self.save_config()
