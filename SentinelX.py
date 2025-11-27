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
:version:      1.4.2

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
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QMessageBox, QSplashScreen, QSystemTrayIcon, QMenu)
from PySide6.QtGui import QIcon, QPixmap, QAction
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
# ESTILO OSCURO (HACKER / PREMIUM)
# -----------------------------------------------------
DARK_STYLE_SHEET = """
    QMainWindow, QWidget, QDialog {
        background-color: #2b2b2b;
        color: #F0F0F0;
        font-family: "Segoe UI", "Helvetica Neue", "Arial", sans-serif;
        font-size: 14px;
        selection-background-color: #4CAF50;
    }

    QFrame {
        background-color: #333333;
        border-radius: 8px;
        border: none;
    }

    #OnAccessFrame {
        background-color: #253529;
        border: 1px solid #2E7D32;
    }

    QPushButton {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 10px 20px;
        border-bottom: 3px solid #2E7D32;
    }
    QPushButton:hover {
        background-color: #57B85B;
        border-bottom: 3px solid #36893B;
    }
    QPushButton:pressed {
        background-color: #2E7D32;
        border-bottom: none;
        padding-top: 13px;
        padding-bottom: 7px;
    }

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

    QTabWidget::pane {
        border: 1px solid #444444;
        border-radius: 4px;
        background-color: #333333;
        top: -1px;
    }
    QTabBar::tab {
        background: #2b2b2b;
        color: #AAAAAA;
        padding: 8px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
        outline: 0px;
    }
    QTabBar::tab:hover {
        background: #3a3a3a;
        color: #FFFFFF;
    }
    QTabBar::tab:selected {
        background: #4CAF50;
        color: white;
        font-weight: bold;
        border-bottom: 2px solid #4CAF50;
    }

    QLineEdit, QComboBox {
        background-color: #1e1e1e;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 5px;
        color: #F0F0F0;
        selection-background-color: #4CAF50;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #4CAF50;
    }

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

    QTextBrowser {
        border: none;
        background-color: transparent;
    }

    /* --- RADIO BUTTONS (FIXED) --- */
    QRadioButton {
        spacing: 10px;
        color: #F0F0F0;
        font-weight: bold;
    }

    /* APAGADO: Aro Gris Vacío */
    QRadioButton::indicator {
        width: 20px;
        height: 20px;
        border-radius: 11px; /* Totalmente redondo */
        background-color: transparent;
        border: 2px solid #888888;
    }
    QRadioButton::indicator:hover {
        border-color: #4CAF50;
    }

    /* ENCENDIDO: BOLA VERDE MACIZA */
    QRadioButton::indicator:checked {
        background-color: #4CAF50;
        border: 2px solid #4CAF50;
    }
"""

