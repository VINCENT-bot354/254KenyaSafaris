from flask import Blueprint, render_template, request, redirect, url_for
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Blueprint
updates_bp = Blueprint('updates', __name__)

# PostgreSQL connection helper
def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(db_url)

# Initialize tables
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS updates (
                    id SERIAL PRIMARY KEY,
                    type TEXT NOT NULL,  -- 'news' or 'trip'
                    title TEXT,
                    story TEXT,
                    destination TEXT,
                    description TEXT
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS update_photos (
                    id SERIAL PRIMARY KEY,
                    update_id INTEGER REFERENCES updates(id) ON DELETE CASCADE,
                    photo_url TEXT
                )
            ''')
            conn.commit()

# Call initialization
init_db()

# ----------------------
# Admin Route: Add Update
# ----------------------
@updates_bp.route('/admin/add-update', methods=['GET', 'POST'])
def add_update():
    if request.method == 'POST':
        type_ = request.form.get('type')
        title = request.form.get('title')
        story = request.form.get('story') if type_ == 'news' else None
        destination = request.form.get('destination') if type_ == 'trip' else None
        description = request.form.get('description') if type_ == 'trip' else None

        photo_urls_text = request.form.get('photo_urls', '')
        photo_urls = [url.strip() for url in photo_urls_text.splitlines() if url.strip()]

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO updates (type, title, story, destination, description) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                    (type_, title, story, destination, description)
                )
                update_id = cur.fetchone()[0]

                for url in photo_urls:
                    cur.execute(
                        'INSERT INTO update_photos (update_id, photo_url) VALUES (%s, %s)',
                        (update_id, url)
                    )
                conn.commit()

        return redirect(url_for('updates.add_update'))

    return render_template('admin_add_update.html')

# ----------------------
# Public Route: View Updates
# ----------------------
@updates_bp.route('/updates')
def view_updates():
    updates_with_photos = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, type, title, story, destination, description FROM updates ORDER BY id DESC')
            updates = cur.fetchall()
            for u in updates:
                update_dict = {
                    'id': u[0],
                    'type': u[1],
                    'title': u[2],
                    'story': u[3],
                    'destination': u[4],
                    'description': u[5],
                    'photos': []
                }
                cur.execute('SELECT photo_url FROM update_photos WHERE update_id=%s', (u[0],))
                photos = cur.fetchall()
                update_dict['photos'] = [p[0] for p in photos]
                updates_with_photos.append(update_dict)

    return render_template('public_updates.html', updates=updates_with_photos)
