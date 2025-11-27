import json
import os
import sys
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # 1. Rutas de Configuración Principal
        self.config_dir = Path.home() / ".config" / "SentinelX"
        self.config_file = self.config_dir / "config.json"

        # 2. Rutas de Auto-Arranque (ESTO ES LO QUE TE FALTABA)
        self.autostart_dir = Path.home() / ".config" / "autostart"
        self.autostart_file = self.autostart_dir / "sentinelx.desktop"

        # 3. Configuración por defecto
        self.config = {
            "language": "es",
            "theme": "dark",
            "start_minimized": False,
            "custom_rules": {},
            "known_networks": {},
            "polkit_installed": False,
            "polkit_version": 0
        }

        # 4. Inicialización
        self.init_storage()
        self.load_config()

    def init_storage(self):
        """Crea la carpeta en .config si no existe"""
        try:
            if not self.config_dir.exists():
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

        # --- BLINDAJE DE CLAVES ---
        if "custom_rules" not in self.config: self.config["custom_rules"] = {}
        if "known_networks" not in self.config: self.config["known_networks"] = {}
        if "theme" not in self.config: self.config["theme"] = "dark"
        if "start_minimized" not in self.config: self.config["start_minimized"] = False

    def save_config(self):
        """Guarda en /home/usuario/.config/SentinelX/config.json"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error guardando config: {e}")

    # --- Getters y Setters Básicos ---

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

    def get_polkit_version(self):
        return self.config.get("polkit_version", 0)

    def set_polkit_version(self, version):
        self.config["polkit_version"] = version
        self.save_config()

    def get_polkit_installed(self):
        # Mantenemos compatibilidad hacia atrás si existe el booleano viejo
        return self.config.get("polkit_installed", False) or (self.get_polkit_version() > 0)

    def set_polkit_installed(self, installed=True):
        self.config["polkit_installed"] = installed
        self.save_config()

    # --- Gestión de Minimizado ---
    def get_start_minimized(self):
        return self.config.get("start_minimized", False)

    def set_start_minimized(self, value):
        self.config["start_minimized"] = value
        self.save_config()

    # --- Gestión de Auto-Arranque (AUTOSTART) ---

    def get_autostart_enabled(self):
        """Devuelve True si el archivo .desktop existe en autostart"""
        # AHORA SÍ FUNCIONARÁ PORQUE autostart_file ESTÁ DEFINIDO EN INIT
        return self.autostart_file.exists()

    def set_autostart_enabled(self, enable):
        if enable:
            self._create_autostart_entry()
        else:
            self._remove_autostart_entry()

    def _create_autostart_entry(self):
        if not self.autostart_dir.exists():
            os.makedirs(self.autostart_dir, exist_ok=True)

        # Detectamos el ejecutable correcto
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = f"{sys.executable} {os.path.abspath(sys.argv[0])}"

        # Icono
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SentinelX-Icon-512.png")

        content = f"""[Desktop Entry]
Type=Application
Name=SentinelX
Comment=Linux Smart Firewall & Antivirus
Exec={exe_path}
Icon={icon_path}
X-GNOME-Autostart-enabled=true
Terminal=false
Categories=System;Security;
"""
        try:
            with open(self.autostart_file, "w") as f:
                f.write(content)
            os.chmod(self.autostart_file, 0o755)
        except Exception as e:
            print(f"Error creando autostart: {e}")

    def _remove_autostart_entry(self):
        try:
            if self.autostart_file.exists():
                os.remove(self.autostart_file)
        except Exception as e:
            print(f"Error borrando autostart: {e}")

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
