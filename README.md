<div align="center">
  <a href="https://github.com/danitxu79/SentinelX">
    <img src="https://raw.githubusercontent.com/danitxu79/SentinelX/main/AnabasaSoft.png" width="600" alt="AnabasaSoft Logo">
  </a>

  <br><br>

  <a href="https://github.com/danitxu79/SentinelX">
    <img src="https://raw.githubusercontent.com/danitxu79/SentinelX/main/SentinelX-Logo.png" width="250" alt="SentinelX Logo">
  </a>

  <h1>SentinelX</h1>

  <p>
    <b>Tu Suite de Seguridad para Linux. Firewall Inteligente & Antivirus.</b>
  </p>

  <p>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
    </a>
    <a href="https://doc.qt.io/qtforpython/">
      <img src="https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green?logo=qt&logoColor=white" alt="Qt6">
    </a>
    <a href="#-licencia">
      <img src="https://img.shields.io/badge/License-Dual%20(LGPLv3%20%2F%20Commercial)-orange" alt="License">
    </a>
    <a href="https://www.kernel.org/">
      <img src="https://img.shields.io/badge/Platform-Linux-black?logo=linux&logoColor=white" alt="Platform Linux">
    </a>
  </p>
</div>

---

**SentinelX** es una interfaz gráfica (GUI) moderna diseñada para simplificar la seguridad en Linux. Pensada para usuarios que vienen de otros sistemas operativos o que prefieren no usar la terminal, SentinelX unifica la gestión del cortafuegos (`firewalld`/`ufw`) y la protección contra malware (`ClamAV`) en una experiencia robusta y accesible.

---

## ✨ Características Principales

### 🔥 Gestión de Firewall Avanzada
* **🕵️ Detección Inteligente de Red:** Monitoriza tu conexión y te permite clasificar redes automáticamente (Casa/Pública) para ajustar la seguridad al instante.
* **🔌 Control de Puertos (Entrada/Salida):** Abre o bloquea puertos fácilmente con una base de datos de nombres personalizados.
* **📦 Filtrado por Aplicaciones:** Permite o bloquea servicios completos (Steam, SSH, HTTP) sin necesidad de saber los puertos técnicos.
* **🔄 Multi-Backend:** Funciona nativamente tanto con **Firewalld** (Fedora, Manjaro, OpenSUSE) como con **UFW** (Ubuntu, Debian, Mint).

### 🦠 Protección Antivirus (ClamAV)
* **🛡️ Control del Daemon:** Activa o desactiva el servicio en segundo plano (`clamav-daemon`) con un solo clic para optimizar el rendimiento.
* **🔍 Escaneo Flexible:** Realiza análisis rápidos de tu carpeta personal o escaneos profundos del sistema completo con visualización de logs en tiempo real.
* **⚙️ Gestión Automática:** SentinelX detecta si ClamAV falta en tu sistema y te ofrece instalarlo automáticamente usando el gestor de paquetes de tu distribución.

### 🚀 Experiencia de Usuario (UX)
* **🔐 Smart Polkit (Auto-Privilegios):** Olvídate de escribir tu contraseña constantemente. SentinelX instala y gestiona automáticamente reglas de política (`polkit`) para permitir la administración segura sin interrupciones.
* **🎨 Interfaz Moderna:** Desarrollada en Qt6 (PySide6) con soporte nativo para temas Claro y Oscuro.
* **🌍 Multi-idioma:** Disponible totalmente en Español e Inglés.

---

## 📸 Capturas de Pantalla

<div align="center">
  <img src="https://raw.githubusercontent.com/danitxu79/SentinelX/main/Captura01.png" alt="Captura de Pantalla SentinelX" width="800">
</div>

---

## 🚀 Instalación y Uso

### Requisitos previos
* Python 3.8 o superior.
* Permisos de administrador (la app configurará las reglas de permisos en el primer inicio).

### Pasos de instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/danitxu79/SentinelX.git](https://github.com/danitxu79/SentinelX.git)
    cd SentinelX
    ```

2.  **Crear un entorno virtual (Recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    python SentinelX.py
    ```

> **Nota sobre el primer inicio:** SentinelX detectará si faltan permisos de sistema y te ofrecerá instalar una regla Polkit. Esto es necesario para gestionar el firewall y el antivirus de forma fluida.

---

## 🛠️ Tecnologías

* **Lenguaje:** Python 3
* **Interfaz Gráfica:** PySide6 (Qt for Python)
* **Seguridad:** Integración con `polkit` para elevación de privilegios segura.
* **Motores:** `firewalld`, `ufw`, `clamav`, `nmcli`.
* **Persistencia:** JSON para configuración de usuario y base de datos de redes conocidas.

---

## 📄 Licencia

Este proyecto se ofrece bajo un modelo de **Doble Licencia (Dual License)**:

1.  **LGPLv3 (GNU Lesser General Public License v3):**
    Ideal para proyectos de código abierto. Si usas esta biblioteca (especialmente si la modificas), debes cumplir con las obligaciones de la LGPLv3. Esto asegura que las mejoras al núcleo open-source se compartan con la comunidad.

2.  **Comercial (Privativa):**
    Si los términos de la LGPLv3 no se ajustan a tus necesidades (por ejemplo, para incluir este software en productos propietarios de código cerrado sin revelar el código fuente), por favor contacta al autor para adquirir una licencia comercial.

Para más detalles, consulta el archivo `LICENSE` incluido en este repositorio.

---

## 📬 Contacto y Autor

Este proyecto ha sido desarrollado con ❤️ y mucho café por:

**Daniel Serrano Armenta (AnabasaSoft)**

* 📧 **Email:** [dani.eus79@gmail.com](mailto:dani.eus79@gmail.com)
* 🐙 **GitHub:** [github.com/danitxu79](https://github.com/danitxu79/)
* 🌐 **Portafolio:** [danitxu79.github.io](https://danitxu79.github.io/)

---
*Si encuentras útil este proyecto, ¡no olvides darle una ⭐ en GitHub!*
