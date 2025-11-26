from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTextEdit, QProgressBar, QMessageBox, QFrame,
                               QApplication)
from PySide6.QtCore import Qt, QDir, QTimer
from PySide6.QtGui import QFont, QColor

import locales
from ui_components import ToggleSwitch # <--- IMPORTANTE: Reutilizamos tu botón
from antivirus_manager import AntivirusManager, ScanWorker, UpdateWorker, InstallWorker

class AntivirusTab(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = AntivirusManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # --- 1. CABECERA (Estilo Firewall) ---
        header_layout = QHBoxLayout()

        # Título
        lbl_title = QLabel(locales.get_text("av_title"))
        lbl_title.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(lbl_title)

        header_layout.addStretch()

        # Label Estado (Activo/Inactivo)
        self.lbl_daemon_status = QLabel("...")
        self.lbl_daemon_status.setFont(QFont("Arial", 10, QFont.Bold))
        self.lbl_daemon_status.setContentsMargins(0, 0, 10, 0)
        header_layout.addWidget(self.lbl_daemon_status)

        # Interruptor (Toggle)
        self.toggle = ToggleSwitch()
        self.toggle.clicked.connect(self.on_toggle_click)
        header_layout.addWidget(self.toggle)

        layout.addLayout(header_layout)

        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(line)

        # Subtítulo Info
        self.lbl_info = QLabel(locales.get_text("av_realtime_title"))
        self.lbl_info.setStyleSheet("color: gray; font-size: 11px;")
        self.lbl_info.setAlignment(Qt.AlignRight)
        layout.addWidget(self.lbl_info)

        # --- 2. BOTONES DE ESCANEO ---
        btn_layout = QHBoxLayout()

        self.btn_scan_home = QPushButton("🏠 " + locales.get_text("av_btn_scan_home"))
        self.btn_scan_home.setMinimumHeight(40)
        self.btn_scan_home.clicked.connect(self.scan_home)

        self.btn_scan_sys = QPushButton("🖥️ " + locales.get_text("av_btn_scan_system"))
        self.btn_scan_sys.setMinimumHeight(40)
        self.btn_scan_sys.clicked.connect(self.scan_system)

        self.btn_update = QPushButton("🔄 " + locales.get_text("av_btn_update_db"))
        self.btn_update.setMinimumHeight(40)
        self.btn_update.clicked.connect(self.update_db)

        # Botón STOP (Oculto)
        self.btn_stop = QPushButton("🛑 " + locales.get_text("av_btn_stop"))
        self.btn_stop.setMinimumHeight(40)
        self.btn_stop.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold;")
        self.btn_stop.clicked.connect(self.stop_scan)
        self.btn_stop.hide()

        btn_layout.addWidget(self.btn_scan_home)
        btn_layout.addWidget(self.btn_scan_sys)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)

        # --- 3. CONSOLA ---
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: Monospace;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.log_output)

        # --- 4. PROGRESO ---
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.hide()
        layout.addWidget(self.progress)

        # --- 5. BOTÓN INSTALAR (Si falta) ---
        self.btn_install = QPushButton("📥 " + locales.get_text("av_btn_install"))
        self.btn_install.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 10px;")
        self.btn_install.clicked.connect(self.install_clamav)
        self.btn_install.hide()
        layout.addWidget(self.btn_install)

        self.setLayout(layout)

        # Chequeo inicial
        self.check_status()

    def check_status(self):
        # 1. Verificar si está instalado
        if self.manager.is_installed():
            self.btn_install.hide()
            self.set_buttons_enabled(True)
            self.toggle.setEnabled(True)

            # 2. Verificar estado del Demonio (Toggle)
            self.toggle.blockSignals(True)
            is_active = self.manager.is_daemon_active()
            self.toggle.setChecked(is_active)

            if is_active:
                self.lbl_daemon_status.setText(locales.get_text("av_daemon_active"))
                self.lbl_daemon_status.setStyleSheet("color: #2ecc71;") # Verde
            else:
                self.lbl_daemon_status.setText(locales.get_text("av_daemon_inactive"))
                self.lbl_daemon_status.setStyleSheet("color: gray;")

            self.toggle.blockSignals(False)

            # Mostrar versión en log si está limpio
            if self.log_output.toPlainText() == "":
                ver = self.manager.get_db_version()
                self.log(f"ℹ️ {locales.get_text('av_status_installed')} | {ver}")

        else:
            # No instalado
            self.lbl_daemon_status.setText(locales.get_text("av_status_missing"))
            self.lbl_daemon_status.setStyleSheet("color: #d32f2f;")

            self.toggle.setChecked(False)
            self.toggle.setEnabled(False)
            self.set_buttons_enabled(False)
            self.btn_install.show()

    def on_toggle_click(self):
        """Maneja el click en el interruptor"""
        target_state = self.toggle.isChecked()

        # Cursor de espera porque systemctl tarda un poco
        QApplication.setOverrideCursor(Qt.WaitCursor)
        success = self.manager.set_daemon_state(target_state)
        QApplication.restoreOverrideCursor()

        if success:
            self.check_status() # Refrescar UI
        else:
            # Revertir si falló (ej. canceló contraseña)
            self.toggle.blockSignals(True)
            self.toggle.setChecked(not target_state)
            self.toggle.blockSignals(False)
            QMessageBox.warning(self, "Error", locales.get_text("av_daemon_error"))

    # ... (El resto de métodos scan_home, install_clamav, logs, etc. SIGUEN IGUAL) ...
    # COPIA AQUÍ EL RESTO DE MÉTODOS DE TU ARCHIVO ANTERIOR
    # (log, set_buttons_enabled, scan_home, scan_system, start_scan, update_db,
    #  install_clamav, stop_scan, set_buttons_visible y los callbacks on_...)

    def log(self, text):
        self.log_output.append(text)
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def set_buttons_enabled(self, enabled):
        self.btn_scan_home.setEnabled(enabled)
        self.btn_scan_sys.setEnabled(enabled)
        self.btn_update.setEnabled(enabled)
        # No tocamos btn_install aquí porque se gestiona en check_status

    def scan_home(self):
        self.start_scan(QDir.homePath())

    def scan_system(self):
        QMessageBox.information(self,
                                locales.get_text("av_scan_info_title"),
                                locales.get_text("av_scan_info_msg"))
        self.start_scan("/")

    def start_scan(self, path):
        self.log_output.clear()
        self.progress.setRange(0, 0)
        self.progress.show()
        self.set_buttons_visible(scanning=True)

        self.worker = ScanWorker(path)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_scan_finished)
        self.worker.start()

    def update_db(self):
        self.log_output.clear()
        self.progress.setRange(0, 0)
        self.progress.show()
        self.set_buttons_enabled(False)

        self.updater = UpdateWorker()
        self.updater.log_signal.connect(self.log)
        self.updater.finished_signal.connect(self.on_update_finished)
        self.updater.start()

    def stop_scan(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.btn_stop.setEnabled(False)
            self.worker.stop()

    def install_clamav(self):
        reply = QMessageBox.question(self,
                                     locales.get_text("av_install_confirm_title"),
                                     locales.get_text("av_install_msg"),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.log_output.clear()
            self.log(locales.get_text("av_install_log_start"))
            self.progress.setRange(0, 0)
            self.progress.show()
            self.set_buttons_enabled(False)

            self.installer_worker = InstallWorker()
            self.installer_worker.log_signal.connect(self.log)
            self.installer_worker.finished_signal.connect(self.on_install_finished)
            self.installer_worker.start()

    def set_buttons_visible(self, scanning):
        if scanning:
            self.btn_scan_home.hide()
            self.btn_scan_sys.hide()
            self.btn_update.hide()
            self.btn_stop.show()
            self.btn_stop.setEnabled(True)
            self.btn_stop.setText("🛑 " + locales.get_text("av_btn_stop"))
        else:
            self.btn_scan_home.show()
            self.btn_scan_sys.show()
            self.btn_update.show()
            self.btn_stop.hide()

    # --- CALLBACKS ---
    def on_scan_finished(self, success, infected_count):
        self.progress.hide()
        self.set_buttons_visible(scanning=False)
        self.log("-" * 30)

        if infected_count == -1: return

        if not success:
            self.log(locales.get_text("av_scan_cancel_log"))
        elif infected_count == 0:
            msg = locales.get_text("av_scan_clean")
            self.log(msg)
            QMessageBox.information(self, locales.get_text("av_scan_clean_title"), msg)
        else:
            msg = locales.get_text("av_scan_infected").format(infected_count)
            self.log(msg)
            QMessageBox.warning(self, locales.get_text("av_scan_threat_title"), msg)

    def on_update_finished(self, success):
        self.progress.hide()
        self.set_buttons_enabled(True)
        if success:
            self.log(locales.get_text("av_update_success_log"))
            self.check_status()
        else:
            self.log(locales.get_text("av_update_fail_log"))
            QMessageBox.warning(self,
                                locales.get_text("av_update_error_title"),
                                locales.get_text("av_error_update"))

    def on_install_finished(self, success):
        self.progress.hide()
        self.set_buttons_enabled(True)

        if success:
            QMessageBox.information(self,
                                    locales.get_text("av_install_success_title"),
                                    locales.get_text("av_install_success_msg"))
            self.check_status()
        else:
            self.log(locales.get_text("av_install_fail_log"))
            QMessageBox.critical(self,
                                 locales.get_text("av_install_error_title"),
                                 locales.get_text("av_install_error_msg"))
