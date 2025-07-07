# 254 Kenya Safaris - Website Management System

## Overview

This is a full-featured, editable website for 254 Kenya Safaris, a Kenyan travel coordination company. The system provides both public-facing pages for customers and admin pages for non-programmer content management. The website showcases safari packages, destinations, activities, and allows online bookings while maintaining a professional presentation with Kenyan visual elements.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 with Flask
- **CSS Framework**: Bootstrap 5.3.0 with custom Kenyan-themed styling
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Responsive Design**: Mobile-first approach with responsive grid layouts
- **Animation System**: Intersection Observer API for scroll-based animations

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **File Structure**: Modular approach with separate routes, utils, and app configuration
- **Session Management**: Flask sessions with configurable secret key
- **File Upload Handling**: Werkzeug secure filename handling with size limits (16MB)
- **Email Integration**: Flask-Mail for contact forms and booking confirmations

### Data Storage
- **Primary Storage**: JSON files for content management
- **File Storage**: Local filesystem for uploaded images
- **Data Files**:
  - `content.json`: Page content and site settings
  - `packages.json`: Safari package information
  - `gallery.json`: Image and video gallery items
  - `bookings.json`: Customer booking submissions

## Key Components

### Public Pages
1. **Homepage** (`/`) - Hero section, featured packages, about preview
2. **Destinations** (`/destinations`) - Featured Kenya safari destinations
3. **Activities** (`/activities`) - Safari activities and experiences
4. **Packages** (`/packages`) - Complete safari package listings
5. **Bookings** (`/bookings`) - Online booking form
6. **Gallery** (`/gallery`) - Photo and video gallery with filtering
7. **About** (`/about`) - Company information, mission, values
8. **Contact** (`/contact`) - Contact form and business information

### Admin System
- **Dashboard**: Overview of bookings, packages, and gallery items
- **Content Management**: Edit all page content without programming
- **Package Management**: Add, edit, delete safari packages
- **Gallery Management**: Upload images, add video links
- **Settings**: Logo and flag upload with dimension controls

### Content Management Features
- **WYSIWYG-style editing**: Direct text editing for all content
- **Image Management**: Upload and resize logos, flags, gallery images
- **Video Integration**: YouTube and Instagram video links
- **Dynamic Updates**: Changes reflect immediately on public pages

## Data Flow

1. **Public Access**: Users browse public pages → Flask routes → Template rendering → JSON data loading
2. **Admin Access**: Admin users edit content → Form submission → Data validation → JSON file updates
3. **File Uploads**: Image uploads → Secure filename processing → File storage → Database reference updates
4. **Email Processing**: Contact/booking forms → Flask-Mail → SMTP delivery via Gmail

## External Dependencies

### Third-Party Services
- **Email Service**: Gmail SMTP (smtp.gmail.com:587)
- **CDN Resources**: 
  - Bootstrap 5.3.0 (CSS framework)
  - Font Awesome 6.4.0 (icons)
- **Image Sources**: Pixabay URLs for default gallery content

### Python Packages
- Flask (web framework)
- Flask-Mail (email handling)
- Werkzeug (utilities, file handling)

### Frontend Libraries
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- Vanilla JavaScript (no external JS dependencies)

## Deployment Strategy

### Environment Configuration
- **Development**: Debug mode enabled, local file storage
- **Production**: Environment variables for sensitive data
- **Session Security**: Configurable session secret key
- **Proxy Support**: ProxyFix middleware for reverse proxy deployments

### File Structure
```
/
├── app.py (Flask application setup)
├── main.py (Application entry point)
├── routes.py (URL routing and view functions)
├── utils.py (Helper functions and data management)
├── data/ (JSON data files)
├── static/ (CSS, JS, uploads)
├── templates/ (HTML templates)
└── templates/admin/ (Admin interface templates)
```

### Security Considerations
- Secure file upload handling with extension validation
- Session management with secret keys
- Input validation and sanitization
- File size limits to prevent abuse

## Changelog

Changelog:
- July 07, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.