from flask import Blueprint, render_template, request, redirect, url_for import os import psycopg2 from dotenv import load_dotenv

Load environment variables from .env file

load_dotenv()

Define Blueprint

reviews_bp = Blueprint('reviews', name)

--- PostgreSQL connection helper ---

def get_connection(): return psycopg2.connect( host=os.getenv("DB_HOST"), dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), sslmode="require" )

--- Create table if not exists ---

def init_db(): with get_connection() as conn: with conn.cursor() as cur: cur.execute(''' CREATE TABLE IF NOT EXISTS reviews ( id SERIAL PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL, comment TEXT NOT NULL, stars INTEGER NOT NULL CHECK (stars >= 1 AND stars <= 5) ) ''') conn.commit()

Initialize the database

init_db()

--- Route: /reviews ---

@reviews_bp.route('/reviews', methods=['GET', 'POST'], endpoint='reviews') def reviews(): if request.method == 'POST': name = request.form['name'] country = request.form['country'] comment = request.form['comment'] stars = int(request.form['stars'])

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

--- Helper: Top reviews ---

def get_top_reviews(limit=5, min_stars=4): with get_connection() as conn: with conn.cursor() as cur: cur.execute( 'SELECT name, country, comment, stars FROM reviews WHERE stars >= %s ORDER BY stars DESC LIMIT %s', (min_stars, limit) ) rows = cur.fetchall()

return [(r[0], r[1], r[2], round(r[3] * 2) / 2) for r in rows]

--- Route: /manage-reviews ---

@reviews_bp.route('/manage-reviews', methods=['GET']) def manage_reviews(): with get_connection() as conn: with conn.cursor() as cur: cur.execute('SELECT id, name, country, comment, stars FROM reviews') all_reviews = cur.fetchall()

return render_template('manage_reviews.html', reviews=all_reviews)

--- Route: /delete-review/<id> ---

@reviews_bp.route('/delete-review/int:review_id', methods=['POST']) def delete_review(review_id): with get_connection() as conn: with conn.cursor() as cur: cur.execute('DELETE FROM reviews WHERE id = %s', (review_id,)) conn.commit()

return redirect(url_for('reviews.manage_reviews'))

