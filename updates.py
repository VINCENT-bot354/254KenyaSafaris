from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Create Blueprint
updates_bp = Blueprint('updates', __name__)

# Assume db is imported from main app or initialized here
from main import db  # or wherever your db object is

# Models
class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    story = db.Column(db.Text, nullable=True)
    destination = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

class UpdatePhoto(db.Model):
    __tablename__ = 'update_photos'
    id = db.Column(db.Integer, primary_key=True)
    update_id = db.Column(db.Integer, db.ForeignKey('updates.id', ondelete="CASCADE"))
    photo_url = db.Column(db.String(500))

# Admin Route
@updates_bp.route('/admin/add-update', methods=['GET', 'POST'])
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
        photo_urls = request.form.get('photo_urls', '').splitlines()
        for url in photo_urls:
            if url.strip():
                db.session.add(UpdatePhoto(update_id=update.id, photo_url=url.strip()))
        db.session.commit()

        return redirect(url_for('updates.add_update'))

    return render_template('admin_add_update.html')


# Public Route
@updates_bp.route('/updates')
def view_updates():
    updates = Update.query.order_by(Update.id.desc()).all()
    updates_with_photos = []
    for u in updates:
        photos = UpdatePhoto.query.filter_by(update_id=u.id).all()
        updates_with_photos.append({'update': u, 'photos': photos})
    return render_template('public_updates.html', updates=updates_with_photos)
