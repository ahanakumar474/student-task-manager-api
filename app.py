from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import task_manager

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api", methods=["GET"])
def api_info():
    return jsonify({
        "message": "Student Task & Deadline Manager API is running!",
        "endpoints": {
            "GET /tasks": "Get all tasks",
            "POST /tasks": "Create a new task",
            "PUT /tasks/<id>": "Toggle task completion status",
            "DELETE /tasks/<id>": "Delete a task"
        }
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = task_manager.load_tasks()
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Task title is required"}), 400

    try:
        new_task = task_manager.add_task(
            title=data["title"],
            subject=data.get("subject", "General"),
            priority=data.get("priority", "Medium"),
            due_date=data.get("due_date", "")
        )
        return jsonify(new_task), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    updated_task = task_manager.toggle_task_status(task_id)
    if not updated_task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(updated_task), 200


@app.route("/tasks/<task_id>", methods=["DELETE"])
def remove_task(task_id):
    deleted = task_manager.delete_task(task_id)
    if not deleted:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)