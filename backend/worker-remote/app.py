import redis
import json
import time
import requests
import os
import psutil
from PIL import Image, ImageOps, ImageFilter

redis_client = redis.Redis(host='172.24.92.26', port=6379, decode_responses=True)
MONITORING_URL = os.getenv('MONITORING_URL', 'http://monitoring:5001')

WORKER_ID = os.getenv('WORKER_ID', 'worker-1')
WORKER_IP = os.getenv('WORKER_IP', '127.0.0.1')
WORKER_PORT = os.getenv('WORKER_PORT', '5002')

def aplicar_filtro_bn(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada).convert("L") 
    imagen.save(ruta_salida)
    print(f"Imagen blanco y negro guardada en {ruta_salida}")

def aplicar_filtro_sepia(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    pixeles = imagen.load()

    for y in range(imagen.height):
        for x in range(imagen.width):
            r, g, b = imagen.getpixel((x, y))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            sepia = (
                min(255, tr),
                min(255, tg),
                min(255, tb)
            )

            pixeles[x, y] = sepia

    imagen.save(ruta_salida)
    print(f"Imagen sepia guardada en {ruta_salida}")

def aplicar_filtro_negativo(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    imagen_negativa = ImageOps.invert(imagen.convert("RGB"))
    imagen_negativa.save(ruta_salida)
    print(f"Imagen negativa guardada en {ruta_salida}")
    
def aplicar_filtro_desenfoque(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    imagen_desenfocada = imagen.filter(ImageFilter.BLUR)
    imagen_desenfocada.save(ruta_salida)
    print(f"Imagen desenfocada guardada en {ruta_salida}")
      
def aplicar_filtro_bordes(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    imagen_bordes = imagen.filter(ImageFilter.FIND_EDGES)
    imagen_bordes.save(ruta_salida)
    print(f"Imagen con bordes guardada en {ruta_salida}")

def aplicar_filtro_grises_ajustable(ruta_entrada, ruta_salida, intensidad):
    imagen = Image.open(ruta_entrada)
    imagen_gris = imagen.convert("L")
    imagen_final = Image.blend(imagen.convert("RGB"), imagen_gris.convert("RGB"), intensidad)
    imagen_final.save(ruta_salida)
    print(f"Imagen en escala de grises ajustada guardada en {ruta_salida}")

def aplicar_filtro_pixelado(ruta_entrada, ruta_salida, pixel_size):
    imagen = Image.open(ruta_entrada)
    imagen_pequeña = imagen.resize(
        (imagen.width // pixel_size, imagen.height // pixel_size), Image.NEAREST
    )
    imagen_pixelada = imagen_pequeña.resize(imagen.size, Image.NEAREST)
    imagen_pixelada.save(ruta_salida)
    print(f"Imagen pixelada guardada en {ruta_salida}")


def register_worker():
    data = {
        'worker_id': WORKER_ID,
        'ip': WORKER_IP,
        'port': WORKER_PORT
    }
    print(f"[REGISTRO] Intentando registrar: {data}")
    try:
        response = requests.post(f'{MONITORING_URL}/register', json=data)
        print(f"[RESPUESTA] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] No se pudo registrar el worker: {e}")



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

        if filter_name == "bn":
            aplicar_filtro_bn(input_path, output_path)
        elif filter_name == "sepia":
            aplicar_filtro_sepia(input_path, output_path)
        elif filter_name == "negativo":
            aplicar_filtro_negativo(input_path, output_path)
        elif filter_name == "desenfoque":
            aplicar_filtro_desenfoque(input_path, output_path)
        elif filter_name == "bordes":
            aplicar_filtro_bordes(input_path, output_path)
        elif filter_name == "grises":
            intensidad = task.get("intensity", 0.5)
            aplicar_filtro_grises_ajustable(input_path, output_path, intensidad)
        elif filter_name == "pixelado":
            pixel_size = task.get("pixel_size", 10)
            aplicar_filtro_pixelado(input_path, output_path, pixel_size)
        else:
            print(f"Unknown filter: {filter_name}")
            return

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
        print("[INICIO] Verificando conexión con Redis...")
        redis_client.ping()
        print("[ÉXITO] Redis está conectado.")

        register_worker()  # 👈 esto es clave

        worker()
    except Exception as e:
        print(f"[ERROR FATAL] {e}")
