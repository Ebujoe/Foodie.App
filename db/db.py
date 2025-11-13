# 🗄️ FOODIE - Database Setup (UPDATED with Phone Number!)

import sqlite3
import os

# 📂 Database file location
DB_PATH = 'foodie.db'

# db/db.py

def get_all_restaurants():
    # Example: return a list of restaurant dictionaries
    return [
        {"name": "Green Garden", "cuisine": "Vegetarian", "rating": 4.5},
        {"name": "Spice Route", "cuisine": "Indian", "rating": 4.2},
        {"name": "Bella Pasta", "cuisine": "Italian", "rating": 4.7}
    ]

def get_all_restaurants():
    return []

def get_restaurant_by_id(restaurant_id):
    return {"id": restaurant_id, "name": "Sample", "cuisine": "Fusion"}

def add_to_cart(item_id, quantity):
    print(f"Added item {item_id} x{quantity} to cart.")

def get_cart_items():
    return []

def clear_cart():
    print("Cart cleared.")

def create_order(user_id, cart_items):
    print(f"Order created for user {user_id} with items: {cart_items}")
    return {"order_id": 1, "status": "confirmed"}

def get_user_orders(user_id):
    return [{"order_id": 1, "items": [], "status": "confirmed"}]

def create_order(username, items, total, address, phone, payment_method):
    # Placeholder logic — replace with actual database code later
    print(f"Order created for {username} with {len(items)} items.")
    return 1  # Simulated order ID


