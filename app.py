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
    clear_cart
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
    return dict(csrf_token=generate_csrf())  # Add parentheses to call the function

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
    🔒 This is like a bouncer at a club!
    It checks if you're logged in before letting you in.
    If not logged in → sends you to login page
    If logged in → lets you through! ✅
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
    🏠 LANDING PAGE - This is the FIRST page people see!
    
    What happens here:
    1. If you're NOT logged in → Shows beautiful landing page
       (Landing page has "Sign Up" and "Login" buttons)
    
    2. If you're ALREADY logged in → Sends you to home page
       (Home page shows restaurants)
    
    Think of it like a door:
    - Visitors see a welcome sign 👋
    - Members go straight inside 🚪
    """
    # Check: Are you logged in?
    if session.get('logged_in', False):
        # YES! You're logged in → Go to home page (restaurants)
        return redirect(url_for('home'))
    else:
        # NO! You're a visitor → Show landing page
        return render_template('landing.html', title="Welcome to FOODIE")


@app.route('/home')
@login_required
def home():
    """
    🏡 HOME PAGE - For logged-in users only!
    
    This shows all the restaurants you can order from.
    Only people who logged in can see this page.
    
    If you try to visit without logging in:
    → The @login_required bouncer sends you to login page!
    """
    restaurants = get_all_restaurants()
    return render_template('index.html', 
                         title="Home",
                         restaurants=restaurants)


@app.route('/about')
def about():
    """📖 About page - Anyone can read this!"""
    return render_template('about.html', title="About Us")

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    📝 SIGN UP PAGE
    """
    # If already logged in, redirect to home
    if session.get('logged_in', False):
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Basic validation
        error = None
        
        if not username or len(username) < 3:
            error = '👤 Username must be at least 3 characters!'
        elif not email or '@' not in email:
            error = '📧 Please enter a valid email address!'
        elif not password or len(password) < 6:
            error = '🔒 Password must be at least 6 characters!'
        elif password != confirm_password:
            error = '🔒 Passwords do not match!'
        
        # Check if username already exists
        users = session.get('registered_users', {})
        if username in users:
            error = f'👤 Username "{username}" is already taken!'
        
        if error:
            flash(error, 'danger')
        else:
            # Save user
            if 'registered_users' not in session:
                session['registered_users'] = {}
            
            session['registered_users'][username] = {
                'username': username,
                'email': email,
                'password': generate_password_hash(password)
            }
            session.modified = True
            
            # SUCCESS!
            flash(f'🎉 Account created successfully! Welcome to FOODIE, {username}!', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', title="Join FOODIE")
    
    # Just visiting? Show the sign-up form
    # Also show any success messages if they exist
    return render_template('register.html', title="Join FOODIE")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    🔑 LOGIN PAGE
    
    Step-by-step flow:
    1. You type your username and password
    2. Click "Login" button
    3. We check if username and password match
    4. If correct → Log you in and send you to HOME page! 🏡✅
    5. If wrong → Show error message ❌
    
    After logging in successfully:
    → You go to HOME page where you can see restaurants!
    """
    
    # Already logged in? Go straight to home!
    if session.get('logged_in', False):
        return redirect(url_for('home'))
    
    # Did you click "Login" button?
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        error = None
        
        if not username:
            error = '👤 Username is required!'
        elif not password:
            error = '🔒 Password is required!'
        else:
            # Check if this user exists
            users = session.get('registered_users', {})
            user = users.get(username)
            
            if not user:
                error = '❌ Invalid username or password!'
            elif not check_password_hash(user['password'], password):
                error = '❌ Invalid username or password!'
        
        # Was there an error?
        if error:
            flash(error, 'danger')
        else:
            # SUCCESS! You're logged in! 🎉
            session['logged_in'] = True
            session['username'] = username
            session['email'] = user['email']
            
            # Show success message
            flash(f'🎉 Welcome back, {username}! Ready to order?', 'success')
            
            # IMPORTANT: Send you to HOME page (restaurants)!
            return redirect(url_for('home'))  # ← SENDS YOU TO HOME!
    
    # Just visiting? Show login form
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    """
    👋 LOGOUT
    
    This clears all your login information and sends you back
    to the LANDING page (the first page visitors see).
    
    It's like leaving a building and the door closes behind you!
    """
    username = session.get('username', 'User')
    session.clear()  # Delete all login info
    flash(f'👋 See you soon, {username}!', 'info')
    return redirect(url_for('index'))  # Go back to landing page

# ============================================
# RESTAURANT ROUTES
# ============================================

@app.route('/restaurants')
def restaurants():
    """
    🍔 ALL RESTAURANTS PAGE
    
    Shows a list of all restaurants.
    You can filter by category or search for specific food!
    """
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    all_restaurants = get_all_restaurants()
    
    # Filter by category (Pizza, Burgers, etc.)
    if category != 'all':
        all_restaurants = [r for r in all_restaurants if r['category'] == category]
    
    # Filter by search words
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
    🍕 SINGLE RESTAURANT PAGE
    
    Shows ONE restaurant with all its menu items.
    Like opening a menu at a restaurant!
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
    """
    🛒 SHOPPING CART
    
    Shows all the food items you want to order.
    Only logged-in users can have a cart!
    """
    cart_items = get_cart_items(session.get('cart', []))
    
    # Add up all prices
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('cart.html',
                         title="Your Cart",
                         cart_items=cart_items,
                         total=total)


@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart_route():
    """
    ➕ ADD TO CART (AJAX)
    
    When you click "Add to Cart" button on a food item,
    this adds it to your cart!
    """
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)
    
    if not item_id:
        return jsonify({'success': False, 'message': 'Invalid item'}), 400
    
    # Add to cart
    if 'cart' not in session:
        session['cart'] = []
    
    # Is this item already in your cart?
    item_found = False
    for item in session['cart']:
        if item['id'] == item_id:
            item['quantity'] += quantity  # Add more!
            item_found = True
            break
    
    # New item? Add it!
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
    """🗑️ Remove item from cart"""
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
        session.modified = True
        flash('🗑️ Item removed from cart', 'info')
    
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """
    💳 CHECKOUT PAGE
    
    Where you pay and enter your delivery address.
    Final step before ordering!
    """
    cart_items = get_cart_items(session.get('cart', []))
    
    if not cart_items:
        flash('🛒 Your cart is empty!', 'warning')
        return redirect(url_for('restaurants'))
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    if request.method == 'POST':
        # Get delivery info
        address = request.form.get('address')
        phone = request.form.get('phone')
        payment_method = request.form.get('payment_method')
        
        if not address or not phone:
            flash('📍 Please fill in all delivery details!', 'danger')
        else:
            # Create order
            from db.db import create_order
            order_id = create_order(
                username=session['username'],
                items=cart_items,
                total=total,
                address=address,
                phone=phone,
                payment_method=payment_method
            )
            
            # Empty the cart
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
    """✅ Order confirmed! Your food is on the way!"""
    return render_template('order_confirmation.html',
                         title="Order Confirmed",
                         order_id=order_id)


@app.route('/my-orders')
@login_required
def my_orders():
    """📜 Your order history - See all your past orders"""
    from db.db import get_user_orders
    orders = get_user_orders(session['username'])
    return render_template('my_orders.html',
                         title="My Orders",
                         orders=orders)

# ============================================
# API ENDPOINTS (for AJAX requests)
# ============================================

@app.route('/api/check-username')
def check_username():
    """Check if username is available (for live checking)"""
    username = request.args.get('username', '').strip()
    users = session.get('registered_users', {})
    available = username not in users and len(username) >= 3
    return jsonify({'available': available})

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    """😢 Page not found (404 error)"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """💥 Something went wrong (500 error)"""
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
    print("\n🎯 USER FLOW:")
    print("   1. Landing Page (/)        → Shows welcome page")
    print("   2. Sign Up (/register)     → Create account")
    print("   3. Login (/login)          → Enter with username/password")
    print("   4. Home Page (/home)       → See restaurants!")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)