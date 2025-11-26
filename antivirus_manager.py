import shutil
import subprocess
import os
from PySide6.QtCore import QThread, Signal

# IMPORTANTE: Importamos el módulo de traducción
import locales

# --- HILO DE INSTALACIÓN ---
class InstallWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(bool)

    def run(self):
        # USO DE LOCALES
        self.log_signal.emit(locales.get_text("log_pkg_detect"))

        distro = self.get_distro_type()
        cmd = []

        if distro == "arch":
            cmd = ["pkexec", "pacman", "-S", "clamav", "--noconfirm"]
        elif distro == "debian":
            cmd = ["pkexec", "apt", "install", "clamav", "clamav-daemon", "-y"]
        elif distro == "redhat":
            cmd = ["pkexec", "dnf", "install", "clamav", "clamav-update", "-y"]
        elif distro == "suse":
            cmd = ["pkexec", "zypper", "install", "-n", "clamav"]
        else:
            # USO DE LOCALES
            self.log_signal.emit(locales.get_text("log_distro_error"))
            self.finished_signal.emit(False)
            return

        # USO DE LOCALES
        self.log_signal.emit(locales.get_text("log_executing").format(' '.join(cmd)))
        self.log_signal.emit(locales.get_text("log_pass_prompt"))

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                self.log_signal.emit(line.strip())

            process.wait()

            if process.returncode == 0:
                self.log_signal.emit(locales.get_text("log_install_ok"))
                self.finished_signal.emit(True)
            else:
                self.log_signal.emit(locales.get_text("log_process_error").format(process.returncode))
                self.finished_signal.emit(False)

        except Exception as e:
            self.log_signal.emit(locales.get_text("log_critical_error").format(e))
            self.finished_signal.emit(False)

    def get_distro_type(self):
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release", "r") as f:
                    content = f.read().lower()
                    if "arch" in content or "manjaro" in content: return "arch"
                    if "debian" in content or "ubuntu" in content or "mint" in content: return "debian"
                    if "fedora" in content or "rhel" in content: return "redhat"
                    if "suse" in content: return "suse"
        except: pass
        return "unknown"

# --- HILO DE ESCANEO ---
class ScanWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(bool, int)

    def __init__(self, target_path):
        super().__init__()
        self.target_path = target_path
        self.process = None # Referencia al proceso para poder matarlo
        self.killed_by_user = False

    def run(self):
        # USO DE LOCALES
        self.log_signal.emit(locales.get_text("log_scan_start").format(self.target_path))

        cmd = ["clamscan", "-r", self.target_path]

        try:
            # Guardamos la referencia en self.process
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )

            infected_count = 0

            # Leemos línea a línea
            for line in self.process.stdout:
                line = line.strip()
                self.log_signal.emit(line)
                if "FOUND" in line:
                    infected_count += 1

            self.process.wait()

            # Si fue matado por el usuario, no emitimos éxito ni fallo normal
            if self.killed_by_user:
                self.log_signal.emit(locales.get_text("av_scan_stopped"))
                self.finished_signal.emit(False, -1) # -1 indica cancelado
            else:
                success = self.process.returncode in [0, 1]
                self.finished_signal.emit(success, infected_count)

        except Exception as e:
            # Si el error fue porque lo matamos nosotros, lo ignoramos
            if not self.killed_by_user:
                self.log_signal.emit(locales.get_text("log_critical_error").format(e))
                self.finished_signal.emit(False, 0)

    def stop(self):
        """Método para matar el proceso desde fuera"""
        if self.process and self.process.poll() is None: # Si está corriendo
            self.killed_by_user = True
            self.process.terminate() # Intentamos terminar suavemente
            # self.process.kill() # Si terminate no funciona, usar kill

