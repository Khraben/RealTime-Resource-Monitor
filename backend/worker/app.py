import redis
import json
import time

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

def process_task(task):
    print(f"Processing task: {task}")
    time.sleep(5)
    print(f"Task completed: {task}")

def worker():
    print("Worker is starting...")
    while True:
        try:
            print("Waiting for tasks...")
            task = redis_client.blpop('task_queue', timeout=10)
            if task:
                _, task_data = task
                print(f"Task received: {task_data}")
                task_json = json.loads(task_data)
                process_task(task_json)
            else:
                print("No tasks in queue. Retrying...")
        except Exception as e:
            print(f"Error in worker: {e}")

if __name__ == '__main__':
    try:
        print("Connecting to Redis...")
        redis_client.ping()
        print("Connected to Redis successfully.")
        worker()
    except Exception as e:
        print(f"Unexpected error: {e}")