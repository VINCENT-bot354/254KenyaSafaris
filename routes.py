import os
import json
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Message
from werkzeug.utils import secure_filename
from app import app, mail
from utils import load_data, save_data, allowed_file, get_file_url

# Public routes
@app.route('/')
def index():
    content = load_data('content.json')
    packages = load_data('packages.json')
    gallery = load_data('gallery.json')
    return render_template('index.html', content=content, packages=packages[:3], gallery=gallery[:6])

@app.route('/destinations')
def destinations():
    content = load_data('content.json')
    return render_template('destinations.html', content=content)

@app.route('/activities')
def activities():
    content = load_data('content.json')
    return render_template('activities.html', content=content)

@app.route('/packages')
def packages():
    content = load_data('content.json')
    packages = load_data('packages.json')
    return render_template('packages.html', content=content, packages=packages)

@app.route('/bookings')
def bookings():
    content = load_data('content.json')
    packages = load_data('packages.json')
    return render_template('bookings.html', content=content, packages=packages)

@app.route('/gallery')
def gallery():
    content = load_data('content.json')
    gallery = load_data('gallery.json')
    return render_template('gallery.html', content=content, gallery=gallery)

@app.route('/about')
def about():
    content = load_data('content.json')
    return render_template('about.html', content=content)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    content = load_data('content.json')
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        travel_dates = request.form.get('travel_dates')
        group_size = request.form.get('group_size')
        budget = request.form.get('budget')
        
        # Validate required fields
        if not name or not email or not subject or not message:
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html', content=content)
        
        try:
            # Send email to admin
            admin_msg = Message(
                subject=f"New Contact Form Submission: {subject}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[app.config['MAIL_DEFAULT_SENDER']]
            )
            
            admin_msg.body = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}
Subject: {subject}
Travel Dates: {travel_dates or 'Not specified'}
Group Size: {group_size or 'Not specified'}
Budget: {budget or 'Not specified'}

Message:
{message}

Please respond to this inquiry within 24 hours.
"""
            
            # Send confirmation email to customer
            customer_msg = Message(
                subject="Thank you for contacting 254 Kenya Safaris",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[email]
            )
            
            customer_msg.body = f"""
Dear {name},

Thank you for contacting 254 Kenya Safaris! We have received your message regarding: {subject}

We will review your inquiry and respond within 24 hours. Our team is excited to help you plan your perfect Kenyan safari experience.

Your message details:
- Subject: {subject}
- Travel Dates: {travel_dates or 'Not specified'}
- Group Size: {group_size or 'Not specified'}
- Budget: {budget or 'Not specified'}

If you have any urgent questions, please don't hesitate to contact us directly at {content.contact.phone}.

Best regards,
The 254 Kenya Safaris Team

---
This is an automated confirmation. Please do not reply to this email.
"""
            
            # Send both emails
            mail.send(admin_msg)
            mail.send(customer_msg)
            
            flash('Your message has been sent successfully! We will get back to you within 24 hours.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('There was an error sending your message. Please try again or contact us directly.', 'error')
            print(f"Email error: {e}")
            return render_template('contact.html', content=content)
    
    return render_template('contact.html', content=content)

# Booking submission
@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        people = request.form.get('people')
        days = request.form.get('days')
        destinations = request.form.getlist('destinations')
        activities = request.form.getlist('activities')
        message = request.form.get('message', '')
        
        # Create booking record
        booking = {
            'name': name,
            'email': email,
            'phone': phone,
            'people': people,
            'days': days,
            'destinations': destinations,
            'activities': activities,
            'message': message
        }
        
        # Save booking
        bookings = load_data('bookings.json')
        bookings.append(booking)
        save_data('bookings.json', bookings)
        
        # Prepare email content
        destinations_list = '\n'.join([f"• {dest}" for dest in destinations])
        activities_list = '\n'.join([f"• {act}" for act in activities])
        
        email_body = f"""
Thank you for booking with 254 KENYA SAFARIS!

Booking Details:
- Name: {name}
- Email: {email}
- Phone: {phone}
- Number of People: {people}
- Number of Days: {days}

