import redis
import json
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import traceback
import time

app = Flask(__name__)
CORS(app)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

MONITORING_URL = os.getenv('MONITORING_URL', 'http://monitoring:5001')

@app.route('/apply-filters', methods=['POST'])
def apply_filters():
    try:
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

        print(f"grayscale_intensity: {grayscale_intensity}, pixel_size: {pixel_size}", flush=True)
        tasks = []
        for filter_name in filters:
            task = {
                "filter": filter_name,
                "image_path": image_path,
                "output_path": f"/tmp/{image_id}_{filter_name}.jpg",
            }
            if filter_name == "grises":
                if grayscale_intensity is None:
                    print("Error: grayscale_intensity is None for grises filter")
                    return jsonify({"error": "Missing grayscaleIntensity for grises filter"}), 400
                try:
                    task["intensity"] = float(grayscale_intensity)
                except Exception as e:
                    print(f"Error converting grayscale_intensity: {e}")
                    return jsonify({"error": "Invalid grayscaleIntensity value"}), 400
            elif filter_name == "pixelado":
                if pixel_size is None:
                    print("Error: pixel_size is None for pixelado filter")
                    return jsonify({"error": "Missing pixelSize for pixelado filter"}), 400
                try:
                    task["pixel_size"] = int(pixel_size)
                except Exception as e:
                    print(f"Error converting pixel_size: {e}")
                    return jsonify({"error": "Invalid pixelSize value"}), 400
            tasks.append(task)

        # Verificar conexión a Redis antes de enviar tareas
        try:
            redis_client.ping()
            print("Connected to Redis successfully.", flush=True)
        except Exception as e:
            print(f"Error connecting to Redis: {e}", flush=True)
            return jsonify({"error": f"Error connecting to Redis: {e}"}), 500

        for task in tasks:
            try:
                redis_client.rpush('task_queue', json.dumps(task))
                print(f"Task pushed to Redis: {task}", flush=True)
            except Exception as e:
                print(f"Error pushing task to Redis: {e}", flush=True)
                return jsonify({"error": f"Error pushing task to Redis: {e}"}), 500

        # Esperar a que los archivos de salida existan (máx 10s)
        output_paths = [task["output_path"] for task in tasks]
        start_time = time.time()
        while True:
            all_exist = all(os.path.exists(path) for path in output_paths)
            if all_exist or (time.time() - start_time) > 10:
                break
            time.sleep(0.2)

        return jsonify({"message": "Tasks created successfully", "tasks": tasks})
    except Exception as e:
        print('Exception in /apply-filters:', e, flush=True)
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/status', methods=['GET'])
def status():
    tasks_in_queue = redis_client.llen('task_queue')
    workers = get_workers()
    return jsonify({
        "tasks_in_queue": tasks_in_queue,
        "active_workers": workers
    }), 200

@app.route('/tmp/<path:filename>')
def serve_image(filename):
    return send_from_directory('/tmp', filename, mimetype='image/jpeg')

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

@app.errorhandler(Exception)
def handle_exception(e):
    print('UNCAUGHT EXCEPTION:', e, flush=True)
    traceback.print_exc()
    return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)