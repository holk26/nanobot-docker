#!/bin/bash
set -e

# Cargar variables de entorno desde .env si existe
envfile="/app/.env"
[ -f "$envfile" ] && export $(grep -v '^#' "$envfile" | xargs)

# Función para pedir dato si no está definido
demand_var() {
  local var="$1"
  local prompt="$2"
  local secret="$3"
  eval val="\${$var}"
  if [ -z "$val" ]; then
    if [ "$secret" = "1" ]; then
      read -rsp "$prompt: " val && echo
    else
      read -rp "$prompt: " val
    fi
    export $var="$val"
    echo "$var=$val" >> "$envfile"
  fi
}

# Pedir API key si no está
if [ -z "$NANOBOT_PROVIDERS__OPENROUTER__APIKEY" ]; then
  demand_var NANOBOT_PROVIDERS__OPENROUTER__APIKEY "Introduce tu OpenRouter API Key (sk-or-xxx)" 1
fi

# Pedir token de Telegram si está habilitado
if [ "$NANOBOT_CHANNELS__TELEGRAM__ENABLED" = "true" ] && [ -z "$NANOBOT_CHANNELS__TELEGRAM__TOKEN" ]; then
  demand_var NANOBOT_CHANNELS__TELEGRAM__TOKEN "Introduce tu Telegram Bot Token" 1
fi

# Pedir email y password si email está habilitado
if [ "$NANOBOT_CHANNELS__EMAIL__ENABLED" = "true" ]; then
  demand_var NANOBOT_CHANNELS__EMAIL__IMAPUSERNAME "Introduce tu email para IMAP" 0
  demand_var NANOBOT_CHANNELS__EMAIL__IMAPPASSWORD "Introduce tu password de email (app password)" 1
fi

# Mostrar resumen de configuración
clear
echo "\nConfiguración cargada:"
env | grep NANOBOT_ | sort

echo "\nArrancando nanobot..."

# Lanzar bash interactivo si se solicita, si no, gateway por defecto
if [ "$1" = "bash" ] || [ "$1" = "sh" ]; then
  exec "$@"
else
  exec nanobot gateway "$@"
fi
