import json
import os
import sys

# --- FUNCIÓN PARA DETECTAR RUTAS (DEV vs PROD) ---
def get_base_path():
    """
    Devuelve la ruta base correcta tanto si ejecutamos el script .py
    como si ejecutamos el binario compilado con PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        # Si estamos en el ejecutable (PyInstaller/AppImage)
        return sys._MEIPASS
    else:
        # Si estamos en desarrollo (python SentinelX.py)
        return os.path.dirname(os.path.abspath(__file__))

# Directorio donde están los json
LANG_DIR = os.path.join(get_base_path(), "lang")

# Variable global para el idioma actual
current_lang = "es"

# Diccionario en memoria
_translations = {}

def load_language(lang_code):
    """Carga el archivo JSON del idioma solicitado en memoria"""
    global _translations, current_lang

    file_path = os.path.join(LANG_DIR, f"{lang_code}.json")

    # Debug para ver qué está pasando si falla
    print(f"DEBUG: Buscando idioma en: {file_path}")

    # 1. Intentar cargar el idioma seleccionado
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                _translations = json.load(f)
            current_lang = lang_code
            print(f"Idioma cargado: {lang_code}")
            return
        except Exception as e:
            print(f"Error cargando idioma {lang_code}: {e}")
    else:
        print(f"Error: No se encuentra el archivo {file_path}")

    # 2. Fallback: Si falla, intentar cargar español por defecto
    fallback_path = os.path.join(LANG_DIR, "es.json")
    if os.path.exists(fallback_path):
        try:
            with open(fallback_path, 'r', encoding='utf-8') as f:
                _translations = json.load(f)
            current_lang = "es"
        except:
            _translations = {} # Pánico
    else:
        # Si no encuentra NI el español, dejarlo vacío (saldrán las claves)
        print("CRÍTICO: No se encuentra lang/es.json")

def get_text(key):
    """Devuelve el texto traducido o la clave si no existe"""
    return _translations.get(key, key)
