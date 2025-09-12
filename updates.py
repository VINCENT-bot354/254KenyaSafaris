from flask import Blueprint, render_template, request, redirect, url_for
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

updates_bp = Blueprint('updates', __name__)

# ----------------------------
# Database connection
# ----------------------------
def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(db_url, sslmode='require')  # SSL required on Render

# ----------------------------
# Initialize tables
# ----------------------------
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Updates table
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
            # Update photos table
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

# ----------------------------
# Admin page: add updates
# Route: /admin/updates
# ----------------------------
@updates_bp.route('/admin/updates', methods=['GET', 'POST'])
def admin_updates():
    try:
        if request.method == 'POST':
            type_ = request.form.get('type') or ''
            title = request.form.get('title') or ''
            story = request.form.get('story') or None
            destination = request.form.get('destination') or None
            description = request.form.get('description') or None

            # Parse image URLs (one per line)
            photo_urls_text = request.form.get('photo_urls', '')
            photo_urls = [url.strip() for url in photo_urls_text.splitlines() if url.strip()]

            with get_connection() as conn:
                with conn.cursor() as cur:
                    # Insert update
                    cur.execute(
                        '''
                        INSERT INTO updates (type, title, story, destination, description)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id
                        ''',
                        (type_, title, story, destination, description)
                    )
                    update_id_row = cur.fetchone()
                    if update_id_row is None:
                        raise Exception("Failed to retrieve update ID after insert")
                    update_id = update_id_row[0]

                    # Insert photo URLs
                    for url in photo_urls:
                        cur.execute(
                            'INSERT INTO update_photos (update_id, photo_url) VALUES (%s, %s)',
                            (update_id, url)
                        )
                    conn.commit()

            return redirect(url_for('updates.admin_updates'))

        # GET: render form
        return render_template('admin_updates.html')

    except Exception as e:
        print("ERROR in /admin/updates:", e)
        raise

# ----------------------------
# Public page: view updates
# Route: /updates
# ----------------------------
@updates_bp.route('/updates')
def view_updates():
    updates_with_photos = []
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT id, type, title, story, destination, description
                    FROM updates ORDER BY id DESC
                ''')
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
                    cur.execute('SELECT photo_url FROM update_photos WHERE update_id=%s', (u[0],))
                    photos = cur.fetchall()
                    update_dict['photos'] = [p[0] for p in photos if p[0]]
                    updates_with_photos.append(update_dict)
    except Exception as e:
        print("ERROR in /updates:", e)
        raise

    return render_template('updates.html', updates=updates_with_photos)

# ----------------------------
# Admin: manage/delete updates
# Route: /admin/manage-updates
# ----------------------------
@updates_bp.route('/admin/manage-updates', methods=['GET'])
def manage_updates():
    updates_list = []
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT id, type, title, story, destination, description
                    FROM updates ORDER BY id DESC
                ''')
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
    except Exception as e:
        print("ERROR in /admin/manage-updates:", e)
        raise

    return render_template('manage_updates.html', updates=updates_list)

@updates_bp.route('/admin/delete-update/<int:update_id>', methods=['POST'])
def delete_update(update_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # delete photos first (optional due to ON DELETE CASCADE)
                cur.execute('DELETE FROM update_photos WHERE update_id=%s', (update_id,))
                cur.execute('DELETE FROM updates WHERE id=%s', (update_id,))
                conn.commit()
        return redirect(url_for('updates.manage_updates'))
    except Exception as e:
        print(f"ERROR deleting update {update_id}:", e)
        raise
