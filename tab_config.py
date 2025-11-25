from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                               QFrame, QMessageBox, QHBoxLayout)
from PySide6.QtGui import QFont

# Importamos nuestros nuevos módulos
import locales
from config_manager import ConfigManager

class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.cfg_manager = ConfigManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 1. Título
        title = QLabel(locales.get_text("cfg_title"))
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)

        # 2. Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(line)

        # 3. SELECTOR DE IDIOMA (Existente)
        lang_layout = QHBoxLayout()
        lbl_lang = QLabel(locales.get_text("cfg_lang_label"))
        lbl_lang.setFont(QFont("Arial", 12))
        lang_layout.addWidget(lbl_lang)

        self.combo_lang = QComboBox()
        self.combo_lang.addItem("Español", "es")
        self.combo_lang.addItem("English", "en")
        self.combo_lang.setFixedWidth(150)

        current_lang = self.cfg_manager.get_language()
        if current_lang == "en":
            self.combo_lang.setCurrentIndex(1)
        else:
            self.combo_lang.setCurrentIndex(0)

        self.combo_lang.currentIndexChanged.connect(self.on_language_change)
        lang_layout.addWidget(self.combo_lang)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        layout.addSpacing(15) # Separación vertical

        # 4. SELECTOR DE TEMA (NUEVO)
        theme_layout = QHBoxLayout()
        lbl_theme = QLabel(locales.get_text("cfg_theme_label"))
        lbl_theme.setFont(QFont("Arial", 12))
        theme_layout.addWidget(lbl_theme)

        self.combo_theme = QComboBox()
        # Añadimos los temas con sus datos asociados
        self.combo_theme.addItem(locales.get_text("theme_dark"), "dark")
        self.combo_theme.addItem(locales.get_text("theme_light"), "light")
        self.combo_theme.setFixedWidth(150)

        current_theme = self.cfg_manager.get_theme()
        if current_theme == "light":
            self.combo_theme.setCurrentIndex(1)
        else:
            self.combo_theme.setCurrentIndex(0)

        self.combo_theme.currentIndexChanged.connect(self.on_theme_change)
        theme_layout.addWidget(self.combo_theme)

        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # 5. Nota de reinicio (MODIFICADA para incluir el tema)
        lbl_note = QLabel(locales.get_text("cfg_restart_note"))
        lbl_note.setStyleSheet("color: #666666; font-style: italic; margin-top: 10px;")
        layout.addWidget(lbl_note)

        layout.addStretch()
        self.setLayout(layout)

    # NUEVO método para manejar el cambio de tema
    def on_theme_change(self, index):
        """Guarda el tema seleccionado"""
        # Obtenemos el valor ('dark' o 'light') asociado al índice
        new_theme = self.combo_theme.itemData(index)
        self.cfg_manager.set_theme(new_theme)
        print(f"Tema cambiado a {new_theme}. Requiere reinicio.")

    # Mantenemos el método on_language_change (solo hay que renombrar la variable)
    def on_language_change(self, index):
        new_lang = self.combo_lang.itemData(index)
        self.cfg_manager.set_language(new_lang)
        print(f"Idioma cambiado a {new_lang}. Requiere reinicio.")
