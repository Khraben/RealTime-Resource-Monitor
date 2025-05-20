from flask import Flask, request, jsonify
import redis
import time

app = Flask(__name__)
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.route('/register', methods=['POST'])
def register_worker():
    data = request.json
    worker_id = data['worker_id']
    worker_info = {
        'ip': data['ip'],
        'port': data['port'],
        'cpu_usage': 0,
        'memory_usage': 0,
        'tasks_processed': 0,
        'last_heartbeat': time.time()
    }
    redis_client.hset(f'worker:{worker_id}', mapping=worker_info)
    redis_client.sadd('workers:active', worker_id)
    return jsonify({'message': f'Worker {worker_id} registered successfully'}), 200

@app.route('/heartbeat', methods=['POST'])
def worker_heartbeat():
    data = request.json
    worker_id = data['worker_id']
    if redis_client.sismember('workers:active', worker_id):
        redis_client.hset(f'worker:{worker_id}', 'cpu_usage', data['cpu_usage'])
        redis_client.hset(f'worker:{worker_id}', 'memory_usage', data['memory_usage'])
        redis_client.hset(f'worker:{worker_id}', 'disk_usage', data['disk_usage'])  # Agregar almacenamiento
        redis_client.hset(f'worker:{worker_id}', 'network_usage', data['network_usage'])  # Agregar red
        redis_client.hset(f'worker:{worker_id}', 'tasks_processed', data['tasks_processed'])
        redis_client.hset(f'worker:{worker_id}', 'last_heartbeat', time.time())
        return jsonify({'message': f'Heartbeat received for worker {worker_id}'}), 200
    else:
        return jsonify({'error': 'Worker not registered'}), 400

@app.route('/workers', methods=['GET'])
def get_workers():
    workers = redis_client.smembers('workers:active')
    worker_data = []
    for worker_id in workers:
        data = redis_client.hgetall(f'worker:{worker_id}')
        worker_data.append(data)
    return jsonify(worker_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)