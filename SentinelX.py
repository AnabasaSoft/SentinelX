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
:version:      1.4.1

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
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QMessageBox, QSplashScreen)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QEventLoop, QTimer

from polkit_manager import PolkitManager

# --- Módulos de lógica ---
from config_manager import ConfigManager
import locales

# --- CARGA DE IDIOMA MEJORADA ---
cfg = ConfigManager()
selected_lang = cfg.get_language()

# Ahora llamamos a la función de carga
locales.load_language(selected_lang)

# --- Módulos de UI ---
from tab_firewall import FirewallTab
from tab_antivirus import AntivirusTab
from tab_config import ConfigTab
from tab_help import HelpTab
from tab_quarantine import QuarantineTab

# -----------------------------------------------------
# ESTILO OSCURO (MODERNO)
# -----------------------------------------------------
DARK_STYLE_SHEET = """
    /* --- VENTANA PRINCIPAL --- */
    QMainWindow, QWidget, QDialog {
        background-color: #2b2b2b; /* Un gris un poco más profundo */
        color: #F0F0F0;
        font-family: "Segoe UI", "Helvetica Neue", "Arial", sans-serif;
        font-size: 14px;
    }

    /* --- PANELES Y TARJETAS --- */
    QFrame {
        background-color: #333333;
        border-radius: 8px; /* Bordes redondeados en los paneles */
    }

    /* --- BOTONES MODERNOS (VERDES) --- */
    QPushButton {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 10px 20px;

        /* Truco para simular profundidad/sombra sutil */
        border-bottom: 3px solid #2E7D32;
    }

    QPushButton:hover {
        background-color: #57B85B; /* Un poco más brillante al pasar el ratón */
        border-bottom: 3px solid #36893B;
    }

    QPushButton:pressed {
        background-color: #2E7D32; /* Color más oscuro al presionar */
        border-bottom: none; /* Quitamos el borde inferior para simular que baja */

        /* Desplazamos el texto para efecto de "hundimiento" */
        padding-top: 13px;
        padding-bottom: 7px;
    }

    /* Botones Peligrosos (Rojos - Eliminación/Parada) */
    /* Usamos el selector de atributo para detectar botones rojos por su estilo inline anterior */
    QPushButton[style*="background-color: #d32f2f"] {
        background-color: #E53935 !important;
        border-bottom: 3px solid #B71C1C !important;
    }
    QPushButton[style*="background-color: #d32f2f"]:hover {
        background-color: #EF5350 !important;
    }
    QPushButton[style*="background-color: #d32f2f"]:pressed {
        background-color: #C62828 !important;
        border-bottom: none !important;
        padding-top: 13px;
    }

    /* --- PESTAÑAS (TABS) --- */
    QTabWidget::pane {
        border: 1px solid #444444;
        border-radius: 4px;
        background-color: #333333;
        top: -1px; /* Fusión con la barra */
    }
    QTabBar::tab {
        background: #2b2b2b;
        color: #AAAAAA;
        padding: 8px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
        outline: 0px; /* Sin linea de foco */
    }
    QTabBar::tab:hover {
        background: #3a3a3a;
        color: #FFFFFF;
    }
    QTabBar::tab:selected {
        background: #4CAF50;
        color: white;
        font-weight: bold;
        /* Pequeño efecto de elevación en la pestaña activa */
        border-bottom: 2px solid #4CAF50;
    }

    /* --- CONTROLES DE FORMULARIO --- */
    QLineEdit, QComboBox {
        background-color: #1e1e1e;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 5px;
        color: #F0F0F0;
        selection-background-color: #4CAF50;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #4CAF50; /* Borde verde al escribir */
    }

    /* --- TABLAS --- */
    QTableWidget {
        background-color: #1e1e1e;
        gridline-color: #333333;
        border: 1px solid #444444;
        border-radius: 4px;
    }
    QHeaderView::section {
        background-color: #333333;
        padding: 5px;
        border: none;
        border-right: 1px solid #444444;
        font-weight: bold;
    }
    QTableWidget::item:selected {
        background-color: #4CAF50;
        color: white;
    }

    /* --- RADIO BUTTONS --- */
    QRadioButton {
        spacing: 8px;
    }
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
        border-radius: 9px;
        background-color: #1e1e1e;
        border: 2px solid #666666;
    }
    QRadioButton::indicator:checked {
        background-color: #1e1e1e;
        border: 2px solid #4CAF50;
    }
    /* El punto central del radio */
    QRadioButton::indicator:checked::image {
        background-color: #4CAF50;
        margin: 3px; /* Crea el efecto de anillo */
        border-radius: 5px;
    }
    QRadioButton::indicator:hover {
        border-color: #4CAF50;
    }
    #OnAccessFrame {
        background-color: #253529; /* Verde muy oscuro y elegante */
        border: 1px solid #2E7D32;
        border-radius: 8px;
    }
    QTextBrowser {
        border: none;
        /* El color de fondo lo dejamos transparente en el código Python,
           pero el color del texto lo heredará de QWidget */
    }
"""

