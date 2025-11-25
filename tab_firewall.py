from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QMessageBox, QFrame, QDialog, QDialogButtonBox,
                               QComboBox, QApplication, QProgressDialog,
                               QTabWidget, QRadioButton, QButtonGroup, QPushButton,
                               QTableWidget, QHeaderView, QAbstractItemView,
                               QTableWidgetItem, QLineEdit, QCompleter)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor, QIntValidator

# Importaciones locales
import locales
from firewall_detector import FirewallDetector, FirewallType, FirewallInstaller
from ui_components import ToggleSwitch
from config_manager import ConfigManager
from network_utils import NetworkUtils

# --- DIÁLOGO PARA RED NUEVA ---
class NewNetworkDialog(QDialog):
    def __init__(self, net_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(locales.get_text("net_detect_title"))
        self.setFixedSize(400, 250)
        self.net_name = net_name
        self.selected_zone = "public" # Por defecto seguridad
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Icono o título
        lbl_info = QLabel(locales.get_text("net_detect_msg").format(self.net_name))
        lbl_info.setWordWrap(True)
        lbl_info.setTextFormat(Qt.RichText) # Para permitir negrita <b>
        lbl_info.setFont(QFont("Arial", 11))
        layout.addWidget(lbl_info)

        layout.addSpacing(10)

        # Botones grandes
        btn_public = QPushButton("☕ " + locales.get_text("net_btn_public"))
        btn_public.setMinimumHeight(40)
        btn_public.clicked.connect(lambda: self.finish("public"))
        layout.addWidget(btn_public)

        btn_home = QPushButton("🏠 " + locales.get_text("net_btn_home"))
        btn_home.setMinimumHeight(40)
        btn_home.clicked.connect(lambda: self.finish("home"))
        layout.addWidget(btn_home)

        layout.addStretch()
        self.setLayout(layout)

    def finish(self, zone):
        self.selected_zone = zone
        self.accept()

# --- CLASES DE UTILIDAD (WORKER y DIALOG) ---
# (Las mantenemos igual que antes, necesarias para la instalación)
class InstallWorker(QThread):
    finished_signal = Signal(bool)
    def __init__(self, installer, fw_name):
        super().__init__()
        self.installer = installer
        self.fw_name = fw_name
    def run(self):
        success = self.installer.install_firewall(self.fw_name)
        self.finished_signal.emit(success)

class InstallDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(locales.get_text("inst_title"))
        self.setFixedSize(400, 250)
        self.installer = FirewallInstaller()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        lbl_title = QLabel(locales.get_text("inst_header"))
        lbl_title.setFont(QFont("Arial", 14, QFont.Bold))
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)

        distro = self.installer.get_distro_type().capitalize()
        msg = locales.get_text("inst_desc").format(distro)
        lbl_msg = QLabel(msg)
        lbl_msg.setWordWrap(True)
        layout.addWidget(lbl_msg)

        layout.addWidget(QLabel(locales.get_text("inst_select_label")))
        self.combo = QComboBox()

        distro_key = self.installer.get_distro_type()
        tag_rec = locales.get_text("inst_rec_tag")
        tag_simple = locales.get_text("inst_simple_tag")
        tag_adv = locales.get_text("inst_adv_tag")

        if distro_key in ["arch", "redhat", "suse"]:
            self.combo.addItem(f"Firewalld{tag_rec}", "firewalld")
            self.combo.addItem(f"UFW{tag_simple}", "ufw")
        elif distro_key == "debian":
            self.combo.addItem(f"UFW{tag_rec}", "ufw")
            self.combo.addItem(f"Firewalld{tag_adv}", "firewalld")
        else:
            self.combo.addItem("Firewalld", "firewalld")
            self.combo.addItem("UFW", "ufw")
        layout.addWidget(self.combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(locales.get_text("inst_btn_install"))
        buttons.button(QDialogButtonBox.Cancel).setText(locales.get_text("inst_btn_cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_selected_firewall(self):
        return self.combo.currentData()

class AddRuleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(locales.get_text("add_rule_title"))
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Puerto
        layout.addWidget(QLabel(locales.get_text("add_rule_port_label")))
        self.inp_port = QLineEdit()
        self.inp_port.setPlaceholderText("8080")
        # Validar que solo sean números hasta 65535
        self.inp_port.setValidator(QIntValidator(1, 65535))
        layout.addWidget(self.inp_port)

        # Input Protocolo
        layout.addWidget(QLabel(locales.get_text("add_rule_proto_label")))
        self.combo_proto = QComboBox()
        self.combo_proto.addItems(["tcp", "udp"])
        layout.addWidget(self.combo_proto)

        # --- CAMPO: NOMBRE ---
        layout.addWidget(QLabel(locales.get_text("add_rule_desc_label")))
        self.inp_desc = QLineEdit()
        self.inp_desc.setPlaceholderText("Ej: Servidor Minecraft")
        layout.addWidget(self.inp_desc)

        layout.addStretch()

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(locales.get_text("add_rule_btn_save"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        return self.inp_port.text(), self.combo_proto.currentText(), self.inp_desc.text()

class InboundRulesPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.detector = FirewallDetector()
        self.cfg = ConfigManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # --- CABECERA ---
        lbl_title = QLabel(locales.get_text("inbound_table_title"))
        lbl_title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(lbl_title)

        # --- TABLA ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        headers = [
            locales.get_text("inbound_header_port"),
            locales.get_text("inbound_header_proto"),
            locales.get_text("inbound_header_action"),
            locales.get_text("inbound_header_source"),
        ]
        self.table.setHorizontalHeaderLabels(headers)

        # Configuración importante para selección
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows) # Seleccionar fila completa
        self.table.setSelectionMode(QAbstractItemView.SingleSelection) # Solo una a la vez

        layout.addWidget(self.table)

        # --- BARRA DE HERRAMIENTAS (BOTONES) ---
        toolbar_layout = QHBoxLayout()

        # Botón Añadir (+)
        self.btn_add = QPushButton("➕ " + locales.get_text("btn_add_rule"))
        self.btn_add.clicked.connect(self.action_add_rule)
        toolbar_layout.addWidget(self.btn_add)

        # Botón Eliminar (-)
        self.btn_del = QPushButton("🗑️ " + locales.get_text("btn_del_rule"))
        self.btn_del.setStyleSheet("background-color: #d32f2f; color: white;") # Rojo para peligro
        self.btn_del.clicked.connect(self.action_del_rule)
        toolbar_layout.addWidget(self.btn_del)

        toolbar_layout.addStretch() # Empujamos botones a la izquierda

        # Botón Refrescar (a la derecha)
        # 1. Añadimos el texto traducido junto al icono
        btn_text = locales.get_text("btn_refresh_rules")
        btn_refresh = QPushButton(f"🔄 {btn_text}")

        # 2. IMPORTANTE: Eliminamos o comentamos la línea de ancho fijo
        # Si dejas esto activado, el texto saldrá cortado.
        # btn_refresh.setFixedWidth(40) <--- BORRAR O COMENTAR ESTO

        # Opcional: Ajustar un poco el padding si lo ves necesario
        btn_refresh.setCursor(Qt.PointingHandCursor)

        # Tooltip (opcional, ya que el botón lo explica, pero no estorba)
        btn_refresh.setToolTip(locales.get_text("btn_refresh_tooltip"))

        btn_refresh.clicked.connect(self.load_rules)
        toolbar_layout.addWidget(btn_refresh)

        layout.addLayout(toolbar_layout)
        self.setLayout(layout)

        self.load_rules()

    def load_rules(self):
        self.table.setRowCount(0)
        rules = self.detector.get_active_rules()

        if not rules: return # (O manejo de vacío previo)

        self.table.setRowCount(len(rules))
        for row, rule in enumerate(rules):
            port = rule.get('port', '')
            proto = rule.get('protocol', '')

            # --- LÓGICA DE NOMBRE INTELIGENTE ---
            # 1. Miramos si tú le pusiste un nombre personalizado
            custom_name = self.cfg.get_rule_description(port, proto)

            # 2. Si no, miramos si el sistema tiene un nombre (ej: ssh)
            system_name = rule.get('service_name', '')

            # 3. Decidimos qué mostrar en la columna 4
            if custom_name:
                display_name = f"⭐ {custom_name}" # Estrellita para tus notas
            elif system_name:
                display_name = system_name
            else:
                display_name = "-"
            # ------------------------------------

            port_item = QTableWidgetItem(port)
            proto_item = QTableWidgetItem(proto)
            action_item = QTableWidgetItem(rule.get('action', 'ALLOW'))
            name_item = QTableWidgetItem(display_name) # Usamos el nombre calculado

            if rule.get('action') == 'ALLOW':
                action_item.setForeground(QColor("#4CAF50"))

            self.table.setItem(row, 0, port_item)
            self.table.setItem(row, 1, proto_item)
            self.table.setItem(row, 2, action_item)
            self.table.setItem(row, 3, name_item)

    def action_add_rule(self):
        dialog = AddRuleDialog(self)
        if dialog.exec():
            # Recuperamos los 3 datos
            port, proto, desc = dialog.get_data()
            if not port: return

            QApplication.setOverrideCursor(Qt.WaitCursor)
            success = self.detector.manage_port("add", port, proto)
            QApplication.restoreOverrideCursor()

            if success:
                # --- GUARDAR TU NOMBRE EN LA CONFIG ---
                self.cfg.save_rule_description(port, proto, desc)
                # --------------------------------------

                QMessageBox.information(self, "Éxito", locales.get_text("msg_success_add"))
                self.load_rules()
            else:
                QMessageBox.critical(self, "Error", locales.get_text("msg_error_cmd"))

    def action_del_rule(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", locales.get_text("msg_error_select"))
            return

        port = self.table.item(current_row, 0).text()
        proto = self.table.item(current_row, 1).text()

        confirm_text = locales.get_text("msg_confirm_del_text").format(port, proto)
        reply = QMessageBox.question(self, locales.get_text("msg_confirm_del_title"),
                                   confirm_text, QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            success = self.detector.manage_port("remove", port, proto)
            QApplication.restoreOverrideCursor()

            if success:
                # --- BORRAR TU NOMBRE DE LA CONFIG PARA LIMPIAR ---
                self.cfg.delete_rule_description(port, proto)
                # --------------------------------------------------

                QMessageBox.information(self, "Éxito", locales.get_text("msg_success_del"))
                self.load_rules()
            else:
                QMessageBox.critical(self, "Error", locales.get_text("msg_error_cmd"))

class OutboundRulesPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.detector = FirewallDetector()
        self.cfg = ConfigManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        lbl_title = QLabel(locales.get_text("outbound_table_title"))
        lbl_title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(lbl_title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        headers = [
            locales.get_text("outbound_header_port"),
            locales.get_text("outbound_header_proto"),
            locales.get_text("outbound_header_action"),
            locales.get_text("outbound_header_source"),
        ]
        self.table.setHorizontalHeaderLabels(headers)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        layout.addWidget(self.table)

        # Botones
        toolbar_layout = QHBoxLayout()

        # Botón Bloquear Salida (En salida solemos querer bloquear)
        # Reusamos el texto "Añadir Regla" o podríamos poner "Bloquear Puerto"
        self.btn_add = QPushButton("⛔ " + locales.get_text("btn_add_rule"))
        self.btn_add.clicked.connect(self.action_add_rule)
        toolbar_layout.addWidget(self.btn_add)

        self.btn_del = QPushButton("🗑️ " + locales.get_text("btn_del_rule"))
        self.btn_del.setStyleSheet("background-color: #d32f2f; color: white;")
        self.btn_del.clicked.connect(self.action_del_rule)
        toolbar_layout.addWidget(self.btn_del)

        toolbar_layout.addStretch()

        btn_text = locales.get_text("btn_refresh_rules")
        btn_refresh = QPushButton(f"🔄 {btn_text}")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.load_rules)
        toolbar_layout.addWidget(btn_refresh)

        layout.addLayout(toolbar_layout)
        self.setLayout(layout)

        self.load_rules()

    def load_rules(self):
        self.table.setRowCount(0)
        # Llamamos al método OUTBOUND del detector
        rules = self.detector.get_active_outbound_rules()

        if not rules:
            # Opcional: Mostrar mensaje de "No hay reglas"
            return

        self.table.setRowCount(len(rules))
        for row, rule in enumerate(rules):
            port = rule.get('port', '')
            proto = rule.get('protocol', '')
            action = rule.get('action', 'DROP')

            # Llamamos al config con "OUT"
            custom_name = self.cfg.get_rule_description(port, proto, "OUT")
            display_name = f"⭐ {custom_name}" if custom_name else "-"

            port_item = QTableWidgetItem(port)
            proto_item = QTableWidgetItem(proto)
            action_item = QTableWidgetItem(action)
            name_item = QTableWidgetItem(display_name)

            # Color Rojo para DROP (Bloqueo)
            if action == "DROP" or action == "REJECT":
                action_item.setForeground(QColor("#d32f2f"))
            else:
                action_item.setForeground(QColor("#4CAF50"))

            self.table.setItem(row, 0, port_item)
            self.table.setItem(row, 1, proto_item)
            self.table.setItem(row, 2, action_item)
            self.table.setItem(row, 3, name_item)

    def action_add_rule(self):
        # Reusamos el diálogo de añadir regla
        dialog = AddRuleDialog(self)
        dialog.setWindowTitle("Bloquear Salida (Egress)") # Personalización rápida

        if dialog.exec():
            port, proto, desc = dialog.get_data()
            if not port: return

            QApplication.setOverrideCursor(Qt.WaitCursor)
            # Acción OUTBOUND: Por defecto añadimos regla DROP (Bloquear)
            success = self.detector.manage_outbound_port("add", port, proto, target="DROP")
            QApplication.restoreOverrideCursor()

            if success:
                self.cfg.save_rule_description(port, proto, desc, "OUT") # Guardar como OUT
                QMessageBox.information(self, "Éxito", "Regla de bloqueo añadida.")
                self.load_rules()
            else:
                QMessageBox.critical(self, "Error", locales.get_text("msg_error_cmd"))

    def action_del_rule(self):
        current_row = self.table.currentRow()
        if current_row < 0: return

        port = self.table.item(current_row, 0).text()
        proto = self.table.item(current_row, 1).text()
        # Asumimos DROP porque es lo que crea nuestro botón de añadir
        # (Para hacerlo perfecto deberíamos leer la acción de la tabla)
        action_target = self.table.item(current_row, 2).text()

        reply = QMessageBox.question(self, "Confirmar", f"¿Eliminar regla {port}/{proto}?", QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            success = self.detector.manage_outbound_port("remove", port, proto, target=action_target)
            QApplication.restoreOverrideCursor()

            if success:
                self.cfg.delete_rule_description(port, proto, "OUT")
                self.load_rules()
            else:
                QMessageBox.critical(self, "Error", locales.get_text("msg_error_cmd"))

# ==========================================
# NUEVAS CLASES PARA LOS PANELES (SUB-TABS)
# ==========================================

class NetworkTypePanel(QWidget):
    zone_changed = Signal()

    def __init__(self):
        super().__init__()
        self.detector = FirewallDetector()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título de sección
        lbl_title = QLabel(locales.get_text("zone_section_title"))
        lbl_title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(lbl_title)

        # Grupo de botones
        self.bg_zones = QButtonGroup(self)

        # --- PREGUNTAMOS AL SISTEMA ---
        current_zone = self.detector.get_default_zone()
        print(f"DEBUG: Zona detectada al inicio: {current_zone}")

        # Opción 1: Pública
        self.rb_public = QRadioButton(locales.get_text("zone_public_title"))
        self.rb_public.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(self.rb_public)
        self.bg_zones.addButton(self.rb_public, 1)

        lbl_public_desc = QLabel(locales.get_text("zone_public_desc"))
        # (Recuerda poner el color gris claro si estás en tema oscuro, o déjalo dinámico)
        lbl_public_desc.setStyleSheet("color: #A0A0A0; margin-left: 25px;")
        layout.addWidget(lbl_public_desc)

        layout.addSpacing(10)

        # Opción 2: Casa
        self.rb_home = QRadioButton(locales.get_text("zone_home_title"))
        self.rb_home.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(self.rb_home)
        self.bg_zones.addButton(self.rb_home, 2)

        lbl_home_desc = QLabel(locales.get_text("zone_home_desc"))
        lbl_home_desc.setStyleSheet("color: #A0A0A0; margin-left: 25px;")
        layout.addWidget(lbl_home_desc)

        # --- LÓGICA DE SELECCIÓN AUTOMÁTICA ---
        # Si la zona es 'home', 'work' o 'trusted', marcamos Casa.
        if current_zone in ["home", "work", "trusted", "internal"]:
            self.rb_home.setChecked(True)
        else:
            # Para 'public', 'block', 'drop', 'external' o cualquier otra
            self.rb_public.setChecked(True)

        layout.addSpacing(20)

        # Botón de aplicar
        self.btn_apply = QPushButton(locales.get_text("zone_btn_apply"))
        self.btn_apply.setFixedWidth(200)
        self.btn_apply.clicked.connect(self.apply_zone)
        layout.addWidget(self.btn_apply)

        layout.addStretch()
        self.setLayout(layout)

    def apply_zone(self):
        selected_id = self.bg_zones.checkedId()

        # Mapeamos la selección a zonas reales de firewalld
        if selected_id == 1:
            target_zone = "public"  # Desconocida
            zone_friendly = "Pública"
        else:
            target_zone = "home"    # Conocida
            zone_friendly = "Casa/Trabajo"

        # Ejecutamos el cambio (Pedirá contraseña)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        success = self.detector.set_default_zone(target_zone)
        QApplication.restoreOverrideCursor()

        if success:
            QMessageBox.information(self, "Éxito", locales.get_text("zone_apply_success").format(zone_friendly))

            # ¡AQUÍ ESTÁ LA MAGIA!
            # Emitimos la señal para avisar al resto de la app
            self.zone_changed.emit()
        else:
            QMessageBox.critical(self, "Error", locales.get_text("msg_error_cmd"))

    def update_selection_visuals(self, zone):
        """Método auxiliar para cambiar el radio button visualmente desde fuera"""
        if zone == "public":
            self.rb_public.setChecked(True)
        else:
            self.rb_home.setChecked(True)

        # Emitimos la señal para que se recarguen las tablas de reglas
        self.zone_changed.emit()

# Clases Placeholder para las otras pestañas
class PlaceholderPanel(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()
        lbl = QLabel(f"🚧 {text} \n(Próximamente)")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        self.setLayout(layout)

# En tab_firewall.py -> Agrega QCompleter si quieres autocompletado pro,
# pero QComboBox editable sirve bien.

class SelectAppDialog(QDialog):
    def __init__(self, all_services, parent=None):
        super().__init__(parent)
        self.setWindowTitle(locales.get_text("add_app_title"))
        self.setFixedSize(350, 150)
        self.all_services = all_services
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel(locales.get_text("add_app_label")))

        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.addItems(self.all_services)

        # --- AQUÍ ESTÁ LA MAGIA DE QCOMPLETER ---
        # 1. Creamos el autocompletador pasándole la misma lista de servicios
        completer = QCompleter(self.all_services, self)

        # 2. Configuración PRO: "MatchContains"
        # Esto permite que si escribes "mana", te encuentre "network-manager".
        # El comportamiento por defecto es "StartsWith" (solo busca el inicio).
        completer.setFilterMode(Qt.MatchContains)

        # 3. Ignorar mayúsculas/minúsculas (SSH = ssh)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        # 4. Asignamos este cerebro mejorado a nuestro combo
        self.combo.setCompleter(completer)
        # ----------------------------------------

        layout.addWidget(self.combo)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(locales.get_text("add_app_btn_save"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_selected_app(self):
        return self.combo.currentText()

class AppsPanel(QWidget):
    def __init__(self, mode="allow"):
        """
        mode: 'allow' (Lista blanca) o 'block' (Lista negra/Rich Rules)
        """
        super().__init__()
        self.mode = mode
        self.detector = FirewallDetector()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Título dinámico
        title_key = "apps_allow_title" if self.mode == "allow" else "apps_block_title"
        lbl_title = QLabel(locales.get_text(title_key))
        lbl_title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(lbl_title)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([
            locales.get_text("apps_header_name"),
            locales.get_text("apps_header_desc")
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus) # Quitamos el borde azul al seleccionar
        layout.addWidget(self.table)

        # Botones
        toolbar = QHBoxLayout()

        self.btn_add = QPushButton("➕ " + locales.get_text("apps_btn_add"))
        self.btn_add.clicked.connect(self.action_add)
        toolbar.addWidget(self.btn_add)

        self.btn_del = QPushButton("➖ " + locales.get_text("apps_btn_remove"))
        self.btn_del.setStyleSheet("background-color: #d32f2f; color: white;")
        self.btn_del.clicked.connect(self.action_remove)
        toolbar.addWidget(self.btn_del)

        toolbar.addStretch()

        btn_refresh = QPushButton("🔄 " + locales.get_text("btn_refresh_rules"))
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.load_data)
        toolbar.addWidget(btn_refresh)

        layout.addLayout(toolbar)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)

        # Obtenemos la lista según el modo
        if self.mode == "allow":
            services = self.detector.get_active_services()
            empty_msg = locales.get_text("apps_no_allowed")
            color = "#4CAF50" # Verde
        else:
            services = self.detector.get_blocked_services()
            empty_msg = locales.get_text("apps_no_blocked")
            color = "#d32f2f" # Rojo

        if not services:
            # Opcional: Poner item de aviso
            return

        self.table.setRowCount(len(services))
        for row, svc in enumerate(services):
            item_name = QTableWidgetItem(svc)
            item_name.setForeground(QColor(color))
            item_name.setFont(QFont("Arial", 10, QFont.Bold))

            # Descripción (Dummy por ahora, firewalld tiene descripciones pero es complejo sacarlas)
            item_desc = QTableWidgetItem(f"Servicio {svc}")

            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_desc)

    def action_add(self):
        # 1. Obtenemos TODOS los servicios posibles para llenar la lista
        all_svcs = self.detector.get_all_available_services()

        dialog = SelectAppDialog(all_svcs, self)
        if dialog.exec():
            selected = dialog.get_selected_app()
            if not selected: return

            QApplication.setOverrideCursor(Qt.WaitCursor)
            # manage_service(action="add", name, mode="allow/block")
            success = self.detector.manage_service("add", selected, self.mode)
            QApplication.restoreOverrideCursor()

            if success:
                self.load_data()
            else:
                QMessageBox.critical(self, "Error", locales.get_text("msg_error_cmd"))

    def action_remove(self):
        current_row = self.table.currentRow()
        if current_row < 0: return

        svc_name = self.table.item(current_row, 0).text()

        QApplication.setOverrideCursor(Qt.WaitCursor)
        success = self.detector.manage_service("remove", svc_name, self.mode)
        QApplication.restoreOverrideCursor()

        if success:
            self.load_data()
        else:
            QMessageBox.critical(self, "Error", locales.get_text("msg_error_cmd"))

# ==========================================
# CLASE PRINCIPAL (FirewallTab)
# ==========================================

class FirewallTab(QWidget):
    def __init__(self):
        super().__init__()
        self.detector = FirewallDetector()
        self.installer = FirewallInstaller()
        self.net_utils = NetworkUtils() # <--- Instanciamos utils
        self.cfg = ConfigManager()      # <--- Instanciamos config
        self.current_service = None
        self.last_known_net = None
        self.init_ui()

        # --- MONITORIZACIÓN DE RED (AUTO-PILOT) ---
        self.net_timer = QTimer(self)
        self.net_timer.timeout.connect(self.check_network_change)
        self.net_timer.start(5000) # Chequear cada 5000ms (5 segundos)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # --- 1. CABECERA (Header) ---
        header_layout = QHBoxLayout()
        title = QLabel(locales.get_text("fw_title"))
        title.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.lbl_status_text = QLabel("...")
        self.lbl_status_text.setFont(QFont("Arial", 10, QFont.Bold))
        self.lbl_status_text.setContentsMargins(0, 0, 10, 0)
        header_layout.addWidget(self.lbl_status_text)

        self.toggle = ToggleSwitch()
        self.toggle.clicked.connect(self.on_toggle_click)
        header_layout.addWidget(self.toggle)
        main_layout.addLayout(header_layout)

        # --- 2. INFO TÉCNICA Y LÍNEA ---
        self.lbl_tech_info = QLabel("-")
        self.lbl_tech_info.setStyleSheet("color: gray; font-size: 11px;")
        self.lbl_tech_info.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.lbl_tech_info)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(line)

        # --- 3. ZONA DE PESTAÑAS ---
        self.tabs_firewall = QTabWidget()
        self.tabs_firewall.setFocusPolicy(Qt.NoFocus) # Sin borde de foco
        self.tabs_firewall.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444444;
            }
            QTabBar::tab { padding: 8px 15px; outline: 0px; }
            QTabBar::tab:selected { font-weight: bold; }
        """)

        # A. Instanciamos TODOS los paneles
        self.panel_net = NetworkTypePanel()
        self.panel_in = InboundRulesPanel()
        self.panel_out = OutboundRulesPanel()
        self.panel_apps_allow = AppsPanel(mode="allow")
        self.panel_apps_block = AppsPanel(mode="block")

        # B. Conectamos la señal de cambio de zona a TODOS los paneles que lo necesitan
        # (Así cuando cambies de zona, se actualizan las reglas y las apps)
        self.panel_net.zone_changed.connect(self.panel_in.load_rules)
        self.panel_net.zone_changed.connect(self.panel_out.load_rules)
        self.panel_net.zone_changed.connect(self.panel_apps_allow.load_data)
        self.panel_net.zone_changed.connect(self.panel_apps_block.load_data)

        # C. Añadimos las pestañas AL WIDGET (Solo una vez cada una)
        self.tabs_firewall.addTab(self.panel_net, locales.get_text("fw_tab_net_type"))
        self.tabs_firewall.addTab(self.panel_in, locales.get_text("fw_tab_rules_in"))
        self.tabs_firewall.addTab(self.panel_out, locales.get_text("fw_tab_rules_out"))
        self.tabs_firewall.addTab(self.panel_apps_allow, locales.get_text("fw_tab_apps_allow"))
        self.tabs_firewall.addTab(self.panel_apps_block, locales.get_text("fw_tab_apps_block"))

        main_layout.addWidget(self.tabs_firewall)

        self.setLayout(main_layout)
        self.check_status()

    def check_status(self):
        self.toggle.blockSignals(True)
        status = self.detector.detect()
        self.current_service = None

        if status.type == FirewallType.FIREWALLD:
            self.current_service = "firewalld"
        elif status.type == FirewallType.UFW:
            self.current_service = "ufw"

        # 1. Actualizar el Toggle
        self.toggle.setChecked(status.active)

        # 2. Lógica de Activación de UI
        if self.current_service:
            self.update_ui_state(status.active, status.details)
            self.toggle.setEnabled(True)

            # --- LÓGICA DE PESTAÑAS (Aquí está el cambio) ---
            if status.active:
                self.tabs_firewall.setEnabled(True)

                # CASO UFW: Desactivar Pestaña 0 (Tipo de Red)
                if self.current_service == "ufw":
                    # Deshabilitar la pestaña 0 (Zonas)
                    self.tabs_firewall.setTabEnabled(0, False)
                    self.tabs_firewall.setTabToolTip(0, locales.get_text("msg_ufw_no_zones"))

                    # Si estamos en la pestaña 0, nos movemos a la 1 (Reglas) forzosamente
                    if self.tabs_firewall.currentIndex() == 0:
                        self.tabs_firewall.setCurrentIndex(1)

                # CASO FIREWALLD: Todo habilitado
                else:
                    self.tabs_firewall.setTabEnabled(0, True)
                    self.tabs_firewall.setTabToolTip(0, "")

            else:
                # Si el firewall está apagado, deshabilitamos todo el panel de pestañas
                self.tabs_firewall.setEnabled(False)
            # ------------------------------------------------

        else:
            # Caso sin gestor instalado
            self.lbl_status_text.setText(locales.get_text("fw_missing_title"))
            self.lbl_status_text.setStyleSheet("color: orange;")
            self.lbl_tech_info.setText(locales.get_text("fw_missing_desc"))
            self.toggle.setEnabled(True)
            self.tabs_firewall.setEnabled(False)

        self.toggle.blockSignals(False)

    def update_ui_state(self, is_active, details):
        service_name = self.current_service if self.current_service else "Desconocido"
        if is_active:
            self.lbl_status_text.setText(locales.get_text("fw_status_active"))
            self.lbl_status_text.setStyleSheet("color: #2ecc71;")
            self.lbl_tech_info.setText(locales.get_text("fw_backend").format(service_name))
        else:
            self.lbl_status_text.setText(locales.get_text("fw_status_inactive"))
            self.lbl_status_text.setStyleSheet("color: #e74c3c;")
            self.lbl_tech_info.setText(locales.get_text("fw_warning").format(service_name))

    def on_toggle_click(self):
        target_state = self.toggle.isChecked()

        if not self.current_service:
            # Lógica de instalación (reutilizada)
            self.toggle.blockSignals(True)
            self.toggle.setChecked(False)
            self.toggle.blockSignals(False)

            dialog = InstallDialog(self)
            if dialog.exec():
                fw_to_install = dialog.get_selected_firewall()
                self.progress = QProgressDialog(
                    locales.get_text("inst_status_working"), None, 0, 0, self)
                self.progress.setWindowTitle("SentinelX")
                self.progress.setWindowModality(Qt.WindowModal)
                self.progress.setMinimumDuration(0)

                self.worker = InstallWorker(self.installer, fw_to_install)
                self.worker.finished_signal.connect(self.on_install_finished)
                self.progress.show()
                self.worker.start()
            return

        # Lógica de toggle
        QApplication.processEvents()
        success = self.detector.set_firewall_state(self.current_service, target_state)

        if success:
            self.update_ui_state(target_state, f"Gestionado por {self.current_service}")
            self.tabs_firewall.setEnabled(target_state) # Activar/Desactivar pestañas
        else:
            self.toggle.blockSignals(True)
            self.toggle.setChecked(not target_state)
            self.toggle.blockSignals(False)

    def on_install_finished(self, success):
        self.progress.close()
        fw_name = self.worker.fw_name
        if success:
            QMessageBox.information(self, locales.get_text("inst_success_title"),
                locales.get_text("inst_success_msg").format(fw_name))
            self.check_status()
        else:
            QMessageBox.critical(self, locales.get_text("inst_error_title"),
                locales.get_text("inst_error_msg"))

    # --- LÓGICA AUTOMÁTICA WIFI ---
    def check_network_change(self):
        # 1. Si no hay firewall activo (o es UFW que no soporta zonas), no hacemos nada
        if not self.current_service or self.current_service == "ufw":
            return

        # 2. Detectar red actual
        current_net_name = self.net_utils.get_active_connection_name()

        # Si no hay red o es la misma que ya procesamos, salir
        if not current_net_name or current_net_name == self.last_known_net:
            return

        # 3. ¡Cambio de red detectado!
        print(f"Red cambiada: {self.last_known_net} -> {current_net_name}")
        self.last_known_net = current_net_name # Actualizamos memoria inmediata

        # 4. Consultar Base de Datos
        saved_zone = self.cfg.get_network_zone(current_net_name)

        if saved_zone:
            # A) RED CONOCIDA -> Aplicar silencio
            print(f"Red conocida. Aplicando zona: {saved_zone}")

            # Solo aplicamos si la zona actual del sistema es diferente (para no spamear comandos)
            current_system_zone = self.detector.get_default_zone()
            if current_system_zone != saved_zone:
                self.detector.set_default_zone(saved_zone)
                # Actualizamos la UI visualmente
                self.panel_net.update_selection_visuals(saved_zone) # (Necesitaremos crear este helper)
                # Notificación flotante (Toast) o en la barra de estado
                # Por ahora un print, o podríamos usar un QSystemTrayIcon
        else:
            # B) RED NUEVA -> Preguntar
            # Pausamos el timer para que no salte otra vez mientras decidimos
            self.net_timer.stop()

            # Traemos la ventana al frente
            if self.window():
                self.window().activateWindow()

            dialog = NewNetworkDialog(current_net_name, self)
            if dialog.exec():
                chosen_zone = dialog.selected_zone

                # 1. Guardar en BD
                self.cfg.save_network_zone(current_net_name, chosen_zone)

                # 2. Aplicar
                self.detector.set_default_zone(chosen_zone)
                self.panel_net.update_selection_visuals(chosen_zone)

            # Reanudamos el timer
            self.net_timer.start(5000)
