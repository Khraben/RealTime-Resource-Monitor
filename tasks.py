import requests

url = "http://localhost:5000/task"

tasks = [
    {"task": "Analyze sentiment"},
    {"task": "Process image"},
    {"task": "Generate report"},
    {"task": "Clean data"},
    {"task": "Train model"},
    {"task": "Fetch API data"},
    {"task": "Optimize database"}
]

for i, task_data in enumerate(tasks, start=1):
    response = requests.post(url, json=task_data)
    if response.status_code == 200:
        print(f"Tarea {i} enviada exitosamente:")
        print(response.json())
    else:
        print(f"Error al enviar la tarea {i}: {response.status_code}")
        print(response.text)