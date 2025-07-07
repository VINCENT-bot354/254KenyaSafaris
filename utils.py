import json
import os
from flask import url_for

def load_data(filename):
    """Load data from JSON file"""
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default data structure based on filename
        if filename == 'content.json':
            return get_default_content()
        elif filename == 'packages.json':
            return get_default_packages()
        elif filename == 'gallery.json':
            return get_default_gallery()
        elif filename == 'bookings.json':
            return []
        else:
            return {}

def save_data(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join('data', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_url(filename):
    """Get URL for uploaded file"""
    if filename:
        return url_for('static', filename=f'uploads/{filename}')
    return None

def get_default_content():
    """Get default content structure"""
    return {
        'settings': {
            'logo': {'filename': '', 'width': '200', 'height': '80'},
            'flag': {'filename': '', 'width': '40', 'height': '30'}
        },
        'homepage': {
            'hero_title': '254 KENYA SAFARIS',
            'hero_subtitle': 'Experience the Wild Beauty of Kenya',
            'hero_description': 'Discover Kenya\'s breathtaking landscapes, incredible wildlife, and rich cultural heritage with our expertly crafted safari experiences.',
            'about_title': 'About Our Safari Adventures',
            'about_description': 'We specialize in creating unforgettable safari experiences that showcase the best of Kenya. From the iconic Maasai Mara to the stunning Mount Kenya, we offer personalized tours that connect you with nature and local culture.',
            'services_title': 'Our Services',
            'services_description': 'Professional safari coordination, wildlife photography tours, cultural experiences, and adventure activities across Kenya.'
        },
        'destinations': {
            'title': 'Explore Kenya\'s Premier Destinations',
            'description': 'From the world-famous Maasai Mara to the pristine beaches of the coast, Kenya offers diverse landscapes and incredible wildlife experiences.',
            'featured_destinations': [
                'Maasai Mara National Reserve',
                'Amboseli National Park',
                'Tsavo East & West',
                'Lake Nakuru National Park',
                'Mount Kenya National Park',
                'Samburu National Reserve'
            ]
        },
        'activities': {
            'title': 'Safari Activities & Adventures',
            'description': 'Experience Kenya through various exciting activities designed to showcase the country\'s natural beauty and wildlife.',
            'featured_activities': [
                'Game Drives',
                'Wildlife Photography',
                'Cultural Village Visits',
                'Hot Air Balloon Safaris',
                'Nature Walks',
                'Bird Watching'
            ]
        },
        'about': {
            'title': 'About 254 Kenya Safaris',
            'description': 'Your trusted partner for authentic Kenyan safari experiences.',
            'mission': 'To provide exceptional safari experiences that showcase Kenya\'s natural beauty while supporting local communities and conservation efforts.',
            'vision': 'To be Kenya\'s leading safari operator, known for our commitment to sustainable tourism and unforgettable wildlife encounters.',
            'values': 'Conservation, Community, Authenticity, Excellence, and Sustainability are at the heart of everything we do.'
        },
        'contact': {
            'title': 'Contact Us',
            'description': 'Get in touch with our safari experts to plan your perfect Kenyan adventure.',
            'address': 'Nairobi, Kenya',
            'phone': '+254 700 000 000',
            'email': '254kenyasafaris@gmail.com',
            'hours': 'Monday - Friday: 8:00 AM - 6:00 PM',
            'instagram': '',
            'tiktok': '',
            'whatsapp': '',
            'twitter': '',
            'facebook': ''
        }
    }

def get_default_packages():
    """Get default package structure"""
    return [
        {
            'id': 1,
            'name': 'Maasai Mara Classic Safari',
            'description': 'Experience the world-famous Maasai Mara with game drives, cultural visits, and luxury accommodation.',
            'price_usd': '450',
            'price_ksh': '58500',
            'duration': '3 Days / 2 Nights',
            'services': [
                'Transport in 4WD safari vehicle',
                'Professional guide',
                'Accommodation',
                'All meals',
                'Game drives',
                'Cultural village visit'
            ],
            'image': 'https://pixabay.com/get/gd4ce8562a698a347be5d199d7e78e63b38593d5f1d3fe1b1867ba44874575baa0238283fde2be284a79a8cf3cf7b6c4226edc52c486d015147849cc1cd5cbbe3_1280.jpg'
        },
        {
            'id': 2,
            'name': 'Amboseli Elephant Safari',
            'description': 'Witness the majestic elephants of Amboseli with the stunning backdrop of Mount Kilimanjaro.',
            'price_usd': '380',
            'price_ksh': '49400',
            'duration': '2 Days / 1 Night',
            'services': [
                'Transport in safari vehicle',
                'Professional guide',
                'Lodge accommodation',
                'Meals included',
                'Game drives',
                'Photography opportunities'
            ],
            'image': 'https://pixabay.com/get/g258f08c919a8441dc0cb8ad34afa7798fe7d1167f6c6b4495b8200d8ac1816c254e10b08622b82d88add5849151e92747af3969299a26a57d3ec6d44a1ae189a_1280.jpg'
        },
        {
            'id': 3,
            'name': 'Kenya Grand Safari',
            'description': 'Comprehensive safari covering multiple parks including Maasai Mara, Amboseli, and Lake Nakuru.',
            'price_usd': '850',
            'price_ksh': '110500',
            'duration': '7 Days / 6 Nights',
            'services': [
                'Transport in 4WD safari vehicle',
                'Professional guide',
                'Accommodation in lodges',
                'All meals',
                'Game drives',
                'Park fees',
                'Cultural experiences'
            ],
            'image': 'https://pixabay.com/get/g0f3dd39779974552feb01ccfd9b948a4e049739c1f1fb736f8353e749672118a7b68530c54003de89d7820c3d86966ce777a9ca68307065136d12b9bf595caab_1280.jpg'
        }
    ]

def get_default_gallery():
    """Get default gallery structure"""
    return [
        {
            'id': 1,
            'type': 'image',
            'title': 'Maasai Mara Landscape',
            'description': 'Stunning views of the Maasai Mara savanna',
            'url': 'https://pixabay.com/get/gd4ce8562a698a347be5d199d7e78e63b38593d5f1d3fe1b1867ba44874575baa0238283fde2be284a79a8cf3cf7b6c4226edc52c486d015147849cc1cd5cbbe3_1280.jpg',
            'width': '400',
            'height': '300'
        },
        {
            'id': 2,
            'type': 'image',
            'title': 'African Elephant',
            'description': 'Majestic elephants in their natural habitat',
            'url': 'https://pixabay.com/get/g599e0c061cf6ffeb62964ebb8335cd5d47efafdd5c8272e5cda2f2e306f328a7704c43a0a216a9945a53393d3aa7589c98ec74f92995319604dfc00515375578_1280.jpg',
            'width': '400',
            'height': '300'
        },
        {
            'id': 3,
            'type': 'image',
            'title': 'Acacia Tree Silhouette',
            'description': 'Classic African savanna scene',
            'url': 'https://pixabay.com/get/gaf29ec73c761fbce0d5ea3b3306a55c6eaa599873d715f75fe5f72c59fb0d31a69a3268715ae5fdfa5d501d2b2b85f9844704a40722bd998c5bf6ebc52c95633_1280.jpg',
            'width': '400',
            'height': '300'
        },
        {
            'id': 4,
            'type': 'image',
            'title': 'Lions in the Wild',
            'description': 'Big cats of the African savanna',
            'url': 'https://pixabay.com/get/gb4b7fb8e67e1002ddb9b62fa04fa9e7dc424a3a1e35ceb356cd10a0700b56f84ea12236f462eb198c0896242d372173f59c6e626d66cc109b4114fdd66b9584f_1280.jpg',
            'width': '400',
            'height': '300'
        },
        {
            'id': 5,
            'type': 'image',
            'title': 'Zebra Herd',
            'description': 'Zebras grazing in the African plains',
            'url': 'https://pixabay.com/get/gbb9097546aaf1fcf2efce2831de1d6519c1c583ce6d125e3917a6eede9c01b2707d1126a1fd2d18c0e2eaed0230c8e30a173782cbed9884f24fe2fab61abf42f_1280.jpg',
            'width': '400',
            'height': '300'
        },
        {
            'id': 6,
            'type': 'image',
            'title': 'Giraffe Portrait',
            'description': 'Graceful giants of the African wilderness',
            'url': 'https://pixabay.com/get/g47b822ecbbf6ccab32d962ec085e5f702fe29f66283d886e173c9d8ec429806b4817b4e39d63f09b19e5849f5dfba1d11bc42bb9cc5732138a3ee01462fef9f5_1280.jpg',
            'width': '400',
            'height': '300'
        }
    ]
