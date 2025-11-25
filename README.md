# 🛡️ SentinelX

> **Tu Guardián de Red para Linux. Simple. Potente. Inteligente.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-Dual%20(LGPLv3%20%2F%20Commercial)-orange)](#-licencia)
[![Linux](https://img.shields.io/badge/Platform-Linux-black?logo=linux&logoColor=white)](https://www.kernel.org/)

**SentinelX** es una interfaz gráfica (GUI) moderna diseñada para simplificar la gestión del cortafuegos en Linux. Pensada para usuarios que vienen de otros sistemas operativos o que prefieren no usar la terminal, SentinelX abstrae la complejidad de `firewalld` y `ufw`, ofreciendo una experiencia de seguridad robusta y accesible.

---

## ✨ Características Principales

* **🕵️ Detección Inteligente de Red:** Detecta automáticamente si estás conectado a una red nueva y te permite clasificarla (Casa/Pública) para ajustar la seguridad al instante.
* **🔌 Gestión de Puertos (Entrada/Salida):** Abre o bloquea puertos fácilmente. Incluye una base de datos interna para que puedas poner nombres personalizados a tus reglas (ej: "8080" -> "Mi Servidor Web").
* **📦 Control de Aplicaciones:** Permite o bloquea servicios completos (Steam, SSH, HTTP) sin necesidad de saber los puertos exactos.
* **🔄 Multi-Backend:** Funciona tanto con **Firewalld** (Fedora, Manjaro, OpenSUSE) como con **UFW** (Ubuntu, Debian, Mint).
* **🎨 Interfaz Moderna:** Desarrollada en Qt6 (PySide6) con soporte para temas Claro y Oscuro.
* **🌍 Multi-idioma:** Disponible en Español e Inglés.

---

## 📸 Capturas de Pantalla

*(Aquí puedes subir tus capturas a la carpeta 'screenshots' del repo y enlazarlas)*

![Dashboard Principal](https://via.placeholder.com/800x450?text=Captura+SentinelX)

---

## 🚀 Instalación y Uso

### Requisitos previos
* Python 3.8 o superior.
* Un gestor de firewall instalado (`firewalld` o `ufw`).
* Permisos de administrador (la app solicitará contraseña vía `pkexec` para aplicar cambios).

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
    *(Asegúrate de tener PySide6 en tu requirements.txt)*

4.  **Ejecutar la aplicación:**
    ```bash
    python SentinelX.py
    ```

---

## 🛠️ Tecnologías

* **Lenguaje:** Python 3
* **Interfaz Gráfica:** PySide6 (Qt for Python)
* **Integración Sistema:** `subprocess` para comunicación con `firewall-cmd`, `ufw` y `nmcli`.
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

**Daniel Serrano Armenta**

* 📧 **Email:** [dani.eus79@gmail.com](mailto:dani.eus79@gmail.com)
* 🐙 **GitHub:** [github.com/danitxu79](https://github.com/danitxu79/)
* 🌐 **Portafolio:** [danitxu79.github.io](https://danitxu79.github.io/)

---
*Si encuentras útil este proyecto, ¡no olvides darle una ⭐ en GitHub!*
