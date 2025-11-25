from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AntivirusTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Módulo de Antivirus (Próximamente)"))
        layout.addStretch()
        self.setLayout(layout)
