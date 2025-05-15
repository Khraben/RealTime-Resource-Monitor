import redis
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/task', methods=['POST'])
def assign_task():
    """
    Recibe una tarea y la distribuye a los workers.
    """
    task = request.json
    redis_client.rpush('task_queue', json.dumps(task))
    return jsonify({"message": "Task added to queue", "task": task}), 200

@app.route('/status', methods=['GET'])
def status():
    """
    Devuelve el estado del sistema.
    """
    tasks_in_queue = redis_client.llen('task_queue')
    return jsonify({"tasks_in_queue": tasks_in_queue}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)