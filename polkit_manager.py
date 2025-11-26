import os
import subprocess
import sys

# Ruta del archivo de reglas
POLKIT_RULE_PATH = "/etc/polkit-1/rules.d/49-sentinelx.rules"

# --- VERSIÓN ACTUAL DE LA REGLA ---
# Incrementa este número cada vez que modifiques el contenido de abajo
CURRENT_RULE_VERSION = 2

# Contenido (Firewall + UFW + Antivirus)
POLKIT_RULE_CONTENT = """/* Regla instalada por SentinelX (v2) */
polkit.addRule(function(action, subject) {
    var is_admin = subject.isInGroup("wheel") || subject.isInGroup("sudo");

    if (is_admin) {
        // 1. D-Bus Firewalld
        if (action.id.indexOf("org.fedoraproject.FirewallD1") == 0) {
            return polkit.Result.YES;
        }

        // 2. Ejecutables (pkexec)
        if (action.id == "org.freedesktop.policykit.exec") {
            var program = action.lookup("program");

            if (program == "/usr/bin/firewall-cmd" ||
                program == "/usr/sbin/firewall-cmd" ||
                program == "/usr/bin/ufw" ||
                program == "/usr/sbin/ufw" ||
                program == "/usr/bin/freshclam") {
                return polkit.Result.YES;
            }
        }
    }
});
"""

class PolkitManager:
    def get_current_version(self):
        return CURRENT_RULE_VERSION

    def install_rule(self):
        print(f"Instalando regla Polkit v{CURRENT_RULE_VERSION}...")

        cmd = ["pkexec", "sh", "-c", f"cat > {POLKIT_RULE_PATH}"]

        try:
            subprocess.run(
                cmd,
                input=POLKIT_RULE_CONTENT.encode('utf-8'),
                check=True
            )

            subprocess.run(["pkexec", "systemctl", "restart", "polkit"], stderr=subprocess.DEVNULL)
            return True

        except subprocess.CalledProcessError:
            return False
        except Exception:
            return False
