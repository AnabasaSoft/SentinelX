# locales.py

TRANSLATIONS = {
    # Spanish
    "es": {
        "app_title": "SentinelX",
        "tab_firewall": "🔥 Firewall",
        "tab_antivirus": "🦠 Antivirus",
        "tab_config": "⚙️ Configuración",

        # Firewall Tab
        "fw_title": "Protección de Red",
        "fw_status_active": "Firewall activado",
        "fw_status_inactive": "Firewall desactivado",
        "fw_backend": "Motor activo: {}",
        "fw_warning": "⚠️ El servicio {} está detenido",
        "fw_managed_by": "Gestionado por {}",
        "fw_missing_title": "⚠️ Faltan componentes",
        "fw_missing_desc": "No se detectó Firewalld ni UFW.",
        "fw_error_install": "Error: Instala firewalld primero.",

        # Config Tab
        "cfg_title": "Configuración Global",
        "cfg_lang_label": "Idioma de la interfaz:",
        "cfg_theme_label": "Tema de la interfaz:",
        "cfg_restart_note": "Nota: Los cambios de interfaz requieren reiniciar la aplicación.",

        # --- Diálogo de Instalación ---
        "inst_title": "Instalación de Componentes",
        "inst_header": "⚠️ Firewall no detectado",
        "inst_desc": "Tu sistema ({}) no tiene un gestor de firewall activo.\nSentinelX puede instalar y configurar uno por ti.",
        "inst_select_label": "Selecciona el motor a instalar:",
        "inst_btn_install": "Instalar ahora",
        "inst_btn_cancel": "Cancelar",

        # Etiquetas para el selector
        "inst_rec_tag": " (Recomendado)",
        "inst_simple_tag": " (Simple)",
        "inst_adv_tag": " (Avanzado)",
        "inst_std_tag": " (Estándar)",

        # Estados de progreso
        "inst_status_working": "Instalando...",
        "inst_status_wait": "Esto puede tardar unos segundos...",

        # Mensajes finales
        "inst_success_title": "Éxito",
        "inst_success_msg": "{} se instaló correctamente.",
        "inst_error_title": "Error",
        "inst_error_msg": "La instalación falló o fue cancelada.",

        # --- SUB-PESTAÑAS FIREWALL ---
        "fw_tab_net_type": "Tipo de Red",
        "fw_tab_rules_in": "Reglas de Entrada",
        "fw_tab_rules_out": "Reglas de Salida",
        "fw_tab_apps_allow": "Apps Permitidas",
        "fw_tab_apps_block": "Apps Bloqueadas",

        # --- PESTAÑA TIPO DE RED (ZONAS) ---
        "zone_section_title": "Define tu entorno actual",
        "zone_public_title": "🕵️ Red Desconocida (Pública)",
        "zone_public_desc": "Usa esto en aeropuertos, cafeterías o hoteles.\nBloquea conexiones entrantes y oculta tu PC.",
        "zone_home_title": "🏠 Red Conocida (Casa/Trabajo)",
        "zone_home_desc": "Usa esto en tu red privada de confianza.\nPermite compartir impresoras, archivos y dispositivos.",
        "zone_btn_apply": "Aplicar perfil de red",
        "zone_apply_success": "Perfil de red actualizado a: {}",

        # Opciones de Tema
        "theme_dark": "Oscuro (Dark)",
        "theme_light": "Claro (Light)",

        # --- PESTAÑA REGLAS DE ENTRADA ---
        "inbound_table_title": "Reglas de Filtrado de Entrada (Puertos)",
        "inbound_header_port": "Puerto/Servicio",
        "inbound_header_proto": "Protocolo",
        "inbound_header_action": "Acción",
        "inbound_header_source": "Nombre/Servicio",
        "add_rule_desc_label": "Nombre (opcional):",
        "inbound_no_rules": "No hay reglas de entrada personalizadas activas.",
        "inbound_error_read": "Error al leer reglas. Asegúrate de que el motor de firewall esté ACTIVO.",

        # --- TABLA REGLAS SALIDA ---
        "outbound_table_title": "Reglas de Filtrado de Salida (Egress)",
        "outbound_header_port": "Puerto/Destino",
        "outbound_header_proto": "Protocolo",
        "outbound_header_action": "Acción",
        "outbound_header_source": "Nombre/Descripción",
        "outbound_no_rules": "No hay reglas de salida personalizadas (Política por defecto: Permitir).",

        # --- BOTONES REGLAS ---
        "btn_add_rule": "Añadir Regla",
        "btn_del_rule": "Eliminar Seleccionada",

        # --- DIÁLOGO AÑADIR REGLA ---
        "add_rule_title": "Abrir Nuevo Puerto",
        "add_rule_port_label": "Número de Puerto (ej: 8080):",
        "add_rule_proto_label": "Protocolo:",
        "add_rule_btn_save": "Guardar Regla",

        # --- MENSAJES ACCIONES ---
        "msg_confirm_del_title": "Confirmar eliminación",
        "msg_confirm_del_text": "¿Seguro que quieres cerrar el puerto {}/{}?",
        "msg_error_select": "Por favor, selecciona una fila primero.",
        "msg_success_add": "Regla añadida correctamente.",
        "msg_success_del": "Regla eliminada correctamente.",
        "msg_error_cmd": "Error al aplicar los cambios.",

        # ... otros textos ...
        "btn_refresh_tooltip": "Recargar lista de reglas desde el sistema",
        "btn_refresh_rules": "Refrescar reglas",
        "msg_ufw_no_zones": "UFW no soporta perfiles de zona.",

        # --- DETECCIÓN DE REDES ---
        "net_detect_title": "Nueva Red Detectada",
        "net_detect_msg": "Te has conectado a la red: \n👉 <b>{}</b>\n\n¿Cómo quieres clasificarla?",
        "net_btn_public": "Pública (Cafetería/Aeropuerto)",
        "net_btn_home": "Privada (Casa/Trabajo)",
        "net_auto_switch_msg": "Red conocida '{}' detectada. Cambiando a zona: {}.",

        # --- APPS TABS ---
        "apps_allow_title": "Aplicaciones/Servicios Permitidos",
        "apps_block_title": "Aplicaciones/Servicios Bloqueados (Rich Rules)",
        "apps_header_name": "Nombre App/Servicio",
        "apps_header_desc": "Descripción",
        "apps_btn_add": "Añadir App",
        "apps_btn_remove": "Quitar App",

        # Diálogo Añadir App
        "add_app_title": "Seleccionar Aplicación",
        "add_app_label": "Buscar servicio (ej: steam, http, ssh):",
        "add_app_btn_save": "Aplicar Cambios",
        "apps_no_blocked": "No hay aplicaciones bloqueadas explícitamente.",
        "apps_no_allowed": "No hay servicios extra permitidos (solo los básicos).",

        # --- POLKIT SETUP ---
        "polkit_title": "Configuración Inicial",
        "polkit_msg": "Para ofrecer una experiencia fluida, SentinelX necesita instalar una regla de sistema.\n\nEsto evitará que se te pida la contraseña cada vez que la aplicación lea el estado del firewall.\n\n¿Deseas instalar esta regla ahora? (Se pedirá contraseña una única vez)",
        "polkit_btn_yes": "Sí, instalar (Recomendado)",
        "polkit_btn_no": "No, prefiero introducir contraseñas",
        "polkit_success": "Regla instalada correctamente. Reiniciando servicios...",
        "polkit_error": "No se pudo instalar la regla.",
        "polkit_title": "Actualización de Componentes",
        "polkit_msg": "SentinelX ha actualizado sus protocolos de seguridad (v{}).\n\nEs necesario actualizar la regla de sistema para soportar las nuevas funciones (Antivirus).\n\n¿Actualizar ahora?",
        "polkit_success": "Sistema actualizado correctamente.",

        # --- ANTIVIRUS TAB ---
        "av_title": "Escáner de Malware (ClamAV)",
        "av_status_installed": "Motor ClamAV detectado",
        "av_status_missing": "ClamAV no está instalado",
        "av_btn_install": "Instalar ClamAV",
        "av_btn_scan_home": "Escanear Carpeta Personal",
        "av_btn_scan_system": "Escanear Sistema Completo",
        "av_btn_update_db": "Actualizar Base de Firmas",
        "av_lbl_last_scan": "Último escaneo: {}",
        "av_lbl_db_version": "Versión de base de datos: {}",
        "av_scan_running": "Escaneando... Por favor espere.",
        "av_scan_completed": "Escaneo completado.",
        "av_scan_infected": "⚠️ AMENAZAS DETECTADAS: {}",
        "av_scan_clean": "✅ No se encontraron amenazas.",
        "av_error_update": "Error al actualizar firmas (necesita root).",
        "av_install_msg": "Se instalará el motor ClamAV en tu sistema.",
        "av_btn_stop": "Detener Escaneo",
        "av_scan_stopped": "🛑 Escaneo detenido por el usuario.",

        # --- MENSAJES INSTALACIÓN ANTIVIRUS ---
        "av_install_confirm_title": "Instalar",
        "av_install_log_start": "🛠️ Iniciando instalación de ClamAV...",
        "av_install_success_title": "Éxito",
        "av_install_success_msg": "ClamAV se instaló correctamente.",
        "av_install_fail_log": "❌ La instalación falló.",
        "av_install_error_title": "Error",
        "av_install_error_msg": "No se pudo completar la instalación. Revisa el log.",
        "av_scan_info_title": "Info",
        "av_scan_info_msg": "El escaneo completo puede tardar mucho tiempo.",
        "av_scan_cancel_log": "❌ Escaneo cancelado o fallido.",
        "av_scan_clean_title": "Limpio",
        "av_scan_threat_title": "AMENAZA",
        "av_update_success_log": "✅ Base de datos actualizada.",
        "av_update_fail_log": "❌ Error al actualizar.",
        "av_update_error_title": "Error",

        # --- LOGS DE WORKERS (ANTIVIRUS MANAGER) ---
        "log_scan_start": "🚀 Iniciando escaneo en: {}",
        "log_critical_error": "❌ Error crítico: {}",
        "log_update_start": "🔄 Actualizando base de datos de virus (freshclam)...",
        "log_pkg_detect": "📦 Detectando gestor de paquetes...",
        "log_distro_error": "❌ Error: Distribución no soportada o no detectada.",
        "log_executing": "🚀 Ejecutando: {}",
        "log_pass_prompt": "⚠️ Por favor, introduce tu contraseña si se solicita...",
        "log_install_ok": "✅ Instalación finalizada con éxito.",
        "log_process_error": "❌ El proceso terminó con código de error: {}",
        "log_generic_error": "Error: {}",
    },

    # English
    "en": {
        "app_title": "SentinelX",
        "tab_firewall": "🔥 Firewall",
        "tab_antivirus": "🦠 Antivirus",
        "tab_config": "⚙️ Settings",
        "fw_title": "Network Protection",
        "fw_status_active": "Firewall Active",
        "fw_status_inactive": "Firewall Inactive",
        "fw_backend": "Active engine: {}",
        "fw_warning": "⚠️ Service {} is stopped",
        "fw_managed_by": "Managed by {}",
        "fw_missing_title": "⚠️ Missing components",
        "fw_missing_desc": "Firewalld or UFW not detected.",
        "fw_error_install": "Error: Please install firewalld first.",
        "cfg_title": "Global Settings",
        "cfg_lang_label": "Interface Language:",
        "cfg_theme_label": "Interface Theme:",
        "cfg_restart_note": "Note: Interface changes require app restart.",

        # --- NEW: Install Dialog ---
        "inst_title": "Component Installation",
        "inst_header": "⚠️ Firewall not detected",
        "inst_desc": "Your system ({}) has no active firewall manager.\nSentinelX can install and configure one for you.",
        "inst_select_label": "Select engine to install:",
        "inst_btn_install": "Install Now",
        "inst_btn_cancel": "Cancel",

        "inst_rec_tag": " (Recommended)",
        "inst_simple_tag": " (Simple)",
        "inst_adv_tag": " (Advanced)",
        "inst_std_tag": " (Standard)",

        "inst_status_working": "Installing...",
        "inst_status_wait": "This might take a few seconds...",

        "inst_success_title": "Success",
        "inst_success_msg": "{} installed successfully.",
        "inst_error_title": "Error",
        "inst_error_msg": "Installation failed or was cancelled.",

        # --- FIREWALL SUB-TABS ---
        "fw_tab_net_type": "Network Type",
        "fw_tab_rules_in": "Inbound Rules",
        "fw_tab_rules_out": "Outbound Rules",
        "fw_tab_apps_allow": "Allowed Apps",
        "fw_tab_apps_block": "Blocked Apps",

        # --- NETWORK TYPE TAB (ZONES) ---
        "zone_section_title": "Define your current environment",
        "zone_public_title": "🕵️ Unknown Network (Public)",
        "zone_public_desc": "Use this in airports, cafes, or hotels.\nBlocks incoming connections and hides your PC.",
        "zone_home_title": "🏠 Known Network (Home/Work)",
        "zone_home_desc": "Use this on your trusted private network.\nAllows printer sharing, files, and devices.",
        "zone_btn_apply": "Apply Network Profile",
        "zone_apply_success": "Network profile updated to: {}",

        # Theme Options
        "theme_dark": "Dark",
        "theme_light": "Light",

        # --- INBOUND RULES TAB ---
        "inbound_table_title": "Inbound Filtering Rules (Ports)",
        "inbound_header_port": "Port/Service",
        "inbound_header_proto": "Protocol",
        "inbound_header_action": "Action",
        "inbound_header_source": "Name/Service",
        "add_rule_desc_label": "Name (optional):",
        "inbound_no_rules": "There are no active custom inbound rules.",
        "inbound_error_read": "Error reading rules. Make sure the firewall engine is ACTIVE.",

        # --- OUTBOUND RULES TABLE ---
        "outbound_table_title": "Outbound Filtering Rules (Egress)",
        "outbound_header_port": "Port/Destination",
        "outbound_header_proto": "Protocol",
        "outbound_header_action": "Action",
        "outbound_header_source": "Name/Description",
        "outbound_no_rules": "No custom outbound rules active (Default Policy: Allow).",

        # --- RULES BUTTONS ---
        "btn_add_rule": "Add Rule",
        "btn_del_rule": "Delete Selected",

        # --- ADD RULE DIALOG ---
        "add_rule_title": "Open New Port",
        "add_rule_port_label": "Port Number (e.g., 8080):",
        "add_rule_proto_label": "Protocol:",
        "add_rule_btn_save": "Save Rule",

        # --- ACTION MESSAGES ---
        "msg_confirm_del_title": "Confirm Deletion",
        "msg_confirm_del_text": "Are you sure you want to close port {}/{}?",
        "msg_error_select": "Please select a row first.",
        "msg_success_add": "Rule added successfully.",
        "msg_success_del": "Rule deleted successfully.",
        "msg_error_cmd": "Error applying changes.",

        # ... other texts ...
        "btn_refresh_tooltip": "Reload rules from system",
        "btn_refresh_rules": "Refresh rules",
        "msg_ufw_no_zones": "UFW does not support zone profiles.",

        # --- NETWORK DETECTION ---
        "net_detect_title": "New Network Detected",
        "net_detect_msg": "You connected to network: \n👉 <b>{}</b>\n\nHow do you want to classify it?",
        "net_btn_public": "Public (Coffee Shop/Airport)",
        "net_btn_home": "Private (Home/Work)",
        "net_auto_switch_msg": "Known network '{}' detected. Switching to zone: {}.",

        # --- APPS TABS ---
        "apps_allow_title": "Allowed Apps/Services",
        "apps_block_title": "Blocked Apps/Services (Rich Rules)",
        "apps_header_name": "App/Service Name",
        "apps_header_desc": "Description",
        "apps_btn_add": "Add App",
        "apps_btn_remove": "Remove App",

        "add_app_title": "Select Application",
        "add_app_label": "Search service (e.g., steam, http, ssh):",
        "add_app_btn_save": "Apply Changes",
        "apps_no_blocked": "No apps explicitly blocked.",
        "apps_no_allowed": "No extra services allowed (only basics).",

        # --- POLKIT SETUP ---
        "polkit_title": "Initial Setup",
        "polkit_msg": "To provide a smooth experience, SentinelX needs to install a system rule.\n\nThis will prevent password prompts every time the app reads firewall status.\n\nDo you want to install this rule now? (Password required once)",
        "polkit_btn_yes": "Yes, Install (Recommended)",
        "polkit_btn_no": "No, I prefer entering passwords",
        "polkit_success": "Rule installed successfully. Restarting services...",
        "polkit_error": "Could not install the rule.",
        "polkit_title": "Component Update",
        "polkit_msg": "SentinelX has updated its security protocols (v{}).\n\nA system rule update is required to support new features (Antivirus).\n\nUpdate now?",
        "polkit_success": "System updated successfully.",

        # --- ANTIVIRUS TAB ---
        "av_title": "Malware Scanner (ClamAV)",
        "av_status_installed": "ClamAV Engine Detected",
        "av_status_missing": "ClamAV is not installed",
        "av_btn_install": "Install ClamAV",
        "av_btn_scan_home": "Scan Home Folder",
        "av_btn_scan_system": "Scan Full System",
        "av_btn_update_db": "Update Signatures DB",
        "av_lbl_last_scan": "Last scan: {}",
        "av_lbl_db_version": "Database version: {}",
        "av_scan_running": "Scanning... Please wait.",
        "av_scan_completed": "Scan completed.",
        "av_scan_infected": "⚠️ THREATS DETECTED: {}",
        "av_scan_clean": "✅ No threats found.",
        "av_error_update": "Error updating signatures (root required).",
        "av_install_msg": "ClamAV engine will be installed on your system.",
        "av_btn_stop": "Stop Scan",
        "av_scan_stopped": "🛑 Scan stopped by user.",

        # --- ANTIVIRUS INSTALL MESSAGES ---
        "av_install_confirm_title": "Install",
        "av_install_log_start": "🛠️ Starting ClamAV installation...",
        "av_install_success_title": "Success",
        "av_install_success_msg": "ClamAV installed successfully.",
        "av_install_fail_log": "❌ Installation failed.",
        "av_install_error_title": "Error",
        "av_install_error_msg": "Could not complete installation. Check the log.",
        "av_scan_info_title": "Info",
        "av_scan_info_msg": "Full system scan may take a long time.",
        "av_scan_cancel_log": "❌ Scan cancelled or failed.",
        "av_scan_clean_title": "Clean",
        "av_scan_threat_title": "THREAT",
        "av_update_success_log": "✅ Database updated.",
        "av_update_fail_log": "❌ Update failed.",
        "av_update_error_title": "Error",

        # --- WORKER LOGS (ANTIVIRUS MANAGER) ---
        "log_scan_start": "🚀 Starting scan in: {}",
        "log_critical_error": "❌ Critical error: {}",
        "log_update_start": "🔄 Updating virus database (freshclam)...",
        "log_pkg_detect": "📦 Detecting package manager...",
        "log_distro_error": "❌ Error: Unsupported or undetected distribution.",
        "log_executing": "🚀 Executing: {}",
        "log_pass_prompt": "⚠️ Please enter your password if prompted...",
        "log_install_ok": "✅ Installation finished successfully.",
        "log_process_error": "❌ Process finished with error code: {}",
        "log_generic_error": "Error: {}",
    }
}

# Variable para guardar el idioma actual (por defecto español)
current_lang = "es"

def get_text(key):
    """Devuelve el texto traducido para la clave dada."""
    # Si la clave no existe, devuelve la clave misma como fallback
    return TRANSLATIONS.get(current_lang, {}).get(key, key)
