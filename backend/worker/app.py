import redis
import json
import time
import requests
import os
import psutil

# Configuración de Redis y Monitoring
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
MONITORING_URL = os.getenv('MONITORING_URL', 'http://monitoring:5001')

# Información del Worker
WORKER_ID = os.getenv('WORKER_ID', 'worker-1')
WORKER_IP = os.getenv('WORKER_IP', '127.0.0.1')
WORKER_PORT = os.getenv('WORKER_PORT', '5002')

def register_worker():
    """Registra el worker en el módulo /monitoring."""
    data = {
        'worker_id': WORKER_ID,
        'ip': WORKER_IP,
        'port': WORKER_PORT
    }
    try:
        response = requests.post(f'{MONITORING_URL}/register', json=data)
        print(response.json())
    except Exception as e:
        print(f"Error registering worker: {e}")

def send_heartbeat(metrics, tasks_processed):
    """Envía un heartbeat periódico al módulo /monitoring."""
    data = {
        'worker_id': WORKER_ID,
        'cpu_usage': metrics['cpu_usage'],
        'memory_usage': metrics['memory_usage'],
        'disk_usage': metrics['disk_usage'],
        'network_usage': metrics['network_usage'],
        'tasks_processed': tasks_processed
    }
    try:
        response = requests.post(f'{MONITORING_URL}/heartbeat', json=data)
        print(response.json())
    except Exception as e:
        print(f"Error sending heartbeat: {e}")

def process_task(task):
    """Procesa una tarea simulada."""
    print(f"Processing task: {task}")
    time.sleep(5)  # Simula el tiempo de procesamiento
    print(f"Task completed: {task}")

def get_system_metrics():
    """Obtiene las métricas del sistema en porcentajes."""
    cpu_usage = psutil.cpu_percent(interval=1)  # Uso de CPU en %
    memory_usage = psutil.virtual_memory().percent  # Uso de memoria en %
    disk_usage = psutil.disk_usage('/').percent  # Uso de almacenamiento en %
    
    # Uso de red: calculamos el porcentaje de bytes enviados/recibidos en relación a un límite arbitrario
    net_io = psutil.net_io_counters()
    max_bandwidth = 1e9  # Ejemplo: 1 Gbps como capacidad máxima (ajustar según el sistema)
    network_usage = ((net_io.bytes_sent + net_io.bytes_recv) * 8 / max_bandwidth) * 100  # En %

    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "network_usage": min(network_usage, 100)  # Limitar al 100%
    }

def worker():
    """Bucle principal del worker."""
    print("Worker is starting...")
    tasks_processed = 0
    while True:
        try:
            print("Waiting for tasks...")
            task = redis_client.blpop('task_queue', timeout=10)
            if task:
                _, task_data = task
                print(f"Task received: {task_data}")
                task_json = json.loads(task_data)
                process_task(task_json)
                tasks_processed += 1
            else:
                print("No tasks in queue. Retrying...")
            
            metrics = get_system_metrics()
            send_heartbeat(metrics, tasks_processed)
        except Exception as e:
            print(f"Error in worker: {e}")

if __name__ == '__main__':
    try:
        print("Connecting to Redis...")
        redis_client.ping()
        print("Connected to Redis successfully.")

        # Registra el worker en el módulo /monitoring
        register_worker()

        # Inicia el bucle principal del worker
        worker()
    except Exception as e:
        print(f"Unexpected error: {e}")