# ============================================
# FOODIE - Food Delivery Application
# ============================================
# A beautiful food delivery platform inspired by Glovo
# Built with Flask, HTML, CSS, and JavaScript
# 
# Author: Your Name
# Date: 2024
# ============================================

from flask import (
    Flask, 
    render_template, 
    url_for, 
    request,
    flash, 
    redirect, 
    session,
    jsonify
)
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash

# Import database functions
from db.db import (
    get_all_restaurants,
    get_restaurant_by_id,
    add_to_cart,
    get_cart_items,
    clear_cart,
    get_user_orders,
    create_order
)

# ============================================
# APPLICATION SETUP
# ============================================

app = Flask(__name__)

# Configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'foodie-super-secret-key-change-in-production-2024'

# Security
csrf = CSRFProtect(app)

# ============================================
# CONTEXT PROCESSORS
# ============================================
# These make variables available in ALL templates

@app.context_processor
def inject_csrf_token():
    """Make CSRF token available to all templates"""
    return dict(csrf_token=generate_csrf())

@app.context_processor
def inject_site_info():
    """Make site information available to all templates"""
    return dict(
        site_name="FOODIE",
        site_tagline="Your Favorite Food, Delivered Fast! 🍕"
    )

@app.context_processor
def inject_user_info():
    """Make user information available to all templates"""
    return dict(
        is_logged_in=session.get('logged_in', False),
        username=session.get('username', 'Guest'),
        cart_count=len(session.get('cart', []))
    )

# ============================================
# HELPER FUNCTIONS
# ============================================

