import redis
import json
import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# URL del módulo /monitoring
MONITORING_URL = os.getenv('MONITORING_URL', 'http://monitoring:5001')

@app.route('/task', methods=['POST'])
def assign_task():
    """
    Recibe una tarea y la distribuye a los workers.
    """
    task = request.json

    # Obtener el worker menos cargado desde el módulo /monitoring
    worker = get_least_loaded_worker()
    if not worker:
        return jsonify({"error": "No active workers available"}), 503

    # Agregar la tarea a la cola de Redis
    redis_client.rpush('task_queue', json.dumps(task))
    return jsonify({"message": "Task added to queue", "task": task, "assigned_worker": worker}), 200

@app.route('/status', methods=['GET'])
def status():
    """
    Devuelve el estado del sistema.
    """
    tasks_in_queue = redis_client.llen('task_queue')
    workers = get_workers()
    return jsonify({
        "tasks_in_queue": tasks_in_queue,
        "active_workers": workers
    }), 200

def get_workers():
    """
    Consulta el módulo /monitoring para obtener la lista de workers activos.
    """
    try:
        response = requests.get(f'{MONITORING_URL}/workers')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching workers: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error connecting to monitoring: {e}")
        return []

def get_least_loaded_worker():
    """
    Obtiene el worker menos cargado desde el módulo /monitoring.
    """
    workers = get_workers()
    if not workers:
        return None

    # Seleccionar el worker con menor uso de CPU
    least_loaded = min(workers, key=lambda w: float(w.get('cpu_usage', 100)))
    return least_loaded

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)