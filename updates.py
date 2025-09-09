from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Define Blueprint
updates_bp = Blueprint('updates', __name__)

# PostgreSQL connection helper
def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(db_url)

# Create table if not exists
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS updates (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    image_url TEXT,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

# Initialize the database
init_db()

# Route: Public updates page
@updates_bp.route('/updates', methods=['GET'])
def updates():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, title, image_url, description, created_at FROM updates ORDER BY created_at DESC')
            all_updates = cur.fetchall()

    # ⚠️ IMPORTANT: Make sure you import/load content from wherever about.html gets it.
    # Example: if you have a content_loader.py or CMS config, pull it here
    from content_loader import content   # adjust import based on your project

    return render_template('updates.html', updates=all_updates, content=content)

# Route: Add update (admin form submits here)
@updates_bp.route('/add-update', methods=['POST'])
def add_update():
    title = request.form['title']
    image_url = request.form.get('image_url')  # optional
    description = request.form['description']

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO updates (title, image_url, description, created_at) VALUES (%s, %s, %s, %s)',
                (title, image_url, description, datetime.utcnow())
            )
            conn.commit()

    return redirect(url_for('updates.updates'))

# Route: Manage updates (admin view)
@updates_bp.route('/manage-updates', methods=['GET'])
def manage_updates():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, title, image_url, description, created_at FROM updates ORDER BY created_at DESC')
            all_updates = cur.fetchall()

    return render_template('manage_updates.html', updates=all_updates)

# Route: Delete update
@updates_bp.route('/delete-update/<int:update_id>', methods=['POST'])
def delete_update(update_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM updates WHERE id = %s', (update_id,))
            conn.commit()

    return redirect(url_for('updates.manage_updates'))
