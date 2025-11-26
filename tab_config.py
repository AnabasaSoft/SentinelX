import sys
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                               QFrame, QMessageBox, QHBoxLayout, QPushButton, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor

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
        # Añadimos (Texto Visible, Clave Interna)
        self.combo_lang.addItem("Español", "es")
        self.combo_lang.addItem("English", "en")
        self.combo_lang.addItem("Euskara", "eu") # <--- Asegúrate de que esté aquí
        self.combo_lang.setFixedWidth(200)

        # --- CORRECCIÓN LÓGICA DE SELECCIÓN ---
        # Obtenemos el idioma guardado (ej: "eu")
        current_lang = self.cfg_manager.get_language()

        # Buscamos en qué índice del combo está ese código
        index = self.combo_lang.findData(current_lang)

        # Si lo encuentra (index != -1), lo selecciona. Si no, deja el 0.
        if index != -1:
            self.combo_lang.setCurrentIndex(index)
        else:
            self.combo_lang.setCurrentIndex(0)
        # --------------------------------------

        self.combo_lang.currentIndexChanged.connect(self.on_language_change)
        lang_layout.addWidget(self.combo_lang)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        # 4. SELECTOR DE TEMA
        theme_layout = QHBoxLayout()
        lbl_theme = QLabel(locales.get_text("cfg_theme_label"))
        lbl_theme.setFont(QFont("Arial", 12))
        theme_layout.addWidget(lbl_theme)

        self.combo_theme = QComboBox()
        self.combo_theme.addItem(locales.get_text("theme_dark"), "dark")
        self.combo_theme.addItem(locales.get_text("theme_light"), "light")
        self.combo_theme.setFixedWidth(200)

        # --- MISMA CORRECCIÓN PARA EL TEMA ---
        current_theme = self.cfg_manager.get_theme()
        idx = self.combo_theme.findData(current_theme)
        if idx != -1:
            self.combo_theme.setCurrentIndex(idx)
        else:
            self.combo_theme.setCurrentIndex(0)
        # -------------------------------------

        self.combo_theme.currentIndexChanged.connect(self.on_theme_change)
        theme_layout.addWidget(self.combo_theme)

        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # 5. Espacio y Botón
        layout.addSpacing(30)

        self.btn_restart = QPushButton("🔄 " + locales.get_text("cfg_btn_restart"))
        self.btn_restart.setFixedWidth(300)
        self.btn_restart.setMinimumHeight(45)
        self.btn_restart.setCursor(QCursor(Qt.PointingHandCursor))

        self.btn_restart.clicked.connect(self.restart_app)

        layout.addWidget(self.btn_restart, alignment=Qt.AlignLeft)

        # 6. Nota de reinicio
        lbl_note = QLabel(locales.get_text("cfg_restart_note"))
        lbl_note.setStyleSheet("color: #888888; font-style: italic; margin-top: 10px;")
        layout.addWidget(lbl_note)

        layout.addStretch()
        self.setLayout(layout)

    def on_theme_change(self, index):
        # Usamos itemData para obtener la clave ("dark", "light") no el texto traducido
        new_theme = self.combo_theme.itemData(index)
        self.cfg_manager.set_theme(new_theme)

    def on_language_change(self, index):
        # Usamos itemData para obtener el código ("es", "en", "eu")
        new_lang = self.combo_lang.itemData(index)
        self.cfg_manager.set_language(new_lang)

    def restart_app(self):
        """Reinicia la aplicación actual"""
        QApplication.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)
