from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

reviews_bp = Blueprint('reviews', __name__)

# Create the reviews table if it doesn't exist
def init_db():
    with sqlite3.connect('reviews.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            comment TEXT NOT NULL,
            stars INTEGER NOT NULL CHECK (stars >= 1 AND stars <= 5)
        )''')
init_db()

@reviews_bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        comment = request.form['comment']
        stars = int(request.form['stars'])

        with sqlite3.connect('reviews.db') as conn:
            conn.execute('INSERT INTO reviews (name, country, comment, stars) VALUES (?, ?, ?, ?)',
                         (name, country, comment, stars))

        return redirect(url_for('reviews.reviews'))

    with sqlite3.connect('reviews.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT name, country, comment, stars FROM reviews')
        all_reviews = cur.fetchall()

    processed_reviews = []
    for r in all_reviews:
        rounded = round(r[3] * 2) / 2
        processed_reviews.append((r[0], r[1], r[2], rounded))

    return render_template('review.html', reviews=processed_reviews)

@reviews_bp.route('/manage-reviews', methods=['GET'])
def manage_reviews():
    with sqlite3.connect('reviews.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, name, country, comment, stars FROM reviews')
        all_reviews = cur.fetchall()

    return render_template('manage_reviews.html', reviews=all_reviews)

@reviews_bp.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    with sqlite3.connect('reviews.db') as conn:
        conn.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
    return redirect(url_for('reviews.manage_reviews'))
