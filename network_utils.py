import subprocess
import shutil

class NetworkUtils:
    def get_active_connection_name(self):
        """
        Devuelve el nombre de la conexión activa (SSID wifi o nombre cableada).
        Retorna None si no hay red.
        """
        if not shutil.which("nmcli"):
            return None # No podemos detectar sin NetworkManager

        try:
            # nmcli -t -f NAME,TYPE connection show --active
            # Devuelve: "MiCasa:802-11-wireless" o "Cableada 1:802-3-ethernet"
            cmd = ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show", "--active"]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0 or not result.stdout.strip():
                return None

            # Cogemos la primera línea (la conexión principal)
            first_line = result.stdout.splitlines()[0]
            name = first_line.split(":")[0] # Solo el nombre

            return name
        except Exception as e:
            print(f"Error detectando red: {e}")
            return None