def login_required(f):
    """
    Decorator to protect routes that require login
    Usage: @login_required above any route function
    """
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in', False):
            flash('⚠️ Please log in to access this page!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================
# PUBLIC ROUTES (No login required)
# ============================================

@app.route('/')
def index():
    """
    Landing Page / Home Page
    Shows featured restaurants and categories
    """
    restaurants = get_all_restaurants()
    return render_template('index.html', 
                         title="Home",
                         restaurants=restaurants)

@app.route('/about')
def about():
    """About page - information about FOODIE"""
    return render_template('about.html', title="About Us")

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration page for new users
    GET: Show registration form
    POST: Process registration
    """
    # If already logged in, redirect to home
    if session.get('logged_in', False):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        error = None
        
        if not username:
            error = '👤 Username is required!'
        elif len(username) < 3:
            error = '👤 Username must be at least 3 characters!'
        elif not email:
            error = '📧 Email is required!'
        elif '@' not in email:
            error = '📧 Please enter a valid email address!'
        elif not password:
            error = '🔒 Password is required!'
        elif len(password) < 6:
            error = '🔒 Password must be at least 6 characters!'
        elif password != confirm_password:
            error = '🔒 Passwords do not match!'
        elif session.get('registered_users', {}).get(username):
            error = f'👤 Username "{username}" is already taken!'
        elif session.get('registered_users', {}).get(email):
            error = f'📧 Email "{email}" is already registered!'
        
        if error:
            flash(error, 'danger')
        else:
            # Store user (in production, use a real database!)
            if 'registered_users' not in session:
                session['registered_users'] = {}
            
            session['registered_users'][username] = {
                'username': username,
                'email': email,
                'password': generate_password_hash(password)
            }
            session.modified = True
            
            flash(f'🎉 Welcome to FOODIE, {username}! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', title="Join FOODIE")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page for existing users
    GET: Show login form
    POST: Process login
    """
    # If already logged in, redirect to home
    if session.get('logged_in', False):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        error = None
        
        if not username:
            error = '👤 Username is required!'
        elif not password:
            error = '🔒 Password is required!'
        else:
            # Check if user exists
            users = session.get('registered_users', {})
            user = users.get(username)
            
            if not user:
                error = '❌ Invalid username or password!'
            elif not check_password_hash(user['password'], password):
                error = '❌ Invalid username or password!'
        
        if error:
            flash(error, 'danger')
        else:
            # Log in the user
            session['logged_in'] = True
            session['username'] = username
            session['email'] = user['email']
            
            flash(f'🎉 Welcome back, {username}! Ready to order?', 'success')
            return redirect(url_for('index'))
    
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    """Log out the current user"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'👋 See you soon, {username}!', 'info')
    return redirect(url_for('index'))

# ============================================
# RESTAURANT ROUTES
# ============================================

@app.route('/restaurants')
def restaurants():
    """
    Show all restaurants
    Can filter by category, cuisine, etc.
    """
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    all_restaurants = get_all_restaurants()
    
    # Filter by category
    if category != 'all':
        all_restaurants = [r for r in all_restaurants if r['category'] == category]
    
    # Filter by search
    if search:
        search = search.lower()
        all_restaurants = [r for r in all_restaurants 
                          if search in r['name'].lower() 
                          or search in r['description'].lower()]
    
    return render_template('restaurants.html',
                         title="Restaurants",
                         restaurants=all_restaurants,
                         current_category=category,
                         search_query=search)

@app.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    """
    Show details of a specific restaurant
    Including menu items
    """
    restaurant = get_restaurant_by_id(restaurant_id)
    
    if not restaurant:
        flash('❌ Restaurant not found!', 'danger')
        return redirect(url_for('restaurants'))
    
    return render_template('restaurant_detail.html',
                         title=restaurant['name'],
                         restaurant=restaurant)

# ============================================
# CART & ORDER ROUTES
# ============================================

@app.route('/cart')
@login_required
def cart():
    """Show shopping cart"""
    cart_items = get_cart_items(session.get('cart', []))
    
    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('cart.html',
                         title="Your Cart",
                         cart_items=cart_items,
                         total=total)

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart_route():
    """Add item to cart (AJAX endpoint)"""
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)
    
    if not item_id:
        return jsonify({'success': False, 'message': 'Invalid item'}), 400
    
    # Add to cart
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if item already in cart
    item_found = False
    for item in session['cart']:
        if item['id'] == item_id:
            item['quantity'] += quantity
            item_found = True
            break
    
    if not item_found:
        session['cart'].append({'id': item_id, 'quantity': quantity})
    
    session.modified = True
    
    return jsonify({
        'success': True, 
        'message': 'Added to cart!',
        'cart_count': len(session['cart'])
    })

@app.route('/remove-from-cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
        session.modified = True
        flash('🗑️ Item removed from cart', 'info')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    cart_items = get_cart_items(session.get('cart', []))
    
    if not cart_items:
        flash('🛒 Your cart is empty!', 'warning')
        return redirect(url_for('restaurants'))
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    if request.method == 'POST':
        # Process order
        address = request.form.get('address')
        phone = request.form.get('phone')
        payment_method = request.form.get('payment_method')
        
        if not address or not phone:
            flash('📍 Please fill in all delivery details!', 'danger')
        else:
            # Create order
            order_id = create_order(
                username=session['username'],
                items=cart_items,
                total=total,
                address=address,
                phone=phone,
                payment_method=payment_method
            )
            
            # Clear cart
            session['cart'] = []
            session.modified = True
            
            flash(f'🎉 Order #{order_id} placed successfully!', 'success')
            return redirect(url_for('order_confirmation', order_id=order_id))
    
    return render_template('checkout.html',
                         title="Checkout",
                         cart_items=cart_items,
                         total=total)

@app.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Order confirmation page"""
    return render_template('order_confirmation.html',
                         title="Order Confirmed",
                         order_id=order_id)

@app.route('/my-orders')
@login_required
def my_orders():
    """Show user's order history"""
    orders = get_user_orders(session['username'])
    return render_template('my_orders.html',
                         title="My Orders",
                         orders=orders)

# ============================================
# API ENDPOINTS (for AJAX requests)
# ============================================

@app.route('/api/check-username')
def check_username():
    """Check if username is available"""
    username = request.args.get('username', '').strip()
    users = session.get('registered_users', {})
    available = username not in users and len(username) >= 3
    return jsonify({'available': available})

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("🍕 Starting FOODIE Application...")
    print("=" * 50)
    print("📱 Open your browser and go to:")
    print("   http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)


