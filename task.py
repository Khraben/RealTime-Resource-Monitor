import requests

# URL del coordinador
url = "http://localhost:5000/task"

# Datos de la tarea
task_data = {
    "task": "Analyze sentiment"
}

# Enviar la solicitud POST
response = requests.post(url, json=task_data)

# Imprimir la respuesta del coordinador
if response.status_code == 200:
    print("Tarea enviada exitosamente:")
    print(response.json())
else:
    print(f"Error al enviar la tarea: {response.status_code}")
    print(response.text)