# -----------------------------------------------------
# ESTILO CLARO (PROFESIONAL)
# -----------------------------------------------------
LIGHT_STYLE_SHEET = """
    QMainWindow, QWidget, QDialog {
        background-color: #C0C0C0;
        color: #2C3E50;
        font-family: "Segoe UI", "Helvetica Neue", "Arial", sans-serif;
        font-size: 14px;
        selection-background-color: #3498DB;
    }

    QFrame {
        background-color: #E0E0E0;
        border-radius: 8px;
        border: none;
    }

    #OnAccessFrame {
        background-color: #E8F5E9;
        border: 1px solid #C8E6C9;
    }

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

    QPushButton[style*="background-color: #d32f2f"] {
        background-color: #E74C3C !important;
        border-bottom: 3px solid #C0392B !important;
    }
    QPushButton[style*="background-color: #d32f2f"]:pressed {
        background-color: #C0392B !important;
        border-bottom: none !important;
        padding-top: 13px;
    }

    QTabWidget::pane {
        border: 1px solid #999999;
        border-radius: 4px;
        background-color: #E0E0E0;
        top: -1px;
    }
    QTabBar::tab {
        background: #B0B0B0;
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
        background: #3498DB;
        color: white;
        font-weight: bold;
        border-bottom: 2px solid #2980B9;
    }

    QLineEdit, QComboBox {
        background-color: #FFFFFF;
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
        background-color: #FFFFFF;
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

    QTextBrowser {
        border: none;
        background-color: transparent;
    }

    /* --- RADIO BUTTONS (FIXED) --- */
    QRadioButton {
        spacing: 10px;
        color: #222222;
        font-weight: bold;
    }

    /* APAGADO: Aro Gris Vacío sobre fondo Blanco/Transparente */
    QRadioButton::indicator {
        width: 20px;
        height: 20px;
        border-radius: 11px;
        background-color: #FFFFFF;
        border: 2px solid #888888;
    }
    QRadioButton::indicator:hover {
        border-color: #3498DB;
    }

    /* ENCENDIDO: BOLA AZUL MACIZA */
    QRadioButton::indicator:checked {
        background-color: #3498DB;
        border: 2px solid #3498DB;
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

        self.force_quit = False

        # Icono
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(base_dir, "SentinelX-Icon-512.png")
        if os.path.exists(icon_path):
            self.app_icon = QIcon(icon_path)
            self.setWindowIcon(self.app_icon)
        else:
            self.app_icon = QIcon()

        # --- SETUP TRAY ICON ---
        self.init_tray_icon()

        self.tabs = QTabWidget()
        self.tabs.setFocusPolicy(Qt.NoFocus)
        self.setCentralWidget(self.tabs)

        # Usamos las claves de traducción para los títulos de pestañas
        self.tabs.addTab(FirewallTab(), locales.get_text("tab_firewall"))
        self.tabs.addTab(AntivirusTab(), locales.get_text("tab_antivirus"))
        self.tabs.addTab(QuarantineTab(), locales.get_text("quarantine_title"))
        self.tabs.addTab(ConfigTab(), locales.get_text("tab_config"))
        self.tabs.addTab(HelpTab(), locales.get_text("tab_help"))

    def init_tray_icon(self):
        """Configura el icono de la bandeja del sistema"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.app_icon)

        # Crear menú contextual (Click derecho)
        tray_menu = QMenu()

        action_restore = QAction(locales.get_text("tray_restore"), self)
        action_restore.triggered.connect(self.show_window)
        tray_menu.addAction(action_restore)

        tray_menu.addSeparator()

        action_quit = QAction(locales.get_text("tray_quit"), self)
        action_quit.triggered.connect(self.quit_application)
        tray_menu.addAction(action_quit)

        self.tray_icon.setContextMenu(tray_menu)

        # Manejar click izquierdo (activar)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        """Si hacen click izquierdo, restauramos"""
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                if self.isMinimized():
                    self.showNormal()
                    self.activateWindow()
                else:
                    self.hide() # Click para ocultar también es útil
            else:
                self.show_window()

    def show_window(self):
        self.showNormal()
        self.activateWindow()

    def quit_application(self):
        """Esta función cierra la app de verdad"""
        self.force_quit = True
        QApplication.quit()

    # --- SOBREESCRIBIR EL EVENTO DE CIERRE (La X de la ventana) ---
    def closeEvent(self, event):
        if self.force_quit:
            # Si le dimos a "Salir" en el tray, cerramos de verdad
            event.accept()
        else:
            # Si le dimos a la X, solo ocultamos
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                locales.get_text("tray_minimize_title"),
                locales.get_text("tray_minimize_msg"),
                QSystemTrayIcon.Information,
                2000
            )

if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QApplication(sys.argv)

    # Evitar que la app se cierre si cerramos la última ventana (porque queda el Tray)
    app.setQuitOnLastWindowClosed(False)

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

    # LÓGICA DE INICIO MINIMIZADO
    if cfg.get_start_minimized():
        # No mostramos la ventana (window.show...), solo el icono tray
        # Mostramos una notificación para que el usuario sepa que está ahí
        if window.tray_icon:
            window.tray_icon.show()
            window.tray_icon.showMessage(
                "SentinelX",
                locales.get_text("tray_minimize_msg"),
                QSystemTrayIcon.Information,
                2000
            )
    else:
        # Inicio normal
        window.showMaximized()

    if splash:
        splash.finish(window)

    sys.exit(app.exec())
