import requests

url = "http://localhost:5000/task"

task_data = {
    "task": "Analyze sentiment"
}

response = requests.post(url, json=task_data)

if response.status_code == 200:
    print("Tarea enviada exitosamente:")
    print(response.json())
else:
    print(f"Error al enviar la tarea: {response.status_code}")
    print(response.text)