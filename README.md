# Monitor de Recursos en Tiempo Real

Este proyecto es un sistema de monitoreo de recursos en tiempo real que utiliza una arquitectura coordinador-trabajador con Redis como intermediario de mensajes. El coordinador asigna tareas a los trabajadores, y estos procesan dichas tareas.

## Requisitos

Para ejecutar este proyecto, necesitas tener instalados los siguientes programas en tu sistema:

- Docker
- Docker Compose

## Estructura del Proyecto

El proyecto está organizado en los siguientes servicios:

- **Redis**: Actúa como intermediario de mensajes.
- **Coordinador**: API desarrollada en Flask que gestiona las tareas y los trabajadores.
- **Trabajadores**: Procesan las tareas asignadas por el coordinador.
- **Frontend**: Interfaz de usuario desarrollada con Next.js para interactuar con el sistema.
- **Monitorización**: Servicio Flask que registra y supervisa el estado de los trabajadores.

## Cómo Ejecutar el Proyecto

### 1. Clonar el Repositorio

Clona este repositorio en tu máquina local:

```bash
git clone <url-del-repositorio>
cd <carpeta-del-repositorio>
```

### 2. Configurar Variables de Entorno

Asegúrate de que el archivo `.env.local` en el directorio `frontend` esté configurado correctamente. Por defecto, debería contener:

```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 3. Iniciar los Servicios Locales

Usa Docker Compose para construir e iniciar los servicios:

```bash
docker-compose up --build
```

Esto iniciará los siguientes servicios:

- Redis en el puerto `6379`.
- Coordinador en el puerto `5000`.
- Monitorización en el puerto `5001`.
- Trabajador (ejemplo: `pc-kevin`) en el puerto `5002`.
- Frontend en el puerto `3000`.

### 4. Configurar un Worker-Remote en Otra Máquina

Si deseas configurar un trabajador remoto (`worker-remote`) en otra máquina, sigue estos pasos:

1. **Clonar el Repositorio en la Máquina Remota**  
   En la máquina remota, clona el repositorio y navega al directorio del proyecto:

   ```bash
   git clone <url-del-repositorio>
   cd <carpeta-del-repositorio>
   ```

2. **Configurar el Archivo `docker-compose.yml` del Worker-Remote**  
   Edita el archivo `docker-compose.yml` en el directorio `backend/worker-remote` para que apunte a la IP de la máquina principal donde se ejecutan Redis y Monitorización. Por ejemplo:

   ```yml
   services:
     pc-justin:
       build:
         context: ./backend/worker
       container_name: pc-justin
       environment:
         - WORKER_ID=pc-justin
         - WORKER_IP=<IP_DE_LA_MAQUINA_REMOTA>
         - WORKER_PORT=5003
         - MONITORING_URL=http://<IP_DE_LA_MAQUINA_PRINCIPAL>:5001
         - REDIS_HOST=<IP_DE_LA_MAQUINA_PRINCIPAL>
   ```

   Reemplaza `<IP_DE_LA_MAQUINA_REMOTA>` con la IP de la máquina remota y `<IP_DE_LA_MAQUINA_PRINCIPAL>` con la IP de la máquina principal.

3. **Asegurarse de que Ambas Máquinas Estén en la Misma Red**  
   Ambas máquinas deben estar en la misma red para que puedan comunicarse. Si estás utilizando Docker en ambas máquinas, puedes configurar una red personalizada en Docker para que los contenedores puedan comunicarse entre sí.

   Por ejemplo, crea una red en la máquina principal:

   ```bash
   docker network create real-time-monitoring-network
   ```

   Luego, asegúrate de que todos los servicios en ambas máquinas usen esta red. Agrega lo siguiente al archivo `docker-compose.yml` de cada máquina:

   ```yml
   networks:
     default:
       external:
         name: real-time-monitoring-network
   ```

4. **Iniciar el Worker-Remote**  
   En la máquina remota, navega al directorio `backend/worker-remote` y ejecuta:

   ```bash
   docker-compose up --build
   ```

   Esto iniciará el trabajador remoto y lo registrará en el sistema de monitorización.

### 5. Acceder a la Interfaz

Abre tu navegador y accede a la interfaz del frontend en:

```
http://localhost:3000
```

### 6. Subir una Imagen y Aplicar Filtros

- En la página principal, selecciona una imagen y los filtros que deseas aplicar.
- Haz clic en el botón "Aplicar Filtros".
- Los resultados se abrirán en nuevas pestañas del navegador.

### 7. Supervisar el Estado de los Trabajadores

- Accede al dashboard en la ruta `/dashboard` del frontend.
- Visualiza el estado de los trabajadores, incluyendo el uso de CPU, memoria, disco y red.

## Endpoints Principales

### Coordinador

- **`POST /apply-filters`**: Sube una imagen y aplica los filtros seleccionados.
- **`GET /status`**: Devuelve el estado de la cola de tareas y los trabajadores activos.

### Monitorización

- **`POST /register`**: Registra un nuevo trabajador.
- **`POST /heartbeat`**: Actualiza el estado de un trabajador.
- **`GET /workers`**: Devuelve la lista de trabajadores activos.

## Tecnologías Utilizadas

- **Backend**: Flask, Redis
- **Frontend**: Next.js, React, Styled Components
- **Infraestructura**: Docker, Docker Compose

## Notas Adicionales

- Asegúrate de que el puerto `6379` de Redis esté disponible en tu máquina.
- Si necesitas detener los servicios, usa el comando:

  ```bash
  docker-compose down
  ```

- Para reconstruir los servicios después de realizar cambios en el código, usa:

  ```bash
  docker-compose up --build
  ```

¡Disfruta utilizando el sistema de monitoreo de recursos en tiempo real!
