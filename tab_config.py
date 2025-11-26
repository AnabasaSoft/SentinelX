import sys
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                               QFrame, QMessageBox, QHBoxLayout, QPushButton, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

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

        # 3. SELECTOR DE IDIOMA
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

        layout.addSpacing(15)

        # 4. SELECTOR DE TEMA
        theme_layout = QHBoxLayout()
        lbl_theme = QLabel(locales.get_text("cfg_theme_label"))
        lbl_theme.setFont(QFont("Arial", 12))
        theme_layout.addWidget(lbl_theme)

        self.combo_theme = QComboBox()
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

        # 5. NOTA DE REINICIO (Opcional, ya que ahora tenemos botón)
        lbl_note = QLabel(locales.get_text("cfg_restart_note"))
        lbl_note.setStyleSheet("color: #666666; font-style: italic; margin-top: 10px;")
        layout.addWidget(lbl_note)

        layout.addSpacing(20)

        # --- 6. BOTÓN DE REINICIO (NUEVO) ---
        self.btn_restart = QPushButton("🔄 " + locales.get_text("cfg_btn_restart"))
        self.btn_restart.setFixedWidth(250)
        self.btn_restart.setMinimumHeight(45)
        # Le damos un estilo naranja para destacar que es una acción de sistema
        self.btn_restart.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-weight: bold;
                border-bottom: 3px solid #F57C00;
            }
            QPushButton:hover { background-color: #FFB74D; }
            QPushButton:pressed {
                background-color: #F57C00;
                border-bottom: none;
                padding-top: 13px;
            }
        """)
        self.btn_restart.clicked.connect(self.restart_app)
        layout.addWidget(self.btn_restart, alignment=Qt.AlignCenter) # Centrado

        layout.addStretch()
        self.setLayout(layout)

    def on_theme_change(self, index):
        new_theme = self.combo_theme.itemData(index)
        self.cfg_manager.set_theme(new_theme)
        # Ya no hace falta el print, el usuario usará el botón

    def on_language_change(self, index):
        new_lang = self.combo_lang.itemData(index)
        self.cfg_manager.set_language(new_lang)

    # --- LÓGICA DE REINICIO ---
    def restart_app(self):
        """Reinicia la aplicación actual"""
        # 1. Cerrar la instancia actual
        QApplication.quit()

        # 2. Lanzar una nueva instancia reemplazando el proceso actual
        # sys.executable es el intérprete de python (o el binario compilado)
        # sys.argv son los argumentos (el nombre del script, etc.)
        os.execl(sys.executable, sys.executable, *sys.argv)
