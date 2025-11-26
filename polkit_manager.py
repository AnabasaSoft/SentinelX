import os
import subprocess
import sys

# Rutas
POLKIT_RULE_PATH = "/etc/polkit-1/rules.d/49-sentinelx.rules"
HELPER_PATH = "/usr/local/bin/sentinelx-helper"

# --- VERSIÓN 7 (Corrección ClamAV Moderno) ---
CURRENT_RULE_VERSION = 7

# 1. CONTENIDO DE LA REGLA (Solo permite nuestro helper y herramientas seguras)
POLKIT_RULE_CONTENT = """/* Regla instalada por SentinelX (v7 - ClamAV Fix) */
polkit.addRule(function(action, subject) {
    var is_admin = subject.isInGroup("wheel") || subject.isInGroup("sudo");

    if (is_admin) {
        // D-Bus Firewalld
        if (action.id.indexOf("org.fedoraproject.FirewallD1") == 0) {
            return polkit.Result.YES;
        }

        // Ejecutables específicos
        if (action.id == "org.freedesktop.policykit.exec") {
            var program = action.lookup("program");

            if (program == "/usr/bin/firewall-cmd" ||
                program == "/usr/sbin/firewall-cmd" ||
                program == "/usr/bin/ufw" ||
                program == "/usr/sbin/ufw" ||
                program == "/usr/bin/freshclam" ||
                // HELPER SEGURO
                program == "/usr/local/bin/sentinelx-helper" ||
                // Systemctl
                program == "/usr/bin/systemctl" ||
                program == "/bin/systemctl") {
                return polkit.Result.YES;
            }
        }
    }
});
"""

# 2. CONTENIDO DEL SCRIPT HELPER (Bash)
# CORREGIDO: Usamos OnAccessExcludeUname en lugar de Uid para compatibilidad con ClamAV > 0.105
HELPER_CONTENT = r"""#!/bin/bash
# SentinelX Helper Script v7

COMMAND="$1"
CONF_PATH="$2"
WATCH_PATH="$3"

case "$COMMAND" in
    "enable-on-access")
        if [ -z "$CONF_PATH" ] || [ -z "$WATCH_PATH" ]; then exit 1; fi

        # Limpiar config vieja (Esto borrará la línea errónea automáticamente)
        sed -i '/^OnAccess/d' "$CONF_PATH"

        # Añadir config nueva (Sintaxis moderna)
        echo "OnAccessIncludePath $WATCH_PATH" >> "$CONF_PATH"
        echo "OnAccessPrevention yes" >> "$CONF_PATH"
        echo "OnAccessExcludeUname root" >> "$CONF_PATH"
        echo "OnAccessExtraScanning yes" >> "$CONF_PATH"
        ;;

    "disable-on-access")
        if [ -z "$CONF_PATH" ]; then exit 1; fi
        sed -i '/^OnAccess/d' "$CONF_PATH"
        ;;

    *)
        echo "Comando desconocido"
        exit 1
        ;;
esac
"""

class PolkitManager:
    def get_current_version(self):
        return CURRENT_RULE_VERSION

    def install_rule(self):
        print(f"Instalando sistema de seguridad v{CURRENT_RULE_VERSION}...")

        setup_cmds = [
            f"cat << 'EOF' > {HELPER_PATH}\n{HELPER_CONTENT}\nEOF",
            f"chmod +x {HELPER_PATH}",
            f"cat << 'EOF' > {POLKIT_RULE_PATH}\n{POLKIT_RULE_CONTENT}\nEOF",
            "systemctl restart polkit"
        ]

        full_cmd = "\n".join(setup_cmds)

        # Última vez que pedimos pass, para actualizar el helper
        cmd = ["pkexec", "sh", "-c", full_cmd]

        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except Exception as e:
            print(f"Error setup: {e}")
            return False
