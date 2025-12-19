<div align="center">
  <a href="https://github.com/AnabasaSoft/SentinelX">
    <img src="https://raw.githubusercontent.com/danitxu79/SentinelX/main/AnabasaSoft.png" width="600" alt="AnabasaSoft Logo">
  </a>

  <br><br>

  <a href="https://github.com/AnabasaSoft/SentinelX">
    <img src="https://raw.githubusercontent.com/danitxu79/SentinelX/main/SentinelX-Logo.png" width="250" alt="SentinelX Logo">
  </a>

  <h1>SentinelX</h1>

  <p>
    <b>Tu Suite de Seguridad para Linux. Firewall Inteligente & Antivirus en Tiempo Real.</b>
  </p>

  <p>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
    </a>
    <a href="https://doc.qt.io/qtforpython/">
      <img src="https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green?logo=qt&logoColor=white" alt="Qt6">
    </a>
    <a href="https://aur.archlinux.org/packages/sentinelx-bin">
      <img src="https://img.shields.io/aur/version/sentinelx-bin?color=purple&label=AUR&logo=arch-linux" alt="AUR Version">
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
* **🔌 Control de Puertos (Entrada/Salida):** Abre o bloquea puertos fácilmente con una base de datos de nombres personalizados para recordar qué es cada regla.
* **📦 Filtrado por Aplicaciones:** Permite o bloquea servicios completos (Steam, SSH, HTTP) sin necesidad de saber los puertos técnicos.
* **🔄 Multi-Backend:** Funciona nativamente tanto con **Firewalld** (Fedora, Manjaro, OpenSUSE) como con **UFW** (Ubuntu, Debian, Mint).

### 🦠 Protección Antivirus (ClamAV)
* **🛡️ Protección en Tiempo Real (On-Access):** Vigila carpetas críticas (configurable) y bloquea el acceso a archivos infectados al instante usando `clamonacc`.
* **🚀 Control del Daemon:** Gestión inteligente de los servicios en segundo plano para equilibrar rendimiento y seguridad.
* **🔍 Escaneo Flexible:** Análisis bajo demanda de carpetas o sistema completo con logs en tiempo real y control de parada.
* **⚙️ Gestión Automática:** Detección e instalación automática del motor y firmas si no están presentes.

### 🚀 Experiencia de Usuario (UX)
* **🔐 Smart Polkit (Auto-Privilegios):** Olvídate de escribir tu contraseña constantemente. SentinelX instala un sistema seguro de reglas (`polkit`) y scripts auxiliares para permitir la administración fluida sin comprometer la seguridad.
* **🎨 Interfaz Moderna:** Desarrollada en Qt6 con temas Claro y Oscuro pulidos profesionalmente.
* **🌍 Multi-idioma:** Disponible totalmente en Español, Inglés y Euskera.

---

## 📸 Capturas de Pantalla

<div align="center">
  <img src="https://raw.githubusercontent.com/danitxu79/SentinelX/main/Captura01.png" alt="Captura de Pantalla SentinelX" width="800">
</div>

---

## 📥 Instalación y Descarga

Elige el método que mejor se adapte a tu distribución.

### 🦅 Arch Linux / Manjaro (AUR)
La forma recomendada para usuarios de Arch. El paquete se actualiza automáticamente.

```bash
yay -S sentinelx-bin
# o
pamac build sentinelx-bin
```

### 🎒 AppImage (Universal Portable)

Funciona en cualquier distribución (Ubuntu, Fedora, OpenSUSE, etc.) sin instalación.

1. Descarga el archivo `.AppImage` desde la sección **[Releases](https://github.com/AnabasaSoft/SentinelX/releases)**.
2. Dale permisos de ejecución:
   ```bash
   chmod +x SentinelX-*.AppImage
   ```
3. Haz doble clic para abrirlo.

### 📦 Paquetes Nativos (.deb / .rpm)

Disponibles en la sección **[Releases](https://github.com/AnabasaSoft/SentinelX/releases)**.

* **Debian/Ubuntu/Mint:** Descarga el `.deb` e instálalo con `sudo apt install ./archivo.deb`.
* **Fedora/RHEL/Suse:** Descarga el `.rpm` e instálalo con `sudo dnf install ./archivo.rpm`.

---

## 👨‍💻 Ejecutar desde Código Fuente (Para Desarrolladores)

Si quieres contribuir o modificar el código, sigue estos pasos.

**Requisitos:**

* Python 3.10 o superior.
* Librerías de sistema para Qt6.

**Pasos:**

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/AnabasaSoft/SentinelX.git
   cd SentinelX
   ```

2. **Crear un entorno virtual (Recomendado):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**

   ```bash
   python SentinelX.py
   ```

> **Nota sobre el primer inicio:** SentinelX detectará si faltan permisos de sistema y te ofrecerá instalar una regla de seguridad automáticamente. Esto es necesario para gestionar el firewall y el antivirus de forma fluida sin pedir contraseñas constantemente.

---

## 🛠️ Tecnologías

* **Lenguaje:** Python 3
* **Interfaz Gráfica:** PySide6 (Qt for Python)
* **Seguridad:** Integración con `polkit` y scripts auxiliares seguros en `/usr/local/bin`.
* **Motores:** `firewalld`, `ufw`, `clamav` (`clamd`, `clamonacc`), `nmcli`.
* **Persistencia:** JSON para configuración de usuario en `~/.config/SentinelX`.

---

## 📄 Licencia

Este proyecto se ofrece bajo un modelo de **Doble Licencia (Dual License)**:

1. **LGPLv3 (GNU Lesser General Public License v3):**
   Ideal para proyectos de código abierto. Si usas esta biblioteca (especialmente si la modificas), debes cumplir con las obligaciones de la LGPLv3. Esto asegura que las mejoras al núcleo open-source se compartan con la comunidad.

2. **Comercial (Privativa):**
   Si los términos de la LGPLv3 no se ajustan a tus necesidades (por ejemplo, para incluir este software en productos propietarios de código cerrado sin revelar el código fuente), por favor contacta al autor para adquirir una licencia comercial.

Para más detalles, consulta el archivo `LICENSE` incluido en este repositorio.

---

## 📬 Contacto y Autor

Este proyecto ha sido desarrollado con ❤️ y mucho café por:

**Daniel Serrano Armenta (AnabasaSoft)**

* 📧 **Email:** [anabasasoft@gmail.com](mailto:anabasasoft@gmail.com)
* 🐙 **GitHub:** [github.com/danitxu79](https://github.com/danitxu79/)
* 🌐 **Portafolio:** [danitxu79.github.io](https://danitxu79.github.io/)

---

*Si encuentras útil este proyecto, ¡no olvides darle una ⭐ en GitHub!*


<div align="center">
  <br/>
  <p><code>>_ sudo buy-me-a-coffee --theme=dark --force</code></p>
  <a href="https://www.buymeacoffee.com/danitxu" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-black.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 180px !important; box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;">
  </a>
  <br/>
</div>
