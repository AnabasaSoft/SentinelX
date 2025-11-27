import sys
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                               QFrame, QMessageBox, QHBoxLayout, QPushButton,
                               QApplication, QCheckBox) # <--- Importante QCheckBox
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
        self.combo_lang.addItem("Español", "es")
        self.combo_lang.addItem("English", "en")
        self.combo_lang.addItem("Euskara", "eu")
        self.combo_lang.setFixedWidth(200)

        # Lógica de selección inteligente
        current_lang = self.cfg_manager.get_language()
        idx = self.combo_lang.findData(current_lang)
        if idx != -1:
            self.combo_lang.setCurrentIndex(idx)
        else:
            self.combo_lang.setCurrentIndex(0)

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

        current_theme = self.cfg_manager.get_theme()
        idx = self.combo_theme.findData(current_theme)
        if idx != -1:
            self.combo_theme.setCurrentIndex(idx)
        else:
            self.combo_theme.setCurrentIndex(0)

        self.combo_theme.currentIndexChanged.connect(self.on_theme_change)
        theme_layout.addWidget(self.combo_theme)

        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # 5. COMPORTAMIENTO DEL SISTEMA (CHECKBOXES)
        layout.addSpacing(10)
        lbl_behavior = QLabel(locales.get_text("cfg_behavior_title"))
        lbl_behavior.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(lbl_behavior)

        # Checkbox: Iniciar con el sistema
        self.chk_autostart = QCheckBox(locales.get_text("cfg_autostart"))
        self.chk_autostart.setChecked(self.cfg_manager.get_autostart_enabled())
        self.chk_autostart.toggled.connect(self.on_autostart_changed)
        self.chk_autostart.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.chk_autostart)

        # Checkbox: Iniciar minimizado
        self.chk_minimized = QCheckBox(locales.get_text("cfg_start_min"))
        self.chk_minimized.setChecked(self.cfg_manager.get_start_minimized())
        self.chk_minimized.toggled.connect(self.on_minimized_changed)
        self.chk_minimized.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.chk_minimized)

        # 6. ESPACIO Y BOTÓN DE REINICIO (RECUPERADO)
        layout.addSpacing(30)

        self.btn_restart = QPushButton("🔄 " + locales.get_text("cfg_btn_restart"))
        self.btn_restart.setFixedWidth(300)
        self.btn_restart.setMinimumHeight(45)
        self.btn_restart.setCursor(QCursor(Qt.PointingHandCursor))

        # Sin estilo hardcoded para que herede el tema (Verde/Azul)
        self.btn_restart.clicked.connect(self.restart_app)

        # Alineado a la izquierda debajo de los checks
        layout.addWidget(self.btn_restart, alignment=Qt.AlignLeft)

        # 7. Nota de reinicio
        lbl_note = QLabel(locales.get_text("cfg_restart_note"))
        lbl_note.setStyleSheet("color: #888888; font-style: italic; margin-top: 10px;")
        layout.addWidget(lbl_note)

        layout.addStretch()
        self.setLayout(layout)

    # --- LOGICA ---

    def on_theme_change(self, index):
        new_theme = self.combo_theme.itemData(index)
        self.cfg_manager.set_theme(new_theme)

    def on_language_change(self, index):
        new_lang = self.combo_lang.itemData(index)
        self.cfg_manager.set_language(new_lang)

    def on_autostart_changed(self, checked):
        self.cfg_manager.set_autostart_enabled(checked)

    def on_minimized_changed(self, checked):
        self.cfg_manager.set_start_minimized(checked)

    def restart_app(self):
        """Reinicia la aplicación actual"""
        QApplication.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)
