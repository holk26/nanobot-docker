# Manual rápido para desplegar y configurar nanobot en la nube con Dokploy

## 1. Pre-requisitos
- Tener una cuenta en Dokploy y acceso a un clúster o máquina dedicada.
- Docker y Dokploy CLI instalados en tu entorno local (o usa la web de Dokploy).
- Tus claves/API y datos de configuración listos.

## 2. Preparar el entorno
1. Clona tu repositorio o sube el código fuente a Dokploy.
2. Copia el archivo de ejemplo y edítalo:
   ```bash
   cp .env.example .env
   # Edita .env y pon tus claves y parámetros
   nano .env
   ```

## 3. Build y despliegue

### Opción A: Usando Dokploy CLI

1. Inicia sesión:
   ```bash
   dokploy login
   ```
2. Construye la imagen (opcional, Dokploy puede hacerlo automáticamente):
   ```bash
   docker build -t nanobot -f Dockerfile.sandbox .
   ```
3. Despliega usando el archivo docker-compose.cloud.yml:
   ```bash
   dokploy deploy -f docker-compose.cloud.yml
   ```

### Opción B: Usando la web de Dokploy

1. Sube tu repositorio o conecta con GitHub.
2. Selecciona el archivo `docker-compose.cloud.yml` como stack principal.
3. Sube tu archivo `.env` (no subas .env.example, solo el real).
4. Haz clic en "Deploy".

## 4. Configuración
- Edita `.env` para tus claves de API, tokens de canales, modelo, zona horaria, etc.
- Puedes escalar el número de réplicas desde el panel de Dokploy o editando `replicas` en el compose.
- Los datos y logs se almacenan en volúmenes persistentes (no se pierden al reiniciar).

## 5. Acceso y administración
- El bot estará disponible en el puerto 18790 de la IP pública o dominio asignado por Dokploy.
- Puedes acceder a la terminal del contenedor desde el panel de Dokploy para instalar paquetes o hacer debug.
- Para actualizar, sube los cambios y redepliega.

## 6. Seguridad
- Nunca subas tu archivo `.env` real a repositorios públicos.
- Usa claves/API dedicadas para producción.
- Revisa los logs y limita el acceso a los canales según tus necesidades.

---

¿Dudas? Consulta la documentación oficial de Dokploy o la de nanobot para detalles avanzados.