# firewall_detector.py
import shutil
import subprocess
from enum import Enum, auto
import socket

class FirewallType(Enum):
    FIREWALLD = auto()
    UFW = auto()
    NFTABLES = auto()
    IPTABLES = auto()
    UNKNOWN = auto()
    NONE = auto()

class FirewallStatus:
    def __init__(self):
        self.type = FirewallType.NONE
        self.active = False
        self.details = ""

# --- NUEVA CLASE PARA INSTALACIÓN ---
class FirewallInstaller:
    def get_distro_type(self):
        """
        Detecta la familia del sistema operativo leyendo /etc/os-release.
        Soporta: Arch (Manjaro), Debian (Ubuntu, Mint, Kali), RedHat (Fedora, CentOS), SUSE.
        """
        os_release_path = "/etc/os-release"
        distro_id = ""
        id_like = ""

        try:
            with open(os_release_path, "r") as f:
                for line in f:
                    # Limpiamos espacios y saltos de línea
                    line = line.strip()
                    if line.startswith("ID="):
                        # Quitamos comillas si las hay: ID="manjaro" -> manjaro
                        distro_id = line.split("=", 1)[1].strip('"').lower()
                    elif line.startswith("ID_LIKE="):
                        id_like = line.split("=", 1)[1].strip('"').lower()

            # Debug para que veas qué detecta
            print(f"DEBUG: Detectado ID='{distro_id}', ID_LIKE='{id_like}'")

            # --- LÓGICA DE DETECCIÓN ---

            # 1. Familia ARCH (Manjaro, EndeavourOS, Arch)
            if "arch" in distro_id or "manjaro" in distro_id or "arch" in id_like:
                return "arch"

            # 2. Familia DEBIAN (Ubuntu, Mint, Pop!_OS, Kali, Debian)
            if "debian" in distro_id or "ubuntu" in distro_id or "mint" in distro_id or "debian" in id_like:
                return "debian"

            # 3. Familia REDHAT (Fedora, RHEL, CentOS, AlmaLinux)
            if "fedora" in distro_id or "rhel" in distro_id or "centos" in distro_id or "fedora" in id_like:
                return "redhat"

            # 4. Familia SUSE (OpenSUSE Leap/Tumbleweed, SLES)
            if "suse" in distro_id or "sles" in distro_id or "opensuse" in id_like:
                return "suse"

        except FileNotFoundError:
            print(f"Error: No se encontró {os_release_path}")
        except Exception as e:
            print(f"Error leyendo distro: {e}")

        return "unknown"

    def install_firewall(self, firewall_name: str) -> bool:
        """
        Instala y habilita combinando comandos en una sola shell root.
        """
        distro = self.get_distro_type()
        install_part = ""

        if distro == "arch":
            install_part = f"pacman -S {firewall_name} --noconfirm"
        elif distro == "debian":
            install_part = f"apt install {firewall_name} -y"
        elif distro == "redhat":
            install_part = f"dnf install {firewall_name} -y"
        elif distro == "suse":
            install_part = f"zypper install --non-interactive {firewall_name}"
        else:
            return False

        # CONSTRUIMOS UN SÚPER COMANDO
        # 1. Instalar && 2. Habilitar y arrancar
        full_command = f"{install_part} && systemctl enable --now {firewall_name}"

        try:
            print(f"Ejecutando bloque de instalación: {full_command}")
            # Usamos 'sh -c' para ejecutar la cadena completa bajo un solo pkexec
            subprocess.run(["pkexec", "sh", "-c", full_command], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error en instalación: {e}")
            return False

class FirewallDetector:
    """Detecta el firewall activo en el sistema."""

    def _is_command_available(self, cmd):
        return shutil.which(cmd) is not None

    def _is_service_active(self, service_name):
        try:
            result = subprocess.run(
                ["systemctl", "is-active", "--quiet", service_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def detect(self) -> FirewallStatus:
        status = FirewallStatus()

        # 1. Firewalld
        if self._is_command_available("firewall-cmd"):
            if self._is_service_active("firewalld"):
                status.type = FirewallType.FIREWALLD
                status.active = True
                status.details = "Firewalld está gestionando este sistema."
                return status
            status.type = FirewallType.FIREWALLD
            status.active = False
            status.details = "Firewalld instalado pero detenido."

        # 2. UFW
        elif self._is_command_available("ufw"):
            if self._is_service_active("ufw"):
                status.type = FirewallType.UFW
                status.active = True
                status.details = "UFW está activo."
                return status
            status.type = FirewallType.UFW

        # 3. Nftables
        elif self._is_command_available("nft") and self._is_service_active("nftables"):
            status.type = FirewallType.NFTABLES
            status.active = True
            status.details = "Nftables (low-level) está activo."
            return status

        # 4. Iptables (Fallback)
        elif self._is_command_available("iptables"):
            if status.type == FirewallType.NONE:
                status.type = FirewallType.IPTABLES
                status.details = "Iptables detectado (legacy)."

        if status.type == FirewallType.NONE:
            status.details = "No se detectó ningún cortafuegos conocido."

        return status

    def set_firewall_state(self, service_name: str, enable: bool) -> bool:
        """
        Activa o desactiva usando 'systemctl enable/disable --now'.
        Esto realiza la persistencia y el cambio de estado en UN SOLO COMANDO.
        """
        action = "enable" if enable else "disable"

        try:
            # El flag --now hace el start/stop inmediato además del enable/disable
            # Al ser un solo comando, solo pide contraseña una vez.
            cmd = ["pkexec", "systemctl", action, "--now", service_name]

            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_active_service(self):
        """Retorna el nombre del servicio activo (firewalld/ufw) o None."""
        status = self.detect()
        if status.active and status.type in [FirewallType.FIREWALLD, FirewallType.UFW]:
            return "firewalld" if status.type == FirewallType.FIREWALLD else "ufw"
        return None

    def get_active_rules(self) -> list:
        service = self.get_active_service()
        rules_list = []

        if not service:
            return rules_list

        # --- BLOQUE FIREWALLD (Ya lo teníamos) ---
        if service == "firewalld":
            try:
                cmd = ["firewall-cmd", "--list-all"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                output = result.stdout.splitlines()
                # ... (Aquí va el código de parseo de firewalld que ya tenías) ...
                # ... Copia y pega el bloque 'for line in output' anterior aquí ...

                # Resumido para no repetir todo el código anterior:
                for line in output:
                    line = line.strip()
                    if line.startswith("services:"):
                        services = line.split(":")[1].strip().split()
                        for svc in services:
                            port_num = "?"
                            try:
                                port_num = str(socket.getservbyname(svc))
                            except:
                                port_num = svc
                            rules_list.append({'port': port_num, 'protocol': 'tcp', 'action': 'ALLOW', 'service_name': svc, 'zone': 'active'})
                    elif line.startswith("ports:"):
                        ports_raw = line.split(":")[1].strip().split()
                        for p in ports_raw:
                            if "/" in p:
                                port, proto = p.split("/")
                                rules_list.append({'port': port, 'protocol': proto, 'action': 'ALLOW', 'service_name': '', 'zone': 'active'})
            except subprocess.CalledProcessError:
                pass

        # --- BLOQUE UFW (NUEVO) ---
        elif service == "ufw":
            try:
                # Necesitamos sudo para ver las reglas en UFW
                cmd = ["pkexec", "ufw", "status"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                output = result.stdout.splitlines()

                # Salida típica de UFW:
                # To                         Action      From
                # --                         ------      ----
                # 22/tcp                     ALLOW       Anywhere

                start_parsing = False
                for line in output:
                    if line.startswith("--"):
                        start_parsing = True
                        continue

                    if start_parsing and line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            # Parte 0: Puerto/Proto (ej: 80/tcp)
                            raw_port = parts[0]
                            action = parts[1] # ALLOW / DENY

                            if "/" in raw_port:
                                port, proto = raw_port.split("/")
                            else:
                                port = raw_port
                                proto = "any" # UFW a veces no especifica si aplica a ambos

                            # Solo mostramos reglas IPv4 para no duplicar en la tabla (UFW muestra (v6))
                            if "(v6)" not in line:
                                rules_list.append({
                                    'port': port,
                                    'protocol': proto,
                                    'action': action,
                                    'service_name': '', # UFW no suele dar el nombre del servicio aquí
                                    'zone': 'ufw-user'
                                })
            except subprocess.CalledProcessError:
                pass

        return rules_list

    def manage_port(self, action: str, port: str, protocol: str) -> bool:
        service = self.get_active_service()
        if not service: return False

        # Obtenemos la zona activa real
        current_zone = self.get_default_zone()

        # --- LÓGICA FIREWALLD ---
        if service == "firewalld":
            cmd_perm = [
                "pkexec", "firewall-cmd", "--permanent",
                f"--zone={current_zone}", # <--- CAMBIO AQUÍ (antes era "public")
                f"--{action}-port={port}/{protocol}"
            ]
            cmd_reload = ["pkexec", "firewall-cmd", "--reload"]

            try:
                subprocess.run(cmd_perm, check=True)
                subprocess.run(cmd_reload, check=True)
                return True
            except subprocess.CalledProcessError:
                return False

        # --- LÓGICA UFW (NUEVO) ---
        elif service == "ufw":
            # UFW es más simple: "ufw allow 80/tcp" o "ufw delete allow 80/tcp"
            ufw_action = "allow"

            cmd = ["pkexec", "ufw"]

            if action == "remove":
                cmd.append("delete")
                cmd.append("allow") # Asumimos que borramos una regla de permitir
            else:
                cmd.append("allow")

            cmd.append(f"{port}/{protocol}")

            try:
                print(f"Ejecutando UFW: {cmd}")
                subprocess.run(cmd, check=True)
                return True
            except subprocess.CalledProcessError:
                return False

        return False

    def set_default_zone(self, zone_name: str) -> bool:
        """Cambia la zona por defecto (public, home, etc.)"""
        try:
            # 1. Cambiar la zona por defecto
            cmd = ["pkexec", "firewall-cmd", "--set-default-zone=" + zone_name]
            print(f"Cambiando zona a: {zone_name}")
            subprocess.run(cmd, check=True)

            # 2. Recargar para asegurar que se aplica a interfaces activas
            subprocess.run(["pkexec", "firewall-cmd", "--reload"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error cambiando zona: {e}")
            return False

    def get_default_zone(self) -> str:
        """Obtiene la zona por defecto activa en el sistema"""
        # Si no es firewalld, devolvemos 'public' por seguridad
        if self.get_active_service() != "firewalld":
            return "public"

        try:
            cmd = ["firewall-cmd", "--get-default-zone"]
            # Ejecutamos sin pkexec porque leer configuración es gratis (no requiere root)
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "public" # Fallback seguro

    def get_active_outbound_rules(self) -> list:
        """
        Lee reglas de salida.
        Soporta Firewalld (Direct Rules) y UFW (Status OUT).
        """
        rules_list = []
        service = self.get_active_service()

        if not service:
            return rules_list

        # --- LÓGICA FIREWALLD (Direct Rules) ---
        if service == "firewalld":
            try:
                cmd = ["firewall-cmd", "--direct", "--get-all-rules"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                output = result.stdout.splitlines()

                for line in output:
                    parts = line.split()
                    if len(parts) >= 6 and parts[0] == "ipv4" and parts[2] == "OUTPUT":
                        protocol = "tcp"
                        port = "?"
                        action = "ALLOW"

                        if "-p" in parts:
                            idx = parts.index("-p")
                            if idx + 1 < len(parts): protocol = parts[idx + 1]

                        if "--dport" in parts:
                            idx = parts.index("--dport")
                            if idx + 1 < len(parts): port = parts[idx + 1]

                        if "-j" in parts:
                            idx = parts.index("-j")
                            if idx + 1 < len(parts): action = parts[idx + 1]

                        rules_list.append({
                            'port': port,
                            'protocol': protocol,
                            'action': action, # ACCEPT/DROP
                            'source': 'Direct Rule'
                        })
            except:
                pass

        # --- LÓGICA UFW (Status OUT) ---
        elif service == "ufw":
            try:
                cmd = ["pkexec", "ufw", "status"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                output = result.stdout.splitlines()

                # Ejemplo salida UFW:
                # 80/tcp                   ALLOW OUT   Anywhere
                # 22                       DENY OUT    Anywhere

                start_parsing = False
                for line in output:
                    if line.startswith("--"):
                        start_parsing = True
                        continue

                    if start_parsing and line.strip():
                        # Buscamos si es una regla de salida
                        if "OUT" in line:
                            parts = line.split()
                            # UFW Output: [Puerto, Action+Direction, Dest]
                            # A veces "ALLOW OUT" son dos elementos, a veces uno si el parseo es raro

                            raw_port = parts[0]
                            # La acción suele ser la segunda columna (ALLOW/DENY/REJECT)
                            # Pero UFW pone "ALLOW OUT". Vamos a simplificar:
                            action = "ALLOW"
                            if "DENY" in line or "REJECT" in line:
                                action = "DROP"

                            if "/" in raw_port:
                                port, proto = raw_port.split("/")
                            else:
                                port = raw_port
                                proto = "any"

                            # Evitar duplicados IPv6
                            if "(v6)" not in line:
                                rules_list.append({
                                    'port': port,
                                    'protocol': proto,
                                    'action': action,
                                    'source': 'UFW Rule'
                                })
            except:
                pass

        return rules_list

    def manage_outbound_port(self, action: str, port: str, protocol: str, target: str = "DROP") -> bool:
        """
        Añade o quita regla de salida.
        target: 'DROP' (Bloquear) o 'ACCEPT'/'ALLOW' (Permitir)
        """
        service = self.get_active_service()
        if not service: return False

        # --- LÓGICA FIREWALLD ---
        if service == "firewalld":
            op_flag = "--add-rule" if action == "add" else "--remove-rule"
            args = ["ipv4", "filter", "OUTPUT", "0", "-p", protocol, "--dport", port, "-j", target]

            cmd_perm = ["pkexec", "firewall-cmd", "--permanent", "--direct", op_flag] + args
            cmd_reload = ["pkexec", "firewall-cmd", "--reload"]

            try:
                subprocess.run(cmd_perm, check=True)
                subprocess.run(cmd_reload, check=True)
                return True
            except subprocess.CalledProcessError:
                return False

        # --- LÓGICA UFW ---
        elif service == "ufw":
            # Sintaxis: ufw [delete] [allow/deny] out [port]/[proto]

            # 1. Mapear target de SentinelX (DROP/ACCEPT) a UFW (deny/allow)
            ufw_target = "deny" if target in ["DROP", "REJECT"] else "allow"

            cmd = ["pkexec", "ufw"]

            if action == "remove":
                cmd.append("delete")
                # Al borrar, tenemos que especificar qué regla exacta borrar
                cmd.append(ufw_target)
            else:
                cmd.append(ufw_target)

            # Añadir dirección y puerto
            cmd.append("out")
            cmd.append(f"{port}/{protocol}")

            try:
                print(f"Ejecutando UFW Outbound: {cmd}")
                subprocess.run(cmd, check=True)
                return True
            except subprocess.CalledProcessError:
                return False

        return False

    def get_all_available_services(self) -> list:
        """Devuelve la lista de servicios/apps conocidos."""
        service = self.get_active_service()
        apps = []

        # --- FIREWALLD ---
        if service == "firewalld":
            try:
                cmd = ["firewall-cmd", "--get-services"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                return sorted(result.stdout.strip().split())
            except:
                return []

        # --- UFW (NUEVO) ---
        elif service == "ufw":
            try:
                # 'ufw app list' devuelve:
                # Available applications:
                #   Apache
                #   OpenSSH
                cmd = ["pkexec", "ufw", "app", "list"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout.splitlines()

                for line in output:
                    # Saltamos cabeceras y líneas vacías
                    if "Available applications" in line or not line.strip():
                        continue
                    # Limpiamos espacios (ej: "  OpenSSH")
                    apps.append(line.strip())
                return sorted(apps)
            except:
                return []

        return []

    def get_active_services(self) -> list:
        """Devuelve aplicaciones PERMITIDAS (Allow)."""
        service = self.get_active_service()
        allowed_apps = []

        # --- FIREWALLD ---
        if service == "firewalld":
            try:
                cmd = ["firewall-cmd", "--list-services"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                return sorted(result.stdout.strip().split())
            except:
                return []

        # --- UFW (NUEVO) ---
        elif service == "ufw":
            try:
                # En UFW, las apps salen en 'ufw status' igual que los puertos.
                # Diferencia: Las apps no suelen tener '/' (ej: "OpenSSH" vs "22/tcp")
                cmd = ["pkexec", "ufw", "status"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout.splitlines()

                start_parsing = False
                for line in output:
                    if line.startswith("--"):
                        start_parsing = True
                        continue

                    if start_parsing and line.strip():
                        # Ejemplo: "OpenSSH    ALLOW    Anywhere"
                        if "ALLOW" in line:
                            parts = line.split()
                            target = parts[0]
                            # Si NO tiene '/' (no es puerto) y no es IP, asumimos que es App
                            if "/" not in target and not target[0].isdigit():
                                if target not in allowed_apps:
                                    allowed_apps.append(target)
                return sorted(allowed_apps)
            except:
                return []

        return []

    def get_blocked_services(self) -> list:
        """Devuelve aplicaciones BLOQUEADAS (Deny/Reject)."""
        service = self.get_active_service()
        blocked_apps = []

        # --- FIREWALLD ---
        if service == "firewalld":
            try:
                cmd = ["firewall-cmd", "--list-rich-rules"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                lines = result.stdout.splitlines()
                for line in lines:
                    if 'service name="' in line and ('drop' in line or 'reject' in line):
                        start = line.find('name="') + 6
                        end = line.find('"', start)
                        blocked_apps.append(line[start:end])
                return sorted(blocked_apps)
            except:
                return []

        # --- UFW (NUEVO) ---
        elif service == "ufw":
            try:
                # Misma lógica que active, pero buscando DENY o REJECT
                cmd = ["pkexec", "ufw", "status"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout.splitlines()

                start_parsing = False
                for line in output:
                    if line.startswith("--"):
                        start_parsing = True
                        continue

                    if start_parsing and line.strip():
                        # Ejemplo: "Apache Full    DENY    Anywhere"
                        if "DENY" in line or "REJECT" in line:
                            parts = line.split()
                            target = parts[0]
                            if "/" not in target and not target[0].isdigit():
                                if target not in blocked_apps:
                                    blocked_apps.append(target)
                return sorted(blocked_apps)
            except:
                return []

        return []

    def manage_service(self, action: str, service_name: str, mode: str = "allow") -> bool:
        service = self.get_active_service()
        if not service: return False

        # Obtenemos la zona activa real (ej: "home" o "public")
        current_zone = self.get_default_zone()

        # --- FIREWALLD ---
        if service == "firewalld":
            cmd_perm = []
            if mode == "allow":
                flag = f"--{action}-service={service_name}"
                # CAMBIO AQUÍ: Usamos current_zone en vez de "public"
                cmd_perm = ["pkexec", "firewall-cmd", "--permanent", f"--zone={current_zone}", flag]

            elif mode == "block":
                rule_str = f'rule service name="{service_name}" drop'
                op = "--add-rich-rule" if action == "add" else "--remove-rich-rule"
                # CAMBIO AQUÍ TAMBIÉN
                cmd_perm = ["pkexec", "firewall-cmd", "--permanent", f"--zone={current_zone}", op, rule_str]

            try:
                subprocess.run(cmd_perm, check=True)
                subprocess.run(["pkexec", "firewall-cmd", "--reload"], check=True)
                return True
            except:
                return False

        # --- UFW (NUEVO) ---
        elif service == "ufw":
            # UFW es muy semántico: ufw allow "OpenSSH" / ufw deny "Apache"

            # 1. Determinar verbo (allow/deny)
            verb = "allow" if mode == "allow" else "deny"

            cmd = ["pkexec", "ufw"]

            if action == "remove":
                # Para borrar: ufw delete allow "OpenSSH"
                cmd.append("delete")
                cmd.append(verb)
            else:
                # Para añadir: ufw allow "OpenSSH"
                cmd.append(verb)

            cmd.append(service_name)

            try:
                print(f"Ejecutando UFW App: {cmd}")
                subprocess.run(cmd, check=True)
                return True
            except:
                return False

        return False
