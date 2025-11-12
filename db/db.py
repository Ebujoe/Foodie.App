# ============================================
# FOODIE - Database Functions
# ============================================
# This file contains all database functions
# For now, we use Python lists (in-memory data)
# Later, we'll upgrade to SQLite/PostgreSQL
# ============================================

from datetime import datetime
import random

# ============================================
# SAMPLE DATA - Restaurants & Menu Items
# ============================================

# Restaurant Categories
CATEGORIES = [
    {'id': 'fast-food', 'name': 'Fast Food', 'icon': '🍔'},
    {'id': 'pizza', 'name': 'Pizza', 'icon': '🍕'},
    {'id': 'asian', 'name': 'Asian', 'icon': '🍜'},
    {'id': 'healthy', 'name': 'Healthy', 'icon': '🥗'},
    {'id': 'desserts', 'name': 'Desserts', 'icon': '🍰'},
    {'id': 'coffee', 'name': 'Coffee & Drinks', 'icon': '☕'},
]

# Sample Restaurants
RESTAURANTS = [
    {
        'id': 1,
        'name': 'Burger Paradise',
        'category': 'fast-food',
        'description': 'The best burgers in town! Made with fresh ingredients',
        'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&h=300&fit=crop',
        'rating': 4.5,
        'delivery_time': '20-30 min',
        'delivery_fee': 2.99,
        'min_order': 10.00,
        'is_open': True,
        'menu': [
            {'id': 101, 'name': 'Classic Burger', 'description': 'Beef patty, lettuce, tomato, cheese', 'price': 8.99, 'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop'},
            {'id': 102, 'name': 'Cheese Burger', 'description': 'Double cheese, special sauce', 'price': 9.99, 'image': 'https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=300&h=200&fit=crop'},
            {'id': 103, 'name': 'Bacon Burger', 'description': 'Crispy bacon, cheese, BBQ sauce', 'price': 10.99, 'image': 'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=300&h=200&fit=crop'},
            {'id': 104, 'name': 'French Fries', 'description': 'Crispy golden fries', 'price': 3.99, 'image': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=300&h=200&fit=crop'},
            {'id': 105, 'name': 'Coke', 'description': '500ml bottle', 'price': 1.99, 'image': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=300&h=200&fit=crop'},
        ]
    },
    {
        'id': 2,
        'name': 'Pizza Heaven',
        'category': 'pizza',
        'description': 'Authentic Italian pizza with wood-fired oven',
        'image': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&h=300&fit=crop',
        'rating': 4.8,
        'delivery_time': '30-40 min',
        'delivery_fee': 3.49,
        'min_order': 12.00,
        'is_open': True,
        'menu': [
            {'id': 201, 'name': 'Margherita', 'description': 'Tomato, mozzarella, basil', 'price': 11.99, 'image': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300&h=200&fit=crop'},
            {'id': 202, 'name': 'Pepperoni', 'description': 'Spicy pepperoni, cheese', 'price': 13.99, 'image': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300&h=200&fit=crop'},
            {'id': 203, 'name': 'Vegetarian', 'description': 'Mixed vegetables, olives', 'price': 12.99, 'image': 'https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=300&h=200&fit=crop'},
            {'id': 204, 'name': 'Hawaiian', 'description': 'Ham, pineapple, cheese', 'price': 13.49, 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=300&h=200&fit=crop'},
            {'id': 205, 'name': 'Garlic Bread', 'description': 'Crispy garlic bread sticks', 'price': 4.99, 'image': 'https://images.unsplash.com/photo-1573140401552-388fab5200f8?w=300&h=200&fit=crop'},
        ]
    },
    {
        'id': 3,
        'name': 'Sushi Master',
        'category': 'asian',
        'description': 'Fresh sushi and Japanese cuisine',
        'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=500&h=300&fit=crop',
        'rating': 4.7,
        'delivery_time': '35-45 min',
        'delivery_fee': 3.99,
        'min_order': 15.00,
        'is_open': True,
        'menu': [
            {'id': 301, 'name': 'California Roll', 'description': '8 pieces, crab, avocado', 'price': 9.99, 'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=300&h=200&fit=crop'},
            {'id': 302, 'name': 'Salmon Sashimi', 'description': '6 pieces of fresh salmon', 'price': 14.99, 'image': 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=300&h=200&fit=crop'},
            {'id': 303, 'name': 'Spicy Tuna Roll', 'description': '8 pieces, spicy mayo', 'price': 11.99, 'image': 'https://images.unsplash.com/photo-1563612116625-3012372fccce?w=300&h=200&fit=crop'},
            {'id': 304, 'name': 'Miso Soup', 'description': 'Traditional Japanese soup', 'price': 3.99, 'image': 'https://images.unsplash.com/photo-1606491048458-b4a6f7fd9984?w=300&h=200&fit=crop'},
            {'id': 305, 'name': 'Edamame', 'description': 'Steamed soybeans', 'price': 4.99, 'image': 'https://images.unsplash.com/photo-1519076772863-1024dbe66004?w=300&h=200&fit=crop'},
        ]
    },
    {
        'id': 4,
        'name': 'Green Bowl',
        'category': 'healthy',
        'description': 'Healthy bowls, salads & smoothies',
        'image': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&h=300&fit=crop',
        'rating': 4.6,
        'delivery_time': '25-35 min',
        'delivery_fee': 2.49,
        'min_order': 8.00,
        'is_open': True,
        'menu': [
            {'id': 401, 'name': 'Buddha Bowl', 'description': 'Quinoa, avocado, vegetables', 'price': 10.99, 'image': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300&h=200&fit=crop'},
            {'id': 402, 'name': 'Caesar Salad', 'description': 'Chicken, lettuce, parmesan', 'price': 9.99, 'image': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=300&h=200&fit=crop'},
            {'id': 403, 'name': 'Protein Bowl', 'description': 'Grilled chicken, rice, veggies', 'price': 11.99, 'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300&h=200&fit=crop'},
            {'id': 404, 'name': 'Green Smoothie', 'description': 'Spinach, banana, mango', 'price': 5.99, 'image': 'https://images.unsplash.com/photo-1505252585461-04db1eb84625?w=300&h=200&fit=crop'},
            {'id': 405, 'name': 'Acai Bowl', 'description': 'Acai, berries, granola', 'price': 8.99, 'image': 'https://images.unsplash.com/photo-1590301157890-4810ed352733?w=300&h=200&fit=crop'},
        ]
    },
    {
        'id': 5,
        'name': 'Sweet Treats',
        'category': 'desserts',
        'description': 'Delicious desserts, cakes & ice cream',
        'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=500&h=300&fit=crop',
        'rating': 4.9,
        'delivery_time': '20-30 min',
        'delivery_fee': 2.99,
        'min_order': 5.00,
        'is_open': True,
        'menu': [
            {'id': 501, 'name': 'Chocolate Cake', 'description': 'Rich chocolate layer cake', 'price': 6.99, 'image': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=200&fit=crop'},
            {'id': 502, 'name': 'Cheesecake', 'description': 'New York style cheesecake', 'price': 7.99, 'image': 'https://images.unsplash.com/photo-1524351199678-941a58a3df50?w=300&h=200&fit=crop'},
            {'id': 503, 'name': 'Ice Cream Sundae', 'description': 'Vanilla, chocolate, toppings', 'price': 5.99, 'image': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=300&h=200&fit=crop'},
            {'id': 504, 'name': 'Tiramisu', 'description': 'Italian coffee dessert', 'price': 7.49, 'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=300&h=200&fit=crop'},
            {'id': 505, 'name': 'Brownies', 'description': '4 pieces chocolate brownies', 'price': 4.99, 'image': 'https://images.unsplash.com/photo-1607920591413-4ec007e70023?w=300&h=200&fit=crop'},
        ]
    },
    {
        'id': 6,
        'name': 'Coffee Corner',
        'category': 'coffee',
        'description': 'Premium coffee, tea & refreshments',
        'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500&h=300&fit=crop',
        'rating': 4.4,
        'delivery_time': '15-25 min',
        'delivery_fee': 1.99,
        'min_order': 5.00,
        'is_open': True,
        'menu': [
            {'id': 601, 'name': 'Cappuccino', 'description': 'Espresso with steamed milk', 'price': 4.99, 'image': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=300&h=200&fit=crop'},
            {'id': 602, 'name': 'Latte', 'description': 'Smooth espresso with milk', 'price': 4.49, 'image': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=300&h=200&fit=crop'},
            {'id': 603, 'name': 'Iced Coffee', 'description': 'Cold brew with ice', 'price': 3.99, 'image': 'https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=300&h=200&fit=crop'},
            {'id': 604, 'name': 'Croissant', 'description': 'Butter croissant', 'price': 2.99, 'image': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=300&h=200&fit=crop'},
            {'id': 605, 'name': 'Muffin', 'description': 'Blueberry muffin', 'price': 3.49, 'image': 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=300&h=200&fit=crop'},
        ]
    },
]

# Orders storage (in-memory)
ORDERS = []

# ============================================
# RESTAURANT FUNCTIONS
# ============================================

def get_all_restaurants():
    """
    Get all restaurants
    Returns: List of restaurant dictionaries
    """
    return RESTAURANTS

def get_restaurant_by_id(restaurant_id):
    """
    Get a specific restaurant by ID
    Args:
        restaurant_id (int): The restaurant ID
    Returns:
        dict: Restaurant data or None if not found
    """
    for restaurant in RESTAURANTS:
        if restaurant['id'] == restaurant_id:
            return restaurant
    return None

def get_restaurants_by_category(category):
    """
    Get restaurants filtered by category
    Args:
        category (str): Category ID
    Returns:
        list: Filtered restaurants
    """
    if category == 'all':
        return RESTAURANTS
    return [r for r in RESTAURANTS if r['category'] == category]

def get_menu_item_by_id(item_id):
    """
    Find a menu item across all restaurants
    Args:
        item_id (int): Menu item ID
    Returns:
        tuple: (restaurant, item) or (None, None) if not found
    """
    for restaurant in RESTAURANTS:
        for item in restaurant['menu']:
            if item['id'] == item_id:
                return restaurant, item
    return None, None

# ============================================
# CART FUNCTIONS
# ============================================

def get_cart_items(cart_data):
    """
    Convert cart data to full item objects with details
    Args:
        cart_data (list): List of {'id': item_id, 'quantity': qty}
    Returns:
        list: Full cart items with restaurant and item details
    """
    cart_items = []
    
    for cart_item in cart_data:
        restaurant, item = get_menu_item_by_id(cart_item['id'])
        if restaurant and item:
            cart_items.append({
                'id': item['id'],
                'name': item['name'],
                'description': item['description'],
                'price': item['price'],
                'image': item['image'],
                'quantity': cart_item['quantity'],
                'restaurant_name': restaurant['name'],
                'restaurant_id': restaurant['id'],
                'subtotal': item['price'] * cart_item['quantity']
            })
    
    return cart_items

def add_to_cart(cart_data, item_id, quantity=1):
    """
    Add item to cart or update quantity
    Args:
        cart_data (list): Current cart
        item_id (int): Item to add
        quantity (int): Quantity to add
    Returns:
        list: Updated cart
    """
    # Check if item exists
    restaurant, item = get_menu_item_by_id(item_id)
    if not restaurant or not item:
        return cart_data
    
    # Check if already in cart
    for cart_item in cart_data:
        if cart_item['id'] == item_id:
            cart_item['quantity'] += quantity
            return cart_data
    
    # Add new item
    cart_data.append({'id': item_id, 'quantity': quantity})
    return cart_data

def clear_cart():
    """Clear all items from cart"""
    return []

# ============================================
# ORDER FUNCTIONS
# ============================================

def create_order(username, items, total, address, phone, payment_method):
    """
    Create a new order
    Args:
        username (str): User's username
        items (list): Cart items
        total (float): Total amount
        address (str): Delivery address
        phone (str): Phone number
        payment_method (str): Payment method
    Returns:
        int: Order ID
    """
    order_id = len(ORDERS) + 1000  # Start from 1000
    
    order = {
        'id': order_id,
        'username': username,
        'items': items,
        'total': total,
        'address': address,
        'phone': phone,
        'payment_method': payment_method,
        'status': 'pending',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'estimated_delivery': '30-40 min'
    }
    
    ORDERS.append(order)
    return order_id

def get_order_by_id(order_id):
    """
    Get order by ID
    Args:
        order_id (int): Order ID
    Returns:
        dict: Order data or None
    """
    for order in ORDERS:
        if order['id'] == order_id:
            return order
    return None

def get_user_orders(username):
    """
    Get all orders for a user
    Args:
        username (str): Username
    Returns:
        list: User's orders (newest first)
    """
    user_orders = [o for o in ORDERS if o['username'] == username]
    return sorted(user_orders, key=lambda x: x['created_at'], reverse=True)

def get_categories():
    """Get all food categories"""
    return CATEGORIES