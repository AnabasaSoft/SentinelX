from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QFrame
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import locales

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Visor de texto enriquecido (HTML)
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True) # ¡Importante para los links!

        # En tab_help.py

        # Construimos el HTML (Añadimos la sección de Sistema al principio)
        html_content = f"""
        <h1 style="color: #4CAF50;">{locales.get_text("help_title")}</h1>
        <hr>

        <h2 style="color: #FF9800;">{locales.get_text("h_sys_title")}</h2>
        {locales.get_text("h_sys_desc")}
        <br>

        <h2 style="color: #3498DB;">{locales.get_text("h_fw_title")}</h2>
        {locales.get_text("h_fw_desc")}
        <br>

        <h2 style="color: #e74c3c;">{locales.get_text("h_av_title")}</h2>
        {locales.get_text("h_av_desc")}

        <br><hr><br>

        <h3>{locales.get_text("h_contact_title")}</h3>
        <p>{locales.get_text("h_contact_desc")}</p>

        <p><b>{locales.get_text("h_links")}</b></p>
        <ul>
            <li><a href="https://danitxu79.github.io/" style="color: #4CAF50; text-decoration: none; font-weight: bold;">
                {locales.get_text("h_portfolio")}
            </a></li>
            <li><a href="https://github.com/danitxu79/SentinelX" style="color: #3498DB; text-decoration: none; font-weight: bold;">
                {locales.get_text("h_github")}
            </a></li>
        </ul>
        <p>{locales.get_text("h_email")}</p>
        """

        self.browser.setHtml(html_content)

        # Estilo específico para que el navegador se integre con el tema
        # Usamos fondo transparente para heredar el color del frame/ventana
        self.browser.setStyleSheet("background-color: transparent; border: none;")

        layout.addWidget(self.browser)
        self.setLayout(layout)
