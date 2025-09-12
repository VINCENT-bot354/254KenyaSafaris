# updates.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # PostgreSQL URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----------------------
# Database Models
# ----------------------

class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # 'news' or 'trip'
    title = db.Column(db.String(200))
    story = db.Column(db.Text, nullable=True)  # for news
    destination = db.Column(db.String(200), nullable=True)  # for trips
    description = db.Column(db.Text, nullable=True)  # for trips

class UpdatePhoto(db.Model):
    __tablename__ = 'update_photos'
    id = db.Column(db.Integer, primary_key=True)
    update_id = db.Column(db.Integer, db.ForeignKey('updates.id', ondelete="CASCADE"))
    photo_url = db.Column(db.String(500))

def create_tables():
    db.create_all()
    print("Tables created (if not existing)")

# ----------------------
# Admin Route (Add Update)
# ----------------------
@app.route('/admin/add-update', methods=['GET', 'POST'])
def add_update():
    if request.method == 'POST':
        type = request.form.get('type')
        title = request.form.get('title')
        story = request.form.get('story') if type == 'news' else None
        destination = request.form.get('destination') if type == 'trip' else None
        description = request.form.get('description') if type == 'trip' else None

        update = Update(type=type, title=title, story=story, destination=destination, description=description)
        db.session.add(update)
        db.session.commit()

        # handle multiple image URLs
        photo_urls = request.form.getlist('photo_urls')  # list of URLs
        for url in photo_urls:
            if url.strip():
                db.session.add(UpdatePhoto(update_id=update.id, photo_url=url.strip()))
        db.session.commit()

        return redirect(url_for('add_update'))

    return render_template('admin_add_update.html')

# ----------------------
# Public Route (View Updates)
# ----------------------
@app.route('/updates')
def view_updates():
    updates = Update.query.order_by(Update.id.desc()).all()
    updates_with_photos = []
    for u in updates:
        photos = UpdatePhoto.query.filter_by(update_id=u.id).all()
        updates_with_photos.append({'update': u, 'photos': photos})
    return render_template('public_updates.html', updates=updates_with_photos)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

