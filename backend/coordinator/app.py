import redis
import json
import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

MONITORING_URL = os.getenv('MONITORING_URL', 'http://monitoring:5001')
WORKER_URL = os.getenv('WORKER_URL', 'http://worker:5001/process-task')

@app.route('/apply-filters', methods=['POST'])
def apply_filters():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filters = request.form.get("filters")
    grayscale_intensity = request.form.get("grayscaleIntensity")
    pixel_size = request.form.get("pixelSize")

    if not filters:
        return jsonify({"error": "No filters selected"}), 400

    filters = json.loads(filters)  # Convert string to list
    image_id = str(os.urandom(16).hex())
    image_path = f"/tmp/{image_id}.jpg"
    image.save(image_path)

    tasks = []
    for filter_name in filters:
        task = {
            "filter": filter_name,
            "image_path": image_path,
            "output_path": f"/tmp/{image_id}_{filter_name}.jpg",
        }
        if filter_name == "grises":
            task["intensity"] = float(grayscale_intensity)
        elif filter_name == "pixelado":
            task["pixel_size"] = int(pixel_size)
        tasks.append(task)

    for task in tasks:
        worker = get_least_loaded_worker()
        if not worker:
            return jsonify({"error": "No active workers available"}), 503

        try:
            response = requests.post(WORKER_URL, json=task)
            if response.status_code != 200:
                return jsonify({"error": f"Failed to send task {task}"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Tasks created successfully", "tasks": tasks})

@app.route('/status', methods=['GET'])
def status():
    tasks_in_queue = redis_client.llen('task_queue')
    workers = get_workers()
    return jsonify({
        "tasks_in_queue": tasks_in_queue,
        "active_workers": workers
    }), 200

def get_workers():
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
    workers = get_workers()
    if not workers:
        return None

    least_loaded = min(workers, key=lambda w: float(w.get('cpu_usage', 100)))
    return least_loaded

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)