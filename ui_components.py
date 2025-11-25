from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QPainter, QColor, QBrush

class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Dimensiones más pequeñas: Ancho 50px, Alto 26px
        self.setFixedSize(50, 26)

        self.setStyleSheet("""
            QCheckBox { spacing: 0px; color: transparent; }
            QCheckBox::indicator { width: 50px; height: 26px; border-radius: 13px; }
            QCheckBox::indicator:unchecked { background-color: #e6e6e6; border: 2px solid #bdc3c7; }
            QCheckBox::indicator:unchecked:hover { background-color: #dcdcdc; }
            QCheckBox::indicator:checked { background-color: #2ecc71; border: 2px solid #27ae60; }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Matemáticas para el círculo (Thumb)
        circle_dia = 20  # Diámetro más pequeño
        margin = 3       # Margen interno

        if self.isChecked():
            # Posición derecha (Ancho total 50 - circulo 20 - margen 3 - borde 2)
            x_pos = 50 - circle_dia - margin - 2
            brush_color = QColor(255, 255, 255)
        else:
            # Posición izquierda
            x_pos = margin + 2
            brush_color = QColor(255, 69, 58) # Rojo

        painter.setBrush(QBrush(brush_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x_pos, margin, circle_dia, circle_dia)
        painter.end()
