from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTextEdit, QProgressBar, QMessageBox, QFrame)
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QColor

import locales
# Importamos el nuevo InstallWorker
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

        # --- CABECERA ---
        header_layout = QHBoxLayout()
        lbl_title = QLabel(locales.get_text("av_title"))
        lbl_title.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(lbl_title)

        self.lbl_status = QLabel("...")
        self.lbl_status.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self.lbl_status)
        layout.addLayout(header_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(line)

        # --- BOTONES ---
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

        self.btn_stop = QPushButton("🛑 " + locales.get_text("av_btn_stop"))
        self.btn_stop.setMinimumHeight(40)
        self.btn_stop.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold;")
        self.btn_stop.clicked.connect(self.stop_scan)
        self.btn_stop.hide() # Oculto al inicio

        btn_layout.addWidget(self.btn_scan_home)
        btn_layout.addWidget(self.btn_scan_sys)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)

        # --- CONSOLA LOGS ---
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

        # --- PROGRESO ---
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.hide()
        layout.addWidget(self.progress)

        # --- BOTÓN INSTALAR ---
        self.btn_install = QPushButton("📥 " + locales.get_text("av_btn_install"))
        self.btn_install.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 10px;")
        self.btn_install.clicked.connect(self.install_clamav)
        self.btn_install.hide()
        layout.addWidget(self.btn_install)

        self.setLayout(layout)
        self.check_status()

    def check_status(self):
        if self.manager.is_installed():
            version = self.manager.get_db_version()
            self.lbl_status.setText(f"✅ {locales.get_text('av_status_installed')} | {version}")
            self.lbl_status.setStyleSheet("color: #4CAF50; font-weight: bold;")

            self.btn_scan_home.setEnabled(True)
            self.btn_scan_sys.setEnabled(True)
            self.btn_update.setEnabled(True)
            self.btn_install.hide()
        else:
            self.lbl_status.setText(f"❌ {locales.get_text('av_status_missing')}")
            self.lbl_status.setStyleSheet("color: #d32f2f; font-weight: bold;")

            self.btn_scan_home.setEnabled(False)
            self.btn_scan_sys.setEnabled(False)
            self.btn_update.setEnabled(False)
            self.btn_install.show()

    def log(self, text):
        self.log_output.append(text)
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    # --- HELPER PARA GESTIONAR VISIBILIDAD ---
    def set_buttons_visible(self, scanning):
        """
        scanning = True -> Muestra STOP, Oculta Escanear
        scanning = False -> Oculta STOP, Muestra Escanear
        """
        if scanning:
            self.btn_scan_home.hide()
            self.btn_scan_sys.hide()
            self.btn_update.hide()
            self.btn_stop.show()
        else:
            self.btn_scan_home.show()
            self.btn_scan_sys.show()
            self.btn_update.show()
            self.btn_stop.hide()

    # --- ACCIONES DE WORKERS ---

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

        # CAMBIO: Ocultamos botones normales, mostramos STOP
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

    # --- CALLBACKS ---

    def on_scan_finished(self, success, infected_count):
        self.progress.hide()
        # CAMBIO: Ocultamos STOP, mostramos botones normales
        self.set_buttons_visible(scanning=False)

        # Restaurar texto del botón stop por si acaso
        self.btn_stop.setEnabled(True)
        self.btn_stop.setText("🛑 " + locales.get_text("av_btn_stop"))

        self.log("-" * 30)

        # Si infected_count es -1, es que fue cancelado por usuario
        if infected_count == -1:
            # Ya el worker mandó el mensaje de "Detenido por usuario" al log
            return

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

    def stop_scan(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            # Deshabilitamos el botón para que no le den 2 veces
            self.btn_stop.setEnabled(False)
            self.btn_stop.setText("Stopping...")
            # Llamamos al backend
            self.worker.stop()