# --- HILO DE ACTUALIZACIÓN ---
class UpdateWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(bool)

    def run(self):
        # USO DE LOCALES
        self.log_signal.emit(locales.get_text("log_update_start"))
        try:
            process = subprocess.Popen(
                ["pkexec", "freshclam"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            for line in process.stdout:
                self.log_signal.emit(line.strip())
            process.wait()
            self.finished_signal.emit(process.returncode == 0)
        except Exception as e:
            self.log_signal.emit(locales.get_text("log_generic_error").format(e))
            self.finished_signal.emit(False)

class AntivirusManager:
    def is_installed(self):
        return shutil.which("clamscan") is not None

    def get_db_version(self):
        if not self.is_installed(): return "N/A"
        try:
            res = subprocess.run(["clamscan", "--version"], capture_output=True, text=True)
            return res.stdout.split("/")[0]
        except:
            return "Unknown"

    def is_daemon_active(self):
        """Comprueba si clamav-daemon o su socket están corriendo"""
        try:
            # Verificamos el servicio principal
            res_svc = subprocess.run(
                ["systemctl", "is-active", "--quiet", "clamav-daemon"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            # Verificamos también el socket (importante en Arch/Manjaro)
            res_sock = subprocess.run(
                ["systemctl", "is-active", "--quiet", "clamav-daemon.socket"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

            # Consideramos activo si cualquiera de los dos está vivo
            return (res_svc.returncode == 0) or (res_sock.returncode == 0)
        except:
            return False

    def set_daemon_state(self, enable: bool):
        """Activa/Desactiva Servicio Y Socket simultáneamente"""
        try:
            # Lista de unidades a controlar
            units = ["clamav-daemon.service", "clamav-daemon.socket"]

            if enable:
                # 1. Desbloquear
                cmd_unmask = ["pkexec", "systemctl", "unmask"] + units
                subprocess.run(cmd_unmask, stderr=subprocess.DEVNULL)

                # 2. Habilitar y arrancar AMBOS
                cmd_enable = ["pkexec", "systemctl", "enable", "--now"] + units
                subprocess.run(cmd_enable, check=True)

                # 3. Esperar un segundo para que systemd respire (evita falsos negativos)
                import time
                time.sleep(1)

            else:
                # Deshabilitar y parar AMBOS
                cmd_disable = ["pkexec", "systemctl", "disable", "--now"] + units
                subprocess.run(cmd_disable, check=True)

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error cambiando estado daemon: {e}")
            return False

    def get_clamd_conf_path(self):
        """Detecta la ubicación del archivo de configuración de ClamAV"""
        # Posibles rutas estándar
        paths = [
            "/etc/clamav/clamd.conf",       # Debian/Ubuntu
            "/etc/clamd.d/scan.conf",       # Fedora/CentOS
            "/etc/clamd.conf"               # Arch/Manjaro
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        return None

    def is_on_access_active(self):
        """Verifica si el servicio clamonacc está corriendo"""
        try:
            # El servicio suele llamarse 'clamav-clamonacc' o simplemente 'clamonacc'
            res = subprocess.run(
                ["systemctl", "is-active", "--quiet", "clamav-clamonacc"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if res.returncode == 0: return True

            # Intento alternativo (algunas distros lo llaman diferente)
            res = subprocess.run(
                ["systemctl", "is-active", "--quiet", "clamonacc"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return res.returncode == 0
        except:
            return False

    def configure_on_access(self, enable: bool, watch_path="/home"):
        conf_path = self.get_clamd_conf_path()
        if not conf_path:
            print("Error: No se encontró clamd.conf")
            return False

        helper = "/usr/local/bin/sentinelx-helper"

        try:
            if enable:
                # 1. Configurar archivo (Esto llamará al helper v7 corregido)
                subprocess.run(["pkexec", helper, "enable-on-access", conf_path, watch_path], check=True)

                # 2. Reiniciar el demonio principal
                subprocess.run(["pkexec", "systemctl", "restart", "clamav-daemon"], check=True)

                # 3. ESPERA ACTIVA (Wait loop)
                print("Esperando a que ClamAV Daemon esté listo...")
                import time
                max_retries = 30
                daemon_ready = False

                for _ in range(max_retries):
                    res = subprocess.run(["systemctl", "is-active", "clamav-daemon"], stdout=subprocess.DEVNULL)
                    # Chequeamos socket en rutas comunes de Linux
                    socket_exists = os.path.exists("/run/clamav/clamd.ctl") or \
                                    os.path.exists("/var/run/clamav/clamd.ctl") or \
                                    os.path.exists("/run/clamd.scan/clamd.sock") # Ruta Fedora

                    if res.returncode == 0 and socket_exists:
                        daemon_ready = True
                        break
                    time.sleep(1)

                if not daemon_ready:
                    print("Error: Tiempo de espera agotado. ClamAV Daemon no arrancó a tiempo.")
                    return False

                # 4. Ahora sí, arrancamos el vigilante
                subprocess.run(["pkexec", "systemctl", "enable", "--now", "clamav-clamonacc"], check=True)

            else:
                subprocess.run(["pkexec", "systemctl", "disable", "--now", "clamav-clamonacc"], check=True)
                subprocess.run(["pkexec", helper, "disable-on-access", conf_path], check=True)
                subprocess.run(["pkexec", "systemctl", "restart", "clamav-daemon"], check=True)

            return True

        except Exception as e:
            print(f"Error configurando On-Access: {e}")
            return False