def get_connection():
    """
    Create a connection to the database
    This is like opening the door to your database!
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Makes rows act like dictionaries
    return conn


def init_db():
    """
    Initialize database - Creates all tables
    This runs when the app starts
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # ═══════════════════════════════════════════════════════════════
    # 👤 USERS TABLE - Stores user accounts (UPDATED!)
    # ═══════════════════════════════════════════════════════════════
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ═══════════════════════════════════════════════════════════════
    # 🏪 RESTAURANTS TABLE - All restaurants
    # ═══════════════════════════════════════════════════════════════
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cuisine_type TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            rating REAL DEFAULT 0.0,
            delivery_time TEXT,
            min_order REAL DEFAULT 0.0,
            delivery_fee REAL DEFAULT 0.0,
            is_open BOOLEAN DEFAULT 1,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ═══════════════════════════════════════════════════════════════
    # 🍽️ MENU ITEMS TABLE - Food items for each restaurant
    # ═══════════════════════════════════════════════════════════════
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT,
            is_available BOOLEAN DEFAULT 1,
            is_vegetarian BOOLEAN DEFAULT 0,
            is_vegan BOOLEAN DEFAULT 0,
            spice_level INTEGER DEFAULT 0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
    ''')
    
    # ═══════════════════════════════════════════════════════════════
    # 🛒 ORDERS TABLE - Customer orders
    # ═══════════════════════════════════════════════════════════════
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            delivery_address TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
    ''')
    
    # ═══════════════════════════════════════════════════════════════
    # 📦 ORDER ITEMS TABLE - Individual items in each order
    # ═══════════════════════════════════════════════════════════════
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
        )
    ''')
    
    # ═══════════════════════════════════════════════════════════════
    # 🌟 Insert Sample Data (Only if tables are empty)
    # ═══════════════════════════════════════════════════════════════
    
    # Check if restaurants table is empty
    cursor.execute('SELECT COUNT(*) FROM restaurants')
    if cursor.fetchone()[0] == 0:
        print("📦 Adding sample restaurants...")
        
        # Sample UK Restaurants
        restaurants_data = [
            ('Pizza Palace', 'Italian', '123 Oxford St, London', '+44 20 1234 5678', 4.8, '20-30 min', 10.00, 2.99, 1, None),
            ('Burger House', 'American', '456 King St, London', '+44 20 2345 6789', 4.6, '25-35 min', 8.00, 1.99, 1, None),
            ('Noodle Express', 'Asian', '789 Queen St, Manchester', '+44 161 3456 7890', 4.9, '15-25 min', 12.00, 3.49, 1, None),
            ('Fresh & Healthy', 'Healthy', '321 Park Rd, Birmingham', '+44 121 4567 8901', 4.7, '20-30 min', 15.00, 2.49, 1, None),
            ('Curry Kingdom', 'Indian', '654 High St, Leeds', '+44 113 5678 9012', 4.8, '30-40 min', 10.00, 2.99, 1, None),
            ('Sushi Master', 'Japanese', '987 Main St, Edinburgh', '+44 131 6789 0123', 4.9, '25-35 min', 18.00, 3.99, 1, None),
        ]
        
        cursor.executemany('''
            INSERT INTO restaurants (name, cuisine_type, address, phone, rating, delivery_time, min_order, delivery_fee, is_open, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', restaurants_data)
        
        print("✅ Sample restaurants added!")
        
        # Sample Menu Items
        print("📦 Adding sample menu items...")
        
        menu_items_data = [
            # Pizza Palace (id: 1)
            (1, 'Margherita Pizza', 'Classic tomato and mozzarella', 9.99, 'Pizza', None, 1, 1, 0, 0),
            (1, 'Pepperoni Pizza', 'Spicy pepperoni with cheese', 11.99, 'Pizza', None, 1, 0, 0, 1),
            (1, 'Vegetarian Supreme', 'Mixed vegetables with cheese', 10.99, 'Pizza', None, 1, 1, 0, 0),
            (1, 'Garlic Bread', 'Fresh baked garlic bread', 4.99, 'Sides', None, 1, 1, 0, 0),
            (1, 'Caesar Salad', 'Fresh romaine with parmesan', 6.99, 'Salads', None, 1, 0, 0, 0),
            
            # Burger House (id: 2)
            (2, 'Classic Beef Burger', 'Juicy beef patty with lettuce', 8.99, 'Burgers', None, 1, 0, 0, 0),
            (2, 'Chicken Burger', 'Grilled chicken breast', 7.99, 'Burgers', None, 1, 0, 0, 0),
            (2, 'Veggie Burger', 'Plant-based patty', 7.49, 'Burgers', None, 1, 1, 1, 0),
            (2, 'French Fries', 'Crispy golden fries', 3.99, 'Sides', None, 1, 1, 1, 0),
            (2, 'Onion Rings', 'Crispy fried onion rings', 4.49, 'Sides', None, 1, 1, 0, 0),
            
            # Noodle Express (id: 3)
            (3, 'Pad Thai', 'Thai stir-fried noodles', 10.99, 'Noodles', None, 1, 0, 0, 2),
            (3, 'Chicken Ramen', 'Japanese noodle soup', 11.99, 'Noodles', None, 1, 0, 0, 1),
            (3, 'Vegetable Chow Mein', 'Stir-fried noodles with veggies', 9.99, 'Noodles', None, 1, 1, 1, 0),
            (3, 'Spring Rolls', 'Crispy vegetable rolls', 5.99, 'Appetizers', None, 1, 1, 1, 0),
            (3, 'Fried Rice', 'Egg fried rice', 7.99, 'Rice', None, 1, 1, 0, 0),
            
            # Fresh & Healthy (id: 4)
            (4, 'Greek Salad', 'Feta, olives, cucumber', 8.99, 'Salads', None, 1, 1, 0, 0),
            (4, 'Quinoa Bowl', 'Quinoa with roasted vegetables', 10.99, 'Bowls', None, 1, 1, 1, 0),
            (4, 'Chicken Caesar Wrap', 'Grilled chicken in tortilla', 7.99, 'Wraps', None, 1, 0, 0, 0),
            (4, 'Green Smoothie', 'Spinach, banana, apple', 5.99, 'Drinks', None, 1, 1, 1, 0),
            (4, 'Avocado Toast', 'Sourdough with smashed avocado', 6.99, 'Breakfast', None, 1, 1, 1, 0),
            
            # Curry Kingdom (id: 5)
            (5, 'Chicken Tikka Masala', 'Creamy tomato curry', 12.99, 'Curry', None, 1, 0, 0, 2),
            (5, 'Vegetable Biryani', 'Fragrant rice with mixed veggies', 9.99, 'Rice', None, 1, 1, 0, 1),
            (5, 'Butter Chicken', 'Mild creamy chicken curry', 13.99, 'Curry', None, 1, 0, 0, 1),
            (5, 'Garlic Naan', 'Fresh baked bread with garlic', 3.99, 'Breads', None, 1, 1, 0, 0),
            (5, 'Samosas', 'Crispy vegetable pastries', 5.99, 'Appetizers', None, 1, 1, 0, 1),
            
            # Sushi Master (id: 6)
            (6, 'California Roll', 'Crab, avocado, cucumber', 8.99, 'Sushi Rolls', None, 1, 0, 0, 0),
            (6, 'Salmon Nigiri', 'Fresh salmon on rice', 6.99, 'Nigiri', None, 1, 0, 0, 0),
            (6, 'Vegetarian Roll', 'Avocado, cucumber, carrot', 7.49, 'Sushi Rolls', None, 1, 1, 1, 0),
            (6, 'Miso Soup', 'Traditional Japanese soup', 3.99, 'Soups', None, 1, 1, 0, 0),
            (6, 'Edamame', 'Steamed soybeans', 4.99, 'Appetizers', None, 1, 1, 1, 0),
        ]
        
        cursor.executemany('''
            INSERT INTO menu_items (restaurant_id, name, description, price, category, image_url, is_available, is_vegetarian, is_vegan, spice_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', menu_items_data)
        
        print("✅ Sample menu items added!")
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


if __name__ == '__main__':
    # Run this to create/reset database
    init_db()
    print("🎉 Database setup complete!")