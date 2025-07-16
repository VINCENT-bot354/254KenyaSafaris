import os
import logging
from flask import Flask
from flask_mail import Mail
from reviews import reviews_bp
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure file uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '254kenyasafaris@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'vketdytghckvgscl')
app.config['MAIL_DEFAULT_SENDER'] = '254kenyasafaris@gmail.com'

mail = Mail(app)

# Add custom Jinja2 filter for video embedding
def get_embed_url(url):
    """Convert video URLs to embed format"""
    if 'youtube.com/watch' in url:
        video_id = url.split('v=')[1].split('&')[0]
        return f"https://www.youtube.com/embed/{video_id}"
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
        return f"https://www.youtube.com/embed/{video_id}"
    elif 'instagram.com' in url:
        # Instagram embed format
        if '/reel/' in url:
            # Extract the reel ID from the URL
            reel_id = url.split('/reel/')[1].split('/')[0].split('?')[0]
            return f"https://www.instagram.com/reel/{reel_id}/embed/"
        elif '/p/' in url:
            # Post format
            post_id = url.split('/p/')[1].split('/')[0].split('?')[0]
            return f"https://www.instagram.com/p/{post_id}/embed/"
        else:
            return url + '/embed/'
    elif 'tiktok.com' in url:
        # TikTok embed format
        return url.replace('/video/', '/embed/')
    return url

app.jinja_env.filters['get_embed_url'] = get_embed_url

# Import routes after app creation
from routes import *

# Create necessary directories
os.makedirs('data', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)
