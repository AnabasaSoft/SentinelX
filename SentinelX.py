import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

# --- Módulos de lógica ---
from config_manager import ConfigManager
import locales  # Importamos el módulo de textos

# Cargamos el idioma ANTES de importar las pestañas para que cojan el texto correcto
cfg = ConfigManager()
selected_lang = cfg.get_language()
locales.current_lang = selected_lang # Seteamos la variable global del módulo locales

# --- Módulos de UI ---
from tab_firewall import FirewallTab
from tab_antivirus import AntivirusTab
from tab_config import ConfigTab

# -----------------------------------------------------
# ESTILO OSCURO
# -----------------------------------------------------
DARK_STYLE_SHEET = """
    /* CONFIGURACIÓN GLOBAL DE VENTANAS Y CONTENEDORES */
    QMainWindow, QWidget, QDialog {
        background-color: #333333;
        color: #F5F5F5;
        selection-background-color: #4CAF50;
    }

    /* PANELES Y MARCOS */
    QFrame {
        background-color: #3a3a3a;
        border: none;
    }

    /* BOTONES ESTÁNDAR */
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
        min-height: 24px;
    }
    QPushButton:hover {
        background-color: #388E3C;
    }
    QPushButton:pressed {
        background-color: #66BB6A;
    }

    /* BARRAS DE PESTAÑAS PRINCIPALES */
    QTabWidget::pane {
        border: 1px solid #444444;
    }
    QTabBar::tab {
        background: #3a3a3a;
        color: #CCCCCC;
        padding: 8px 15px;
        border: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;

        /* --- ¡ESTO ES LO QUE FALTABA! --- */
        outline: 0px; /* Elimina el subrayado/recuadro de foco */
    }
    QTabBar::tab:selected {
        background: #4CAF50;
        color: white;
        font-weight: bold;
        border: none; /* Asegura que no haya borde al seleccionarse */
    }

    /* RADIO BUTTONS */
    QRadioButton {
        color: #F5F5F5;
        spacing: 5px;
    }
    QRadioButton::indicator {
        width: 14px;
        height: 14px;
        border-radius: 7px;
        background-color: #555555;
        border: 1px solid #777777;
    }
    QRadioButton::indicator:checked {
        background-color: #4CAF50;
        border: 1px solid #388E3C;
    }
"""

# -----------------------------------------------------
# ESTILO CLARO
# -----------------------------------------------------
LIGHT_STYLE_SHEET = """
    QMainWindow, QWidget, QDialog {
        background-color: #F0F0F0;
        color: #333333;
        selection-background-color: #4CAF50;
    }

    QFrame {
        background-color: #FFFFFF;
        border: none;
    }

    QPushButton {
        background-color: #007ACC;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
        min-height: 24px;
    }
    QPushButton:hover {
        background-color: #005A99;
    }
    QPushButton:pressed {
        background-color: #3399FF;
    }

    QTabWidget::pane {
        border: 1px solid #CCCCCC;
    }
    QTabBar::tab {
        background: #E0E0E0;
        color: #555555;
        padding: 8px 15px;
        border: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;

        /* --- ¡ESTO ES LO QUE FALTABA! --- */
        outline: 0px; /* Elimina el subrayado/recuadro de foco */
    }
    QTabBar::tab:selected {
        background: #FFFFFF;
        color: #333333;
        font-weight: bold;
        border: none; /* Asegura que no haya borde al seleccionarse */
    }

    QLabel {
        color: #333333;
    }

    QComboBox {
        background-color: white;
        color: #333333;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        padding: 3px;
    }

    QRadioButton {
        color: #333333;
        spacing: 5px;
    }
    QRadioButton::indicator {
        width: 14px;
        height: 14px;
        border-radius: 7px;
        background-color: #CCCCCC;
        border: 1px solid #AAAAAA;
    }
    QRadioButton::indicator:checked {
        background-color: #007ACC;
        border: 1px solid #005A99;
    }
"""

THEMES = {
    "dark": DARK_STYLE_SHEET,
    "light": LIGHT_STYLE_SHEET
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Usamos el texto traducido
        self.setWindowTitle(locales.get_text("app_title"))
        self.setMinimumSize(800, 600)

        # ... (Resto del código de icono igual) ...
        base_dir = os.path.dirname(__file__)
        icon_path = os.path.join(base_dir, "SentinelX-Icon-512.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.tabs = QTabWidget()
        self.tabs.setFocusPolicy(Qt.NoFocus)
        self.setCentralWidget(self.tabs)

        # Usamos las claves de traducción para los títulos de pestañas
        self.tabs.addTab(FirewallTab(), locales.get_text("tab_firewall"))
        self.tabs.addTab(AntivirusTab(), locales.get_text("tab_antivirus"))
        self.tabs.addTab(ConfigTab(), locales.get_text("tab_config"))

# ... (Resto del main igual) ...
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Cargar la configuración y el tema ---
    cfg = ConfigManager()
    current_theme = cfg.get_theme() # Obtenemos el tema (ej: "dark")

    # Aplicar el estilo
    if current_theme in THEMES:
        app.setStyleSheet(THEMES[current_theme])
    else:
        # Fallback al oscuro si hay un error en la config
        app.setStyleSheet(THEMES["dark"])

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())
