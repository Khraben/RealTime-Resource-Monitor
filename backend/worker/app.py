import redis
import json
import time
import requests
import os
import psutil
from PIL import Image, ImageOps, ImageFilter

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
MONITORING_URL = os.getenv('MONITORING_URL', 'http://monitoring:5001')

WORKER_ID = os.getenv('WORKER_ID', 'worker-1')
WORKER_IP = os.getenv('WORKER_IP', '127.0.0.1')
WORKER_PORT = os.getenv('WORKER_PORT', '5002')

def aplicar_filtro_bn(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    if imagen.mode != "RGB":
        imagen = imagen.convert("RGB")
    imagen_bn = imagen.convert("L").convert("RGB")
    imagen_bn.save(ruta_salida, format='JPEG')
    print(f"Imagen blanco y negro guardada en {ruta_salida}")

def aplicar_filtro_negativo(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    if imagen.mode != "RGB":
        imagen = imagen.convert("RGB")
    imagen_negativa = ImageOps.invert(imagen)
    imagen_negativa.save(ruta_salida, format='JPEG')
    print(f"Imagen negativa guardada en {ruta_salida}")

def aplicar_filtro_grises_ajustable(ruta_entrada, ruta_salida, intensidad):
    imagen = Image.open(ruta_entrada)
    if imagen.mode != "RGB":
        imagen = imagen.convert("RGB")
    imagen_gris = imagen.convert("L").convert("RGB")
    imagen_final = Image.blend(imagen, imagen_gris, intensidad)
    imagen_final.save(ruta_salida, format='JPEG')
    print(f"Imagen en escala de grises ajustada guardada en {ruta_salida}")


def register_worker():
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
    try:
        print(f"Processing task: {task}")
        filter_name = task.get("filter")
        input_path = task.get("image_path")
        output_path = task.get("output_path")

        # Solo permitir un filtro a la vez
        filtros_validos = ["bn", "negativo", "grises"]
        if filter_name not in filtros_validos:
            print(f"Unknown or multiple filters: {filter_name}")
            return

        if filter_name == "bn":
            aplicar_filtro_bn(input_path, output_path)
        elif filter_name == "negativo":
            aplicar_filtro_negativo(input_path, output_path)
        elif filter_name == "grises":
            intensidad = task.get("intensity", 0.5)
            aplicar_filtro_grises_ajustable(input_path, output_path, intensidad)

        print(f"Task completed: {task}")
    except Exception as e:
        print(f"Error processing task: {e}")

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    net_io = psutil.net_io_counters()
    max_bandwidth = 1e8  # 100 Mbps
    network_usage = ((net_io.bytes_sent + net_io.bytes_recv) * 8 / max_bandwidth) * 100
    network_usage = round(network_usage, 10)

    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "network_usage": min(network_usage, 100)
    }

def worker():
    print("Worker is starting...")
    tasks_processed = 0
    while True:
        try:
            print("Waiting for tasks...")
            task = redis_client.blpop('task_queue', timeout=10)
            if task:
                # task is a tuple (queue_name, task_data)
                _, task_data = task
                print(f"Task received: {task_data}")
                try:
                    task_json = json.loads(task_data)
                except Exception as e:
                    print(f"Error decoding task JSON: {e}")
                    continue
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

        register_worker()

        worker()
    except Exception as e:
        print(f"Unexpected error: {e}")