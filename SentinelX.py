#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
🛡️ SentinelX - The Smart Linux Firewall & Antivirus GUI
===============================================================================

A modern, intelligent, and user-friendly graphical interface for managing
Linux firewalls (Firewalld & UFW). Designed to simplify network security
for everyone.

:author:       Daniel Serrano Armenta (AnabasaSoft)
:email:        dani.eus79@gmail.com
:website:      https://danitxu79.github.io/
:github:       https://github.com/danitxu79/SentinelX
:copyright:    (c) 2025 Daniel Serrano Armenta. All rights reserved.
:license:      Dual License (LGPLv3 / Commercial)
:version:      0.3 (Beta)

===============================================================================
LICENSE NOTICE
===============================================================================
This program is offered under a Dual License model. You may choose to use it
under one of the following two licenses:

1. GNU LESSER GENERAL PUBLIC LICENSE (LGPLv3):
   You can redistribute it and/or modify it under the terms of the GNU Lesser
   General Public License as published by the Free Software Foundation, either
   version 3 of the License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU Lesser General Public License for more details.

2. COMMERCIAL LICENSE:
   If the terms of the LGPLv3 do not suit your needs (e.g., for proprietary
   closed-source integration or distribution without source code disclosure),
   please contact the author at <dani.eus79@gmail.com> to acquire a
   Commercial License.
===============================================================================
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from polkit_manager import PolkitManager

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
        color: #333333;if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Cargar config y estilos ---
    cfg = ConfigManager()
    current_theme = cfg.get_theme()

    if current_theme in THEMES:
        app.setStyleSheet(THEMES[current_theme])
    else:
        app.setStyleSheet(THEMES["dark"])

    # --- VERIFICACIÓN POLKIT (LÓGICA NUEVA) ---
    # Consultamos si ya lo tenemos marcado como instalado en config.json
    if not cfg.get_polkit_installed():
        msg_box = QMessageBox()
        msg_box.setWindowTitle(locales.get_text("polkit_title"))
        msg_box.setText(locales.get_text("polkit_msg"))
        msg_box.setIcon(QMessageBox.Question)

        btn_yes = msg_box.addButton(locales.get_text("polkit_btn_yes"), QMessageBox.YesRole)
        btn_no = msg_box.addButton(locales.get_text("polkit_btn_no"), QMessageBox.NoRole)
        msg_box.setDefaultButton(btn_yes)

        msg_box.exec()

        if msg_box.clickedButton() == btn_yes:
            # Instanciamos el manager
            from polkit_manager import PolkitManager
            polkit_mgr = PolkitManager()

            # Intentamos instalar
            if polkit_mgr.install_rule():
                # ¡ÉXITO! Guardamos en la config para no volver a preguntar
                cfg.set_polkit_installed(True)
                QMessageBox.information(None, "SentinelX", locales.get_text("polkit_success"))
            else:
                QMessageBox.warning(None, "SentinelX", locales.get_text("polkit_error"))

    # -----------------------------------

    # Icono global y ventana
    base_dir = os.path.dirname(__file__)
    icon_path = os.path.join(base_dir, "SentinelX-Icon-512.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())
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

        self.tabs = QTabWidget()
        self.tabs.setFocusPolicy(Qt.NoFocus)
        self.setCentralWidget(self.tabs)

        # Usamos las claves de traducción para los títulos de pestañas
        self.tabs.addTab(FirewallTab(), locales.get_text("tab_firewall"))
        self.tabs.addTab(AntivirusTab(), locales.get_text("tab_antivirus"))
        self.tabs.addTab(ConfigTab(), locales.get_text("tab_config"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Cargar config y estilos ---
    cfg = ConfigManager()
    current_theme = cfg.get_theme()

    if current_theme in THEMES:
        app.setStyleSheet(THEMES[current_theme])
    else:
        app.setStyleSheet(THEMES["dark"])

    # --- VERIFICACIÓN POLKIT INTELIGENTE ---
    from polkit_manager import PolkitManager
    polkit_mgr = PolkitManager()

    installed_ver = cfg.get_polkit_version()
    required_ver = polkit_mgr.get_current_version()

    # Si la versión instalada es MENOR que la requerida, forzamos update
    if installed_ver < required_ver:
        msg_box = QMessageBox()
        msg_box.setWindowTitle(locales.get_text("polkit_title"))

        # Formateamos el mensaje con el número de versión nueva
        msg_text = locales.get_text("polkit_msg").format(required_ver)
        msg_box.setText(msg_text)
        msg_box.setIcon(QMessageBox.Information) # Icono Info (menos agresivo que Question)

        btn_yes = msg_box.addButton(locales.get_text("polkit_btn_yes"), QMessageBox.YesRole)
        btn_no = msg_box.addButton(locales.get_text("polkit_btn_no"), QMessageBox.NoRole)
        msg_box.setDefaultButton(btn_yes)

        msg_box.exec()

        if msg_box.clickedButton() == btn_yes:
            if polkit_mgr.install_rule():
                # ¡ÉXITO! Guardamos la NUEVA versión (2)
                cfg.set_polkit_version(required_ver)
                QMessageBox.information(None, "SentinelX", locales.get_text("polkit_success"))
            else:
                QMessageBox.warning(None, "SentinelX", locales.get_text("polkit_error"))

    # Icono global y ventana
    base_dir = os.path.dirname(__file__)
    icon_path = os.path.join(base_dir, "SentinelX-Icon-512.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())
