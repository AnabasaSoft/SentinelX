from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTableWidget, QHeaderView,
                               QAbstractItemView, QTableWidgetItem, QMessageBox)
from PySide6.QtGui import QFont, QColor, QCursor
from PySide6.QtCore import Qt

import locales
from antivirus_manager import AntivirusManager

class QuarantineTab(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = AntivirusManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        lbl_title = QLabel("☣️ " + locales.get_text("quarantine_title"))
        lbl_title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(lbl_title)

        lbl_desc = QLabel(locales.get_text("quarantine_desc"))
        lbl_desc.setStyleSheet("color: #888;")
        layout.addWidget(lbl_desc)

        layout.addSpacing(10)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([
            locales.get_text("quarantine_header_date"),
            locales.get_text("quarantine_header_file")
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.table)

        # Botones
        btn_layout = QHBoxLayout()

        self.btn_restore = QPushButton("↩️ " + locales.get_text("quarantine_btn_restore"))
        self.btn_restore.clicked.connect(self.action_restore)

        self.btn_delete = QPushButton("🗑️ " + locales.get_text("quarantine_btn_delete"))
        self.btn_delete.setStyleSheet("background-color: #d32f2f; color: white;")
        self.btn_delete.clicked.connect(self.action_delete)

        # --- BOTÓN REFRESCAR MEJORADO ---
        # Ahora tiene texto y tooltip
        btn_text = locales.get_text("btn_refresh_rules")
        self.btn_refresh = QPushButton(f"🔄 {btn_text}")
        self.btn_refresh.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_refresh.setToolTip(locales.get_text("quarantine_refresh_tooltip"))
        self.btn_refresh.clicked.connect(self.load_data)
        # --------------------------------

        btn_layout.addWidget(self.btn_restore)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_refresh)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.load_data()

    # --- AUTO-REFRESCO AL ENTRAR ---
    def showEvent(self, event):
        """Se ejecuta automáticamente cada vez que esta pestaña se hace visible"""
        super().showEvent(event)
        self.load_data()
    # -------------------------------

    def load_data(self):
        self.table.setRowCount(0)
        files = self.manager.get_quarantine_files()

        self.table.setRowCount(len(files))
        for row, file_data in enumerate(files):
            date_item = QTableWidgetItem(file_data['date'])
            path_item = QTableWidgetItem(file_data['original_path'])

            # Guardamos el ID real (nombre en disco) en el item para usarlo luego
            date_item.setData(Qt.UserRole, file_data['id'])

            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, path_item)

    def get_selected_id(self):
        row = self.table.currentRow()
        if row < 0: return None
        return self.table.item(row, 0).data(Qt.UserRole)

    def action_restore(self):
        fid = self.get_selected_id()
        if not fid:
            QMessageBox.warning(self, "Aviso", locales.get_text("msg_error_select"))
            return

        if self.manager.restore_file(fid):
            QMessageBox.information(self, "Info", locales.get_text("quarantine_success_restore"))
            self.load_data()
        else:
            QMessageBox.warning(self, "Error", "No se pudo restaurar el archivo (¿permisos?).")

    def action_delete(self):
        fid = self.get_selected_id()
        if not fid:
            QMessageBox.warning(self, "Aviso", locales.get_text("msg_error_select"))
            return

        # Obtener nombre visual para el mensaje
        row = self.table.currentRow()
        name_visual = self.table.item(row, 1).text()

        reply = QMessageBox.question(self, "Confirmar",
                                     locales.get_text("quarantine_confirm_delete").format(name_visual),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.manager.delete_quarantine_file(fid):
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", "No se pudo borrar el archivo.")
