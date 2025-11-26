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
* **🌍 Multi-idioma:** Disponible totalmente en Español e Inglés.

---

## 📸 Capturas de Pantalla

<div align="center">
  <img src="https://raw.githubusercontent.com/danitxu79/SentinelX/main/Captura01.png" alt="Captura de Pantalla SentinelX" width="800">
</div>

---

## 🚀 Instalación

### Opción A: Arch Linux / Manjaro (AUR)
La forma más fácil si usas una distribución basada en Arch:

```bash
yay -S sentinelx-bin
# o
pamac build sentinelx-bin
