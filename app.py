from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

# Database connection configuration
db_connection = psycopg2.connect(
    host=os.environ.get('DB_HOST', 'todo-db'),
    user=os.environ.get('DB_USER', 'postgres'),
    password=os.environ.get('DB_PASSWORD', '123456'),
    dbname=os.environ.get('DB_DATABASE', 'todoapp_db'),
    port=os.environ.get('DB_PORT', 5432)
)

# Route for the homepage
@app.route('/')
def index():
    # Fetch all tasks from the database
    with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    # Render the index.html template with the list of tasks
    return render_template('index.html', tasks=tasks)

# Route for adding a new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    # Add the new task to the database
    add_task_to_database(title, description)
    # Redirect to the homepage
    return redirect(url_for('index'))

# Route for deleting a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        # Execute delete operation for the given task ID
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sql = "DELETE FROM tasks WHERE id = %s"
            cursor.execute(sql, (task_id,))
            db_connection.commit()
    except Exception as e:
        # Print error message and rollback transaction if an error occurs
        print(f"An error occurred: {e}")
        db_connection.rollback()
    # Redirect to the homepage
    return redirect(url_for('index'))

# Route for marking a task as complete
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    try:
        # Execute update operation to mark the task as complete for the given task ID
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sql = "UPDATE tasks SET is_complete = TRUE WHERE id = %s"
            cursor.execute(sql, (task_id,))
            db_connection.commit()
    except Exception as e:
        # Print error message and rollback transaction if an error occurs
        print(f"An error occurred: {e}")
        db_connection.rollback()
    # Redirect to the homepage
    return redirect(url_for('index'))

# Helper function to add a new task to the database
def add_task_to_database(title, description):
    try:
        # Insert a new task record into the tasks table
        with db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sql = "INSERT INTO tasks (title, description) VALUES (%s, %s)"
            cursor.execute(sql, (title, description))
        db_connection.commit()
    except Exception as e:
        # Print error message and rollback transaction if an error occurs
        print(f"An error occurred: {e}")
        db_connection.rollback()

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', debug=True)
