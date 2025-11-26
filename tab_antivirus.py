from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTextEdit, QProgressBar, QMessageBox, QFrame,
                               QApplication, QFileDialog)
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont

import locales
from ui_components import ToggleSwitch
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

        # Interruptor (Toggle) del Demonio Principal
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

        # --- 2. BOTONES DE ACCIÓN (ESCANEO / UPDATE) ---
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

        # Botón STOP (Oculto por defecto)
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

        # --- 3. SECCIÓN ON-ACCESS (TIEMPO REAL) ---
        # Línea separadora 2
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(line2)

        # >>> AQUÍ ESTABA EL ERROR <<<
        oa_layout = QVBoxLayout()

        # Título y Estado OA
        oa_header = QHBoxLayout()
        lbl_oa_title = QLabel("🛡️ " + locales.get_text("oa_title"))
        lbl_oa_title.setFont(QFont("Arial", 14, QFont.Bold))
        oa_header.addWidget(lbl_oa_title)

        oa_header.addStretch()

        self.lbl_oa_status = QLabel("...")
        self.lbl_oa_status.setFont(QFont("Arial", 10, QFont.Bold))
        oa_header.addWidget(self.lbl_oa_status)

        oa_layout.addLayout(oa_header)

        # Descripción OA
        lbl_oa_desc = QLabel(locales.get_text("oa_desc"))
        lbl_oa_desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        oa_layout.addWidget(lbl_oa_desc)

        # --- ZONA DE CONFIGURACIÓN (Botón + Ruta) ---
        config_layout = QHBoxLayout()

        # Botón Activar/Desactivar (Tamaño controlado)
        self.btn_oa_toggle = QPushButton(locales.get_text("oa_btn_enable"))
        self.btn_oa_toggle.setFixedSize(200, 45)
        self.btn_oa_toggle.clicked.connect(self.toggle_on_access)
        config_layout.addWidget(self.btn_oa_toggle)

        config_layout.addStretch()

        # Etiqueta "Carpeta vigilada:"
        lbl_watch = QLabel(locales.get_text("oa_watched_dirs"))
        lbl_watch.setStyleSheet("font-weight: bold;")
        config_layout.addWidget(lbl_watch)

        # La ruta actual
        self.current_watch_path = "/home" # Valor por defecto
        self.lbl_oa_path = QLabel(self.current_watch_path)
        self.lbl_oa_path.setStyleSheet("font-style: italic; color: #555; background: #fff; padding: 5px; border-radius: 4px;")
        config_layout.addWidget(self.lbl_oa_path)

        # Botón para cambiar carpeta
        self.btn_change_path = QPushButton("📁")
        self.btn_change_path.setFixedSize(40, 30)
        self.btn_change_path.setToolTip(locales.get_text("av_path_dialog"))
        self.btn_change_path.clicked.connect(self.change_watch_path)
        config_layout.addWidget(self.btn_change_path)

        oa_layout.addLayout(config_layout)

        # Enmarcar todo en un Frame bonito
        oa_frame = QFrame()
        oa_frame.setLayout(oa_layout)
        # Usamos un ID para que el estilo cambie según el tema (Oscuro/Claro) en SentinelX.py
        oa_frame.setObjectName("OnAccessFrame")

        layout.addWidget(oa_frame)

        # --- 4. CONSOLA DE LOGS ---
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

        # --- 5. BARRA DE PROGRESO ---
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.hide()
        layout.addWidget(self.progress)

        # --- 6. BOTÓN DE INSTALACIÓN (Si falta) ---
        self.btn_install = QPushButton("📥 " + locales.get_text("av_btn_install"))
        self.btn_install.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 10px;")
        self.btn_install.clicked.connect(self.install_clamav)
        self.btn_install.hide()
        layout.addWidget(self.btn_install)

        self.setLayout(layout)

        # Chequeo inicial
        self.check_status()

    def check_status(self):
        # 1. Verificar si está instalado el paquete base
        if self.manager.is_installed():
            self.btn_install.hide()
            self.set_buttons_enabled(True)
            self.toggle.setEnabled(True)

            # 2. Verificar estado del Demonio (Toggle superior)
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

        # 3. Verificar estado On-Access
        is_oa_active = self.manager.is_on_access_active()
        if is_oa_active:
            self.lbl_oa_status.setText(locales.get_text("oa_status_active"))
            self.lbl_oa_status.setStyleSheet("color: #2ecc71;")
            self.btn_oa_toggle.setText(locales.get_text("oa_btn_disable"))
            # Estilo rojo para desactivar
            self.btn_oa_toggle.setStyleSheet("background-color: #d32f2f; color: white;")
        else:
            self.lbl_oa_status.setText(locales.get_text("oa_status_inactive"))
            self.lbl_oa_status.setStyleSheet("color: #7f8c8d;")
            self.btn_oa_toggle.setText(locales.get_text("oa_btn_enable"))
            # Resetear estilo (para que use el tema por defecto)
            self.btn_oa_toggle.setStyleSheet("")

    # --- CONTROL DEL DEMONIO (TOGGLE SUPERIOR) ---
    def on_toggle_click(self):
        """Maneja el click en el interruptor del Demonio Principal"""
        target_state = self.toggle.isChecked()

        # LÓGICA DE SEGURIDAD:
        # Si intentamos APAGAR el demonio pero el On-Access está ACTIVO,
        # tenemos que prohibir la acción.
        if not target_state and self.manager.is_on_access_active():
            QMessageBox.warning(self, locales.get_text("msg_warning"),
                "No puedes detener el servicio principal mientras la Protección en Tiempo Real está activa.\n\n"
                "Desactiva primero la Protección On-Access.")

            # Revertimos el botón visualmente
            self.toggle.blockSignals(True)
            self.toggle.setChecked(True)
            self.toggle.blockSignals(False)
            return

        # Si todo bien, procedemos
        QApplication.setOverrideCursor(Qt.WaitCursor)
        success = self.manager.set_daemon_state(target_state)
        QApplication.restoreOverrideCursor()

        if success:
            self.check_status()
        else:
            # Revertir si falló
            self.toggle.blockSignals(True)
            self.toggle.setChecked(not target_state)
            self.toggle.blockSignals(False)
            QMessageBox.warning(self, locales.get_text("av_update_error_title"), locales.get_text("av_daemon_error"))

    # --- CONTROL ON-ACCESS (BOTÓN INFERIOR) ---
    def toggle_on_access(self):
        """Maneja el botón de Protección en Tiempo Real"""
        currently_active = self.manager.is_on_access_active()
        target_state = not currently_active

        QApplication.setOverrideCursor(Qt.WaitCursor)

        # AUTO-CORRECCIÓN: Asegurar que el demonio esté activo
        if target_state:
            # 1. Visual
            self.toggle.blockSignals(True)
            self.toggle.setChecked(True)
            self.lbl_daemon_status.setText(locales.get_text("av_daemon_active"))
            self.lbl_daemon_status.setStyleSheet("color: #2ecc71;")
            self.toggle.blockSignals(False)

            # 2. Sistema
            if not self.manager.is_daemon_active():
                self.manager.set_daemon_state(True)

        # Configurar On-Access con la ruta elegida
        success = self.manager.configure_on_access(target_state, watch_path=self.current_watch_path)

        # Espera de seguridad para systemd
        import time
        time.sleep(2)

        QApplication.restoreOverrideCursor()

        if success:
            self.check_status()

            if target_state:
                # Verificar si arrancó
                if self.manager.is_on_access_active():
                    QMessageBox.information(self,
                                            locales.get_text("msg_info"),
                                            locales.get_text("av_path_active").format(self.current_watch_path))
                else:
                    # Fallo silencioso (logs)
                    QMessageBox.warning(self,
                                        locales.get_text("msg_warning"),
                                        "El servicio no arrancó. Revisa journalctl.")
        else:
            self.check_status()
            QMessageBox.critical(self,
                                 locales.get_text("av_install_error_title"),
                                 locales.get_text("oa_config_error"))

    def change_watch_path(self):
        # Si está activo, avisar que hay que desactivar primero
        if self.manager.is_on_access_active():
            QMessageBox.warning(self,
                                locales.get_text("msg_warning"),
                                locales.get_text("av_path_warn"))
            return

        # Abrir selector de carpetas
        folder = QFileDialog.getExistingDirectory(self,
                                                  locales.get_text("av_path_dialog"),
                                                  self.current_watch_path)

        if folder:
            self.current_watch_path = folder
            self.lbl_oa_path.setText(folder)

    # --- HELPERS DE UI ---
    def log(self, text):
        self.log_output.append(text)
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def set_buttons_enabled(self, enabled):
        self.btn_scan_home.setEnabled(enabled)
        self.btn_scan_sys.setEnabled(enabled)
        self.btn_update.setEnabled(enabled)
        self.btn_oa_toggle.setEnabled(enabled)
        self.btn_change_path.setEnabled(enabled) # También bloqueamos el cambio de ruta

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
