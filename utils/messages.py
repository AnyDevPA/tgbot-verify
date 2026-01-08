"""Plantillas de mensajes"""
from config import CHANNEL_URL, VERIFY_COST, HELP_NOTION_URL


def get_welcome_message(full_name: str, invited_by: bool = False) -> str:
    """Obtener mensaje de bienvenida"""
    msg = (
        f"🎉 ¡Bienvenido, {full_name}!\n"
        "Te has registrado con éxito y has recibido 1 punto.\n"
    )
    if invited_by:
        msg += "Gracias por unirte mediante invitación. Quien te invitó ha recibido 2 puntos.\n"

    msg += (
        "\nEste bot completa automáticamente la verificación de SheerID.\n"
        "Inicio rápido:\n"
        "/about - Conocer funciones del bot\n"
        "/balance - Ver saldo de puntos\n"
        "/help - Ver lista completa de comandos\n\n"
        "Conseguir más puntos:\n"
        "/qd - Check-in diario\n"
        "/invite - Invitar amigos\n"
        f"Únete al canal: {CHANNEL_URL}"
    )
    return msg


def get_about_message() -> str:
    """Obtener mensaje 'Acerca de'"""
    return (
        "🤖 Bot de Verificación Automática SheerID\n"
        "\n"
        "Funciones:\n"
        "- Completa automáticamente la verificación de Estudiante/Profesor en SheerID\n"
        "- Soporta: Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student y Bolt.new Teacher\n"
        "\n"
        "Obtener Puntos:\n"
        "- Registro: 1 punto de regalo\n"
        "- Check-in diario: +1 punto\n"
        "- Invitar amigos: +2 puntos/persona\n"
        "- Usar Keys (según el valor de la key)\n"
        f"- Canal oficial: {CHANNEL_URL}\n"
        "\n"
        "Cómo usar:\n"
        "1. Inicia la verificación en la web del servicio y copia el enlace completo.\n"
        "2. Envía /verify, /verify2, /verify3, /verify4 o /verify5 seguido del enlace.\n"
        "3. Espera el procesamiento y mira el resultado.\n"
        "4. En Bolt.new el código se obtiene solo, si necesitas consultarlo manual usa /getV4Code <verification_id>\n"
        "\n"
        "Para más comandos envía /help"
    )


def get_help_message(is_admin: bool = False) -> str:
    """Obtener mensaje de ayuda"""
    msg = (
        "📖 Bot SheerID Auto - Ayuda\n"
        "\n"
        "Comandos de Usuario:\n"
        "/start - Iniciar (Registro)\n"
        "/about - Conocer funciones\n"
        "/balance - Ver saldo de puntos\n"
        "/qd - Check-in diario (+1 punto)\n"
        "/invite - Generar link de invitación (+2 puntos/persona)\n"
        "/use <key> - Canjear puntos con una Key\n"
        f"/verify <link> - Gemini One Pro (-{VERIFY_COST} puntos)\n"
        f"/verify2 <link> - ChatGPT Teacher K12 (-{VERIFY_COST} puntos)\n"
        f"/verify3 <link> - Spotify Student (-{VERIFY_COST} puntos)\n"
        f"/verify4 <link> - Bolt.new Teacher (-{VERIFY_COST} puntos)\n"
        f"/verify5 <link> - YouTube Student Premium (-{VERIFY_COST} puntos)\n"
        "/getV4Code <verification_id> - Ver código de Bolt.new\n"
        "/help - Ver esta ayuda\n"
        f"Solución de errores: {HELP_NOTION_URL}\n"
    )

    if is_admin:
        msg += (
            "\nComandos de Admin:\n"
            "/addbalance <UserID> <Puntos> - Añadir puntos a usuario\n"
            "/block <UserID> - Bloquear usuario\n"
            "/white <UserID> - Desbloquear usuario\n"
            "/blacklist - Ver lista negra\n"
            "/genkey <Key> <Puntos> [Veces] [Días] - Generar una Key\n"
            "/listkeys - Ver lista de Keys activas\n"
            "/broadcast <Texto> - Difusión a todos los usuarios\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int) -> str:
    """Obtener mensaje de saldo insuficiente"""
    return (
        f"¡Puntos insuficientes! Necesitas {VERIFY_COST} puntos, tienes {current_balance}.\n\n"
        "Cómo conseguir puntos:\n"
        "- Check-in diario /qd\n"
        "- Invitar amigos /invite\n"
        "- Usar una Key /use <key>"
    )


def get_verify_usage_message(command: str, service_name: str) -> str:
    """Obtener instrucciones de comando de verificación"""
    return (
        f"Uso: {command} <Enlace SheerID>\n\n"
        "Ejemplo:\n"
        f"{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n"
        "Cómo obtener el enlace:\n"
        f"1. Ve a la página de verificación de {service_name}\n"
        "2. Inicia el proceso de verificación\n"
        "3. Copia la URL completa de la barra de direcciones del navegador\n"
        f"4. Envíala usando el comando {command}"
    )
