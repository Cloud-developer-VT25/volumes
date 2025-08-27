from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "todo_db")
DB_USER = os.getenv("DB_USER", "test")
DB_PASS = os.getenv("DB_PASS", "test")

def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return connection

@app.route("/todos", methods=["GET"])
def get_todos():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("SELECT id, title, done FROM todos ORDER BY id;")
    todos = cur.fetchall()
    cur.close()
    connection.close()

    todos = [{ "id": id_, "title": title, "done": done } for id_, title, done in todos]
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.json
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("INSERT INTO todos (title) VALUES (%s) RETURNING id, title, done;", (title,))
    connection.commit()
    cur.close()
    connection.close()

    return jsonify({ "success": True, "message": "Todo added!" }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
