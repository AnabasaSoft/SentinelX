# locales.py
import json
import os

# Directorio donde están los json
LANG_DIR = os.path.join(os.path.dirname(__file__), "lang")

# Variable global para el idioma actual
current_lang = "es"

# Diccionario en memoria
_translations = {}

def load_language(lang_code):
    """Carga el archivo JSON del idioma solicitado en memoria"""
    global _translations, current_lang

    file_path = os.path.join(LANG_DIR, f"{lang_code}.json")

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

    # 2. Fallback: Si falla, intentar cargar español por defecto
    print(f"Aviso: No se encontró idioma {lang_code}, usando fallback (es).")
    fallback_path = os.path.join(LANG_DIR, "es.json")
    if os.path.exists(fallback_path):
        try:
            with open(fallback_path, 'r', encoding='utf-8') as f:
                _translations = json.load(f)
            current_lang = "es"
        except:
            _translations = {} # Pánico: diccionario vacío

def get_text(key):
    """Devuelve el texto traducido o la clave si no existe"""
    return _translations.get(key, key)