Selected Destinations:
{destinations_list}

Selected Activities:
{activities_list}

Additional Message:
{message}

We will contact you shortly to confirm your booking and provide further details.

Best regards,
254 KENYA SAFARIS Team
        """
        
        # Send confirmation email to customer
        msg = Message(
            subject="Thank you for booking with 254 KENYA SAFARIS",
            recipients=[email],
            body=email_body
        )
        mail.send(msg)
        
        # Send notification to admin
        admin_msg = Message(
            subject="New Booking Received - 254 KENYA SAFARIS",
            recipients=['254kenyasafaris@gmail.com'],
            body=f"New booking received from {name}.\n\n{email_body}"
        )
        mail.send(admin_msg)
        
        flash('✅ Booking received! Please check your email for confirmation.', 'success')
        return redirect(url_for('bookings'))
        
    except Exception as e:
        app.logger.error(f"Booking submission error: {str(e)}")
        flash('There was an error processing your booking. Please try again.', 'error')
        return redirect(url_for('bookings'))

# Admin routes
@app.route('/admin')
def admin_index():
    content = load_data('content.json')
    return render_template('admin/index.html', content=content)

@app.route('/admin/destinations')
def admin_destinations():
    content = load_data('content.json')
    return render_template('admin/destinations.html', content=content)

@app.route('/admin/activities')
def admin_activities():
    content = load_data('content.json')
    return render_template('admin/activities.html', content=content)

@app.route('/admin/packages')
def admin_packages():
    content = load_data('content.json')
    packages = load_data('packages.json')
    return render_template('admin/packages.html', content=content, packages=packages)

@app.route('/admin/gallery')
def admin_gallery():
    content = load_data('content.json')
    gallery = load_data('gallery.json')
    return render_template('admin/gallery.html', content=content, gallery=gallery)

@app.route('/admin/about')
def admin_about():
    content = load_data('content.json')
    return render_template('admin/about.html', content=content)

@app.route('/admin/contact')
def admin_contact():
    content = load_data('content.json')
    return render_template('admin/contact.html', content=content)

@app.route('/admin/settings')
def admin_settings():
    content = load_data('content.json')
    return render_template('admin/settings.html', content=content)

# Admin update routes
@app.route('/admin/update_content', methods=['POST'])
def update_content():
    try:
        page = request.form.get('page')
        content = load_data('content.json')
        
        # Update content based on page
        if page == 'homepage':
            content['homepage'] = {
                'hero_title': request.form.get('hero_title'),
                'hero_subtitle': request.form.get('hero_subtitle'),
                'hero_description': request.form.get('hero_description'),
                'about_title': request.form.get('about_title'),
                'about_description': request.form.get('about_description'),
                'services_title': request.form.get('services_title'),
                'services_description': request.form.get('services_description')
            }
        elif page == 'destinations':
            content['destinations'] = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'featured_destinations': request.form.get('featured_destinations').split('\n') if request.form.get('featured_destinations') else []
            }
        elif page == 'activities':
            content['activities'] = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'featured_activities': request.form.get('featured_activities').split('\n') if request.form.get('featured_activities') else []
            }
        elif page == 'about':
            content['about'] = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'mission': request.form.get('mission'),
                'vision': request.form.get('vision'),
                'values': request.form.get('values')
            }
        elif page == 'contact':
            content['contact'] = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'address': request.form.get('address'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'hours': request.form.get('hours')
            }
        
        save_data('content.json', content)
        flash('Content updated successfully!', 'success')
        return redirect(request.referrer)
        
    except Exception as e:
        app.logger.error(f"Content update error: {str(e)}")
        flash('Error updating content. Please try again.', 'error')
        return redirect(request.referrer)

@app.route('/admin/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.referrer)
        
        file = request.files['file']
        file_type = request.form.get('file_type')
        width = request.form.get('width')
        height = request.form.get('height')
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.referrer)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update content with file info
            content = load_data('content.json')
            if file_type == 'logo':
                content['settings']['logo'] = {
                    'filename': filename,
                    'width': width or '200',
                    'height': height or '80'
                }
            elif file_type == 'flag':
                content['settings']['flag'] = {
                    'filename': filename,
                    'width': width or '40',
                    'height': height or '30'
                }
            
            save_data('content.json', content)
            flash('File uploaded successfully!', 'success')
        else:
            flash('Invalid file type', 'error')
            
        return redirect(request.referrer)
        
    except Exception as e:
        app.logger.error(f"File upload error: {str(e)}")
        flash('Error uploading file. Please try again.', 'error')
        return redirect(request.referrer)

@app.route('/admin/add_package', methods=['POST'])
def add_package():
    try:
        packages = load_data('packages.json')
        
        new_package = {
            'id': len(packages) + 1,
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price_usd': request.form.get('price_usd'),
            'price_ksh': request.form.get('price_ksh'),
            'duration': request.form.get('duration'),
            'services': request.form.get('services').split('\n') if request.form.get('services') else [],
            'image': request.form.get('image', '')
        }
        
        packages.append(new_package)
        save_data('packages.json', packages)
        flash('Package added successfully!', 'success')
        return redirect(url_for('admin_packages'))
        
    except Exception as e:
        app.logger.error(f"Package add error: {str(e)}")
        flash('Error adding package. Please try again.', 'error')
        return redirect(url_for('admin_packages'))

@app.route('/admin/update_package', methods=['POST'])
def update_package():
    try:
        package_id = int(request.form.get('package_id'))
        packages = load_data('packages.json')
        
        for package in packages:
            if package['id'] == package_id:
                package['name'] = request.form.get('name')
                package['description'] = request.form.get('description')
                package['price_usd'] = request.form.get('price_usd')
                package['price_ksh'] = request.form.get('price_ksh')
                package['duration'] = request.form.get('duration')
                package['services'] = request.form.get('services').split('\n') if request.form.get('services') else []
                package['image'] = request.form.get('image', '')
                break
        
        save_data('packages.json', packages)
        flash('Package updated successfully!', 'success')
        return redirect(url_for('admin_packages'))
        
    except Exception as e:
        app.logger.error(f"Package update error: {str(e)}")
        flash('Error updating package. Please try again.', 'error')
        return redirect(url_for('admin_packages'))

@app.route('/admin/delete_package/<int:package_id>')
def delete_package(package_id):
    try:
        packages = load_data('packages.json')
        packages = [p for p in packages if p['id'] != package_id]
        save_data('packages.json', packages)
        flash('Package deleted successfully!', 'success')
        return redirect(url_for('admin_packages'))
        
    except Exception as e:
        app.logger.error(f"Package delete error: {str(e)}")
        flash('Error deleting package. Please try again.', 'error')
        return redirect(url_for('admin_packages'))

@app.route('/admin/add_gallery_item', methods=['POST'])
def add_gallery_item():
    try:
        gallery = load_data('gallery.json')
        
        new_item = {
            'id': len(gallery) + 1,
            'type': request.form.get('type'),
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'url': request.form.get('url'),
            'width': request.form.get('width', '400'),
            'height': request.form.get('height', '300')
        }
        
        gallery.append(new_item)
        save_data('gallery.json', gallery)
        flash('Gallery item added successfully!', 'success')
        return redirect(url_for('admin_gallery'))
        
    except Exception as e:
        app.logger.error(f"Gallery add error: {str(e)}")
        flash('Error adding gallery item. Please try again.', 'error')
        return redirect(url_for('admin_gallery'))

@app.route('/admin/delete_gallery_item/<int:item_id>')
def delete_gallery_item(item_id):
    try:
        gallery = load_data('gallery.json')
        gallery = [item for item in gallery if item['id'] != item_id]
        save_data('gallery.json', gallery)
        flash('Gallery item deleted successfully!', 'success')
        return redirect(url_for('admin_gallery'))
        
    except Exception as e:
        app.logger.error(f"Gallery delete error: {str(e)}")
        flash('Error deleting gallery item. Please try again.', 'error')
        return redirect(url_for('admin_gallery'))
