# Real-Time Resource Monitor

This project is a real-time resource monitoring system that uses a coordinator-worker architecture with Redis as the message broker. The coordinator assigns tasks to workers, and the workers process the tasks.

## Requirements

To run this project, you need the following installed on your system:

- Docker
- Docker Compose

## How to Run

1. **Clone the Repository**

   Clone this repository to your local machine.

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Start the Services**

   Use Docker Compose to build and start the services.

   ```bash
   docker-compose up --build
   ```

   This will start the following services:

   - Redis (message broker)
   - Coordinator (Flask API)
   - Worker (task processor)

3. **Send a Task**

   Use the task.py script to send a task to the coordinator.

   ```bash
   python task.py
   ```

   The script sends a POST request to the coordinator with a sample task.

4. **Check the Status**

   You can check the status of the task queue by accessing the /status endpoint of the coordinator.

   Open your browser or use a tool like curl:

   ```bash
   curl http://localhost:5000/status
   ```

   This will return the number of tasks currently in the queue.
