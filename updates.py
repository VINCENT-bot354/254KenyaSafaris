from flask import Blueprint, render_template, request, redirect, url_for
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ----------------------------
# Database connection helper
# ----------------------------
def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL environment variable not set")
    return psycopg2.connect(db_url, sslmode="require")


# ----------------------------
# Initialize tables safely
# ----------------------------
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Reviews table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    country TEXT NOT NULL,
                    comment TEXT NOT NULL,
                    stars INTEGER NOT NULL CHECK (stars >= 1 AND stars <= 5)
                )
            ''')

            # Updates table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS updates (
                    id SERIAL PRIMARY KEY,
                    type TEXT NOT NULL CHECK (type IN ('news','trip')) DEFAULT 'news',
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


# Run init
init_db()

# =======================================================
# REVIEWS BLUEPRINT
# =======================================================
reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/reviews', methods=['GET', 'POST'], endpoint='reviews')
def reviews():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        comment = request.form['comment']
        stars = int(request.form['stars'])

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO reviews (name, country, comment, stars) VALUES (%s, %s, %s, %s)',
                    (name, country, comment, stars)
                )
                conn.commit()

        return redirect(url_for('reviews.reviews'))

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name, country, comment, stars FROM reviews')
            all_reviews = cur.fetchall()

    processed_reviews = [(r[0], r[1], r[2], round(r[3] * 2) / 2) for r in all_reviews]
    return render_template('review.html', reviews=processed_reviews)


@reviews_bp.route('/manage-reviews', methods=['GET'])
@admin_required
def manage_reviews():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, country, comment, stars FROM reviews')
            all_reviews = cur.fetchall()

    return render_template('manage_reviews.html', reviews=all_reviews)


@reviews_bp.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM reviews WHERE id = %s', (review_id,))
            conn.commit()

    return redirect(url_for('reviews.manage_reviews'))


# =======================================================
# UPDATES BLUEPRINT
# =======================================================
updates_bp = Blueprint('updates', __name__)

@updates_bp.route('/admin/updates', methods=['GET', 'POST'])

def admin_updates():
    if request.method == 'POST':
        type_ = request.form.get('type') or 'news'
        title = request.form.get('title') or ''
        story = request.form.get('story') or None
        destination = request.form.get('destination') or None
        description = request.form.get('description') or None

        photo_urls_text = request.form.get('photo_urls', '')
        photo_urls = [url.strip() for url in photo_urls_text.splitlines() if url.strip()]

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    INSERT INTO updates (type, title, story, destination, description)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                    ''',
                    (type_, title, story, destination, description)
                )
                update_id = cur.fetchone()[0]

                # Insert photos
                for url in photo_urls:
                    cur.execute(
                        'INSERT INTO update_photos (update_id, photo_url) VALUES (%s, %s)',
                        (update_id, url)
                    )
            conn.commit()

        return redirect(url_for('updates.admin_updates'))

    return render_template('admin_updates.html')


@updates_bp.route('/updates')
def view_updates():
    updates_with_photos = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, type, title, story, destination, description FROM updates ORDER BY id DESC'
            )
            updates = cur.fetchall()
            for u in updates:
                cur.execute('SELECT photo_url FROM update_photos WHERE update_id=%s', (u[0],))
                photos = cur.fetchall()
                updates_with_photos.append({
                    'id': u[0],
                    'type': u[1] or '',
                    'title': u[2] or '',
                    'story': u[3] or '',
                    'destination': u[4] or '',
                    'description': u[5] or '',
                    'photos': [p[0] for p in photos if p[0]]
                })
    return render_template('updates.html', updates=updates_with_photos)


@updates_bp.route('/admin/manage-updates', methods=['GET'])
def manage_updates():
    updates_list = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, type, title, story, destination, description FROM updates ORDER BY id DESC'
            )
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


@updates_bp.route('/admin/delete-update/<int:update_id>', methods=['POST'])
def delete_update(update_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM update_photos WHERE update_id=%s', (update_id,))
            cur.execute('DELETE FROM updates WHERE id=%s', (update_id,))
            conn.commit()
    return redirect(url_for('updates.manage_updates'))

# ... your existing code above remains unchanged ...

# -----------------------------------------------------
# HELPER FUNCTION TO CHECK FOR NEW UPDATES
# -----------------------------------------------------
def has_new_updates():
    """Return True if there are any updates in the updates table."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT EXISTS(SELECT 1 FROM updates)')
            exists = cur.fetchone()[0]
    return exists
        
