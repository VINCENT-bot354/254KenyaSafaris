// 254 Kenya Safaris - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initializeAnimations();

    // Initialize gallery
    initializeGallery();

    // Initialize form handling
    initializeFormHandling();

    // Initialize navbar toggle
    initializeNavbar();

    // Initialize video handling
    initializeVideoHandling();
});

// Animation functions
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe all elements with animation classes
    document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right').forEach(el => {
        observer.observe(el);
    });
}

// Gallery functionality
function initializeGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');

    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img) {
                const imgSrc = img.src;
                const overlayContent = this.querySelector('.gallery-overlay-content');
                const title = overlayContent?.querySelector('h5')?.textContent || '';
                const description = overlayContent?.querySelector('p')?.textContent || '';

                showImageModal(imgSrc, title, description);
            }
        });
    });
}

function showImageModal(src, title, description) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'galleryModal';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title text-white">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <img src="${src}" alt="${title}" class="img-fluid">
                    ${description ? `<p class="text-white mt-3">${description}</p>` : ''}
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();

    // Clean up modal after hiding
    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

// Form handling
function initializeFormHandling() {
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            if (!validateBookingForm()) {
                e.preventDefault();
                return false;
            }

            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;

            // Re-enable button after form submission
            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 3000);
        });
    }

    // Admin form handling
    const adminForms = document.querySelectorAll('.admin-form');
    adminForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Saving...';
            submitBtn.disabled = true;

            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    });
}

function validateBookingForm() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const people = document.getElementById('people').value;
    const days = document.getElementById('days').value;
    const destinations = document.querySelectorAll('input[name="destinations"]:checked');
    const activities = document.querySelectorAll('input[name="activities"]:checked');

    if (!name || !email || !phone || !people || !days) {
        showAlert('Please fill in all required fields.', 'error');
        return false;
    }

    if (!isValidEmail(email)) {
        showAlert('Please enter a valid email address.', 'error');
        return false;
    }

    if (destinations.length === 0) {
        showAlert('Please select at least one destination.', 'error');
        return false;
    }

    if (activities.length === 0) {
        showAlert('Please select at least one activity.', 'error');
        return false;
    }

    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container').firstElementChild;
    container.insertBefore(alertDiv, container.firstChild);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Navbar functionality
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Video handling
function initializeVideoHandling() {
    const videoContainers = document.querySelectorAll('.video-container');

    videoContainers.forEach(container => {
        const iframe = container.querySelector('iframe');
        if (iframe) {
            // Add click handler for fullscreen
            container.addEventListener('click', function() {
                if (iframe.requestFullscreen) {
                    iframe.requestFullscreen();
                } else if (iframe.webkitRequestFullscreen) {
                    iframe.webkitRequestFullscreen();
                } else if (iframe.msRequestFullscreen) {
                    iframe.msRequestFullscreen();
                }
            });

            // Adjust aspect ratio based on video type
            const src = iframe.src;
            if (src.includes('instagram.com') || src.includes('tiktok.com')) {
                container.classList.add('aspect-9-16');
            }
        }
    });

    // Initialize video play buttons
    const videoPlayButtons = document.querySelectorAll('[onclick^="playVideo"]');
    videoPlayButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const onclickValue = this.getAttribute('onclick');
            const urlMatch = onclickValue.match(/playVideo\('([^']+)'\)/);
            if (urlMatch) {
                playVideo(urlMatch[1]);
            }
        });
    });
}

// Video player function
function playVideo(url) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title text-white">Safari Video</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-0">
                    <div class="ratio ratio-16x9">
                        <iframe src="${getEmbedUrl(url)}" allowfullscreen></iframe>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();

    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

// Get embed URL for videos
function getEmbedUrl(url) {
    if (url.includes('youtube.com/watch')) {
        const videoId = url.split('v=')[1].split('&')[0];
        return `https://www.youtube.com/embed/${videoId}`;
    } else if (url.includes('youtu.be/')) {
        const videoId = url.split('youtu.be/')[1];
        return `https://www.youtube.com/embed/${videoId}`;
    } else if (url.includes('instagram.com')) {
        return url + '/embed';
    } else if (url.includes('tiktok.com')) {
        // TikTok embed format
        return url.replace('/video/', '/embed/');
    }
    return url;
}

