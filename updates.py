from flask import Blueprint, render_template, request, redirect, url_for
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

updates_bp = Blueprint('updates', __name__)

# ----------------------------
# Database connection
# ----------------------------
def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL environment variable not set")
    # SSL required on Render
    return psycopg2.connect(db_url, sslmode='require')

# ----------------------------
# Initialize tables
# ----------------------------
def init_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Main updates table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS updates (
                        id SERIAL PRIMARY KEY,
                        type TEXT NOT NULL CHECK (type IN ('news', 'trip')),
                        title TEXT,
                        story TEXT,
                        destination TEXT,
                        description TEXT
                    )
                ''')

                # Photos table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS update_photos (
                        id SERIAL PRIMARY KEY,
                        update_id INTEGER REFERENCES updates(id) ON DELETE CASCADE,
                        photo_url TEXT
                    )
                ''')
                conn.commit()
                print("Tables checked/created successfully")
    except Exception as e:
        print("ERROR initializing database:", e)
        raise

# Initialize on import
init_db()

# ----------------------------
# Admin: Add update
# ----------------------------
@updates_bp.route('/admin/updates', methods=['GET', 'POST'])
def admin_updates():
    if request.method == 'POST':
        try:
            # Get form data
            type_ = request.form.get('type') or ''
            title = request.form.get('title') or ''
            story = request.form.get('story') or None
            destination = request.form.get('destination') or None
            description = request.form.get('description') or None

            # Parse image URLs (one per line)
            photo_urls_text = request.form.get('photo_urls', '')
            photo_urls = [url.strip() for url in photo_urls_text.splitlines() if url.strip()]

            # Insert into updates table
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        '''
                        INSERT INTO updates (type, title, story, destination, description)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id
                        ''',
                        (type_, title, story, destination, description)
                    )
                    update_id_row = cur.fetchone()
                    if not update_id_row:
                        raise Exception("Failed to retrieve update ID")
                    update_id = update_id_row[0]

                    # Insert photos if any
                    for url in photo_urls:
                        cur.execute(
                            'INSERT INTO update_photos (update_id, photo_url) VALUES (%s, %s)',
                            (update_id, url)
                        )
                    conn.commit()

            return redirect(url_for('updates.admin_updates'))

        except Exception as e:
            print("ERROR in /admin/updates POST:", e)
            raise

    # GET: render form
    return render_template('admin_updates.html')


# ----------------------------
# Public: View updates
# ----------------------------
@updates_bp.route('/updates')
def view_updates():
    try:
        updates_with_photos = []
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Get all updates
                cur.execute('SELECT id, type, title, story, destination, description FROM updates ORDER BY id DESC')
                updates = cur.fetchall()
                for u in updates:
                    update_dict = {
                        'id': u[0],
                        'type': u[1] or '',
                        'title': u[2] or '',
                        'story': u[3] or '',
                        'destination': u[4] or '',
                        'description': u[5] or '',
                        'photos': []
                    }

                    # Get associated photos
                    cur.execute('SELECT photo_url FROM update_photos WHERE update_id=%s', (u[0],))
                    photos = cur.fetchall()
                    update_dict['photos'] = [p[0] for p in photos if p[0]]
                    updates_with_photos.append(update_dict)
        return render_template('updates.html', updates=updates_with_photos)

    except Exception as e:
        print("ERROR in /updates GET:", e)
        raise


# ----------------------------
# Admin: Manage updates
# ----------------------------
@updates_bp.route('/admin/manage-updates', methods=['GET'])
def manage_updates():
    try:
        updates_list = []
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT id, type, title, story, destination, description FROM updates ORDER BY id DESC')
                updates = cur.fetchall()
                for u in updates:
                    cur.execute('SELECT photo_url FROM update_photos WHERE update_id=%s', (u[0],))
                    photos = cur.fetchall()
                    updates_list.append({
                        'id': u[0],
                        'type': u[1] or '',
                        'title': u[2] or '',
                        'story': u[3] or '',
                        'destination': u[4] or '',
                        'description': u[5] or '',
                        'photos': [p[0] for p in photos if p[0]]
                    })
        return render_template('manage_updates.html', updates=updates_list)
    except Exception as e:
        print("ERROR in /admin/manage-updates GET:", e)
        raise


# ----------------------------
# Admin: Delete update
# ----------------------------
@updates_bp.route('/admin/delete-update/<int:update_id>', methods=['POST'])
def delete_update(update_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Delete photos first (optional, but safe)
                cur.execute('DELETE FROM update_photos WHERE update_id=%s', (update_id,))
                cur.execute('DELETE FROM updates WHERE id=%s', (update_id,))
                conn.commit()
        return redirect(url_for('updates.manage_updates'))
    except Exception as e:
        print(f"ERROR deleting update {update_id}:", e)
        raise