# -----------------------------------------------------
# ESTILO CLARO (GRIS PROFESIONAL - MÁS OSCURO)
# -----------------------------------------------------
LIGHT_STYLE_SHEET = """
    QMainWindow, QWidget, QDialog {
        background-color: #C0C0C0; /* Gris Plata sólido (Mucho menos brillo) */
        color: #2C3E50;
        font-family: "Segoe UI", "Helvetica Neue", "Arial", sans-serif;
        font-size: 14px;
        selection-background-color: #4CAF50;
    }

    /* Los paneles ahora destacan claramente sobre el fondo gris */
    QFrame {
        background-color: #E0E0E0;
        border-radius: 8px;
    }

    /* --- BOTONES --- */
    QPushButton {
        background-color: #3498DB;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 10px 20px;
        border-bottom: 3px solid #2980B9;
    }
    QPushButton:hover {
        background-color: #5DADE2;
        border-bottom: 3px solid #3498DB;
    }
    QPushButton:pressed {
        background-color: #2980B9;
        border-bottom: none;
        padding-top: 13px;
        padding-bottom: 7px;
    }

    /* Botones Rojos */
    QPushButton[style*="background-color: #d32f2f"] {
        background-color: #E74C3C !important;
        border-bottom: 3px solid #C0392B !important;
    }
    QPushButton[style*="background-color: #d32f2f"]:pressed {
        background-color: #C0392B !important;
        border-bottom: none !important;
        padding-top: 13px;
    }

    /* --- PESTAÑAS --- */
    QTabWidget::pane {
        border: 1px solid #999999;
        border-radius: 4px;
        background-color: #E0E0E0; /* Coincide con los frames */
    }
    QTabBar::tab {
        background: #B0B0B0; /* Pestañas inactivas más oscuras para contraste */
        color: #444444;
        padding: 8px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
        outline: 0px;
    }
    QTabBar::tab:hover {
        background: #D0D0D0;
        color: #222222;
    }
    QTabBar::tab:selected {
        background: #3498DB; /* Azul para la activa */
        color: white;
        font-weight: bold;
        border-bottom: 2px solid #2980B9;
    }

    /* --- INPUTS Y TABLAS (BLANCOS PARA LEER MEJOR) --- */
    QLineEdit, QComboBox {
        background-color: #FFFFFF; /* Blanco puro para el texto */
        border: 1px solid #888888;
        border-radius: 4px;
        padding: 5px;
        color: #2C3E50;
        selection-background-color: #3498DB;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #3498DB;
    }

    QTableWidget {
        background-color: #FFFFFF; /* Tabla blanca sobre fondo gris */
        gridline-color: #DDDDDD;
        border: 1px solid #888888;
        border-radius: 4px;
    }
    QHeaderView::section {
        background-color: #D0D0D0;
        padding: 5px;
        border: none;
        border-right: 1px solid #AAAAAA;
        font-weight: bold;
        color: #2C3E50;
    }
    QTableWidget::item:selected {
        background-color: #3498DB;
        color: white;
    }

    /* --- RADIO BUTTONS --- */
    QRadioButton {
        spacing: 8px;
        color: #222222; /* Texto casi negro */
    }
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
        border-radius: 9px;
        background-color: #FFFFFF;
        border: 2px solid #666666;
    }
    QRadioButton::indicator:checked {
        background-color: #E0E0E0;
        border: 2px solid #3498DB;
    }
    QRadioButton::indicator:checked::image {
        background-color: #3498DB;
        margin: 3px;
        border-radius: 5px;
    }
    #OnAccessFrame {
        background-color: #E8F5E9; /* Verde claro suave */
        border: 1px solid #C8E6C9;
        border-radius: 8px;
    }
    QTextBrowser {
        border: none;
        /* El color de fondo lo dejamos transparente en el código Python,
           pero el color del texto lo heredará de QWidget */
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
        self.tabs.addTab(QuarantineTab(), locales.get_text("quarantine_title"))
        self.tabs.addTab(ConfigTab(), locales.get_text("tab_config"))
        self.tabs.addTab(HelpTab(), locales.get_text("tab_help"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- 1. SPLASH SCREEN (Pantalla de Carga) ---
    # Calculamos ruta base (compatible con PyInstaller y Script)
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    splash_img_path = os.path.join(base_dir, "AnabasaSoft.png")
    splash = None

    if os.path.exists(splash_img_path):
        # Crear y mostrar el Splash
        pixmap = QPixmap(splash_img_path)

        # Opcional: Si la imagen es gigante, la escalamos a algo razonable (ej: 600px ancho)
        # pixmap = pixmap.scaledToWidth(600, Qt.SmoothTransformation)

        splash = QSplashScreen(pixmap)
        splash.setWindowFlag(Qt.WindowStaysOnTopHint) # Que se quede encima
        splash.show()

        # Forzamos a Qt a dibujar la imagen inmediatamente
        app.processEvents()

        # Esperamos 2 segundos (2000 ms) sin congelar el sistema
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec()

    # --- 2. CARGA DE CONFIGURACIÓN ---
    cfg = ConfigManager()
    current_theme = cfg.get_theme()
    selected_lang = cfg.get_language() # Cargar idioma guardado

    # Cargar textos
    locales.load_language(selected_lang)

    # Cargar tema
    if current_theme in THEMES:
        app.setStyleSheet(THEMES[current_theme])
    else:
        app.setStyleSheet(THEMES["dark"])

    # --- 3. VERIFICACIÓN POLKIT ---
    from polkit_manager import PolkitManager
    polkit_mgr = PolkitManager()

    installed_ver = cfg.get_polkit_version()
    required_ver = polkit_mgr.get_current_version()

    if installed_ver < required_ver:
        # Si hay splash, lo ocultamos temporalmente para mostrar el diálogo
        # o dejamos que el diálogo salga encima (Qt lo gestiona bien).

        msg_box = QMessageBox()
        msg_box.setWindowTitle(locales.get_text("polkit_title"))
        msg_text = locales.get_text("polkit_msg").format(required_ver)
        msg_box.setText(msg_text)
        msg_box.setIcon(QMessageBox.Information)

        btn_yes = msg_box.addButton(locales.get_text("polkit_btn_yes"), QMessageBox.YesRole)
        btn_no = msg_box.addButton(locales.get_text("polkit_btn_no"), QMessageBox.NoRole)
        msg_box.setDefaultButton(btn_yes)

        # Hacemos que el mensaje salga encima del splash si este existe
        if splash:
            msg_box.setWindowModality(Qt.ApplicationModal)

        msg_box.exec()

        if msg_box.clickedButton() == btn_yes:
            if polkit_mgr.install_rule():
                cfg.set_polkit_version(required_ver)
                QMessageBox.information(None, "SentinelX", locales.get_text("polkit_success"))
            else:
                QMessageBox.warning(None, "SentinelX", locales.get_text("polkit_error"))

    # --- 4. INICIO VENTANA PRINCIPAL ---
    icon_path = os.path.join(base_dir, "SentinelX-Icon-512.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    window = MainWindow()
    window.showMaximized()

    # Cerrar el Splash cuando la ventana principal ya está lista
    if splash:
        splash.finish(window)

    sys.exit(app.exec())