// Gallery filtering function
function filterGallery(type) {
    const items = document.querySelectorAll('.gallery-filter-item');
    const buttons = document.querySelectorAll('.btn-group button');

    // Update active button
    buttons.forEach(btn => btn.classList.remove('active'));

    // Find the clicked button using event.target or find by onclick attribute
    const activeButton = document.querySelector(`button[onclick="filterGallery('${type}')"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }

    // Filter items
    items.forEach(item => {
        if (type === 'all' || item.dataset.type === type) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Admin-specific functions
function deleteItem(type, id) {
    if (confirm(`Are you sure you want to delete this ${type}?`)) {
        const form = document.createElement('form');
        form.method = 'POST';

        if (type === 'package') {
            form.action = `/admin/delete_package/${id}`;
        } else if (type === 'gallery') {
            form.action = `/admin/delete_gallery_item/${id}`;
        }

        document.body.appendChild(form);
        form.submit();
    }
}

function toggleEditMode(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.error('Element not found:', elementId);
        return;
    }

    const isEditing = element.classList.contains('editing');

    if (isEditing) {
        element.classList.remove('editing');
        // Save changes
        saveContent(elementId);
    } else {
        element.classList.add('editing');
        // Make content editable
        element.contentEditable = true;
        element.focus();
    }
}

function saveContent(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.error('Element not found:', elementId);
        return;
    }

    element.contentEditable = false;

    // Here you would typically send the content to the server
    // For now, we'll just show a success message
    showAlert('Content saved successfully!', 'success');
}

// File upload preview
function previewFile(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('filePreview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(file);
    }
}

// Image dimension management
function updateImageDimensions(input) {
    const width = document.getElementById('imageWidth').value;
    const height = document.getElementById('imageHeight').value;

    if (width && height) {
        const preview = document.getElementById('filePreview');
        if (preview) {
            preview.style.width = width + 'px';
            preview.style.height = height + 'px';
        }
    }
}

// Package management
function addService() {
    const servicesList = document.getElementById('servicesList');
    const serviceInput = document.getElementById('newService');

    if (serviceInput.value.trim()) {
        const serviceItem = document.createElement('div');
        serviceItem.className = 'input-group mb-2';
        serviceItem.innerHTML = `
            <input type="text" class="form-control" name="services" value="${serviceInput.value.trim()}" readonly>
            <button type="button" class="btn btn-outline-danger" onclick="removeService(this)">
                <i class="fas fa-trash"></i>
            </button>
        `;

        servicesList.appendChild(serviceItem);
        serviceInput.value = '';
    }
}

function removeService(button) {
    button.closest('.input-group').remove();
}

// Video URL validation
function validateVideoUrl(input) {
    const url = input.value;
    const validPatterns = [
        /youtube\.com\/watch\?v=/,
        /youtu\.be\//,
        /instagram\.com\/p\//,
        /instagram\.com\/reel\//,
        /tiktok\.com\//
    ];

    const isValid = validPatterns.some(pattern => pattern.test(url));

    if (url && !isValid) {
        showAlert('Please enter a valid YouTube, Instagram, or TikTok URL.', 'error');
        input.setCustomValidity('Invalid video URL');
    } else {
        input.setCustomValidity('');
    }
}

// Booking calculator
function calculateTotal() {
    const people = parseInt(document.getElementById('people').value) || 0;
    const days = parseInt(document.getElementById('days').value) || 0;
    const selectedPackages = document.querySelectorAll('input[name="packages"]:checked');

    let total = 0;
    selectedPackages.forEach(pkg => {
        const price = parseFloat(pkg.dataset.price) || 0;
        total += price * people * days;
    });

    const totalElement = document.getElementById('estimatedTotal');
    if (totalElement) {
        totalElement.textContent = `Estimated Total: $${total.toFixed(2)}`;
    }
}

// Initialize booking calculator if on bookings page
document.addEventListener('DOMContentLoaded', function() {
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        const inputs = bookingForm.querySelectorAll('input[name="people"], input[name="days"], input[name="packages"]');
        inputs.forEach(input => {
            input.addEventListener('change', calculateTotal);
        });
    }
});

// Mobile menu handling
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('show');
    }
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const mobileMenu = document.getElementById('mobileMenu');
    const navbarToggler = document.querySelector('.navbar-toggler');

    if (mobileMenu && !mobileMenu.contains(e.target) && !navbarToggler.contains(e.target)) {
        mobileMenu.classList.remove('show');
    }
});

// Lazy loading for images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initializeLazyLoading);

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize navbar toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const navbar = document.querySelector('.navbar-collapse');
            if (navbar) {
                navbar.classList.toggle('show');
            }
        });
    }

    // Initialize fade-in animations
    const fadeElements = document.querySelectorAll('.fade-in');
    if (fadeElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        });

        fadeElements.forEach(el => observer.observe(el));
    }

    // Initialize forms
    initializeForms();

    // Initialize service card animations
    initializeServiceCards();
});

function initializeForms() {
    // Add any form-specific JavaScript here
    console.log('Forms initialized');
}

function initializeServiceCards() {
    // Add hover effects to service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}