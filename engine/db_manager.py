"""
db_manager.py
=============
Database Management Module

This module handles all SQLite database operations for the InsightPro inventory system.
It manages:
- Database initialization and schema creation
- Inventory data CRUD operations
- Sales history tracking
- Mock data generation for demo purposes

Tables:
- inventory: Product information and stock levels
- sales: Historical sales data for ML analysis

Author: InsightPro Team
Version: 2.1
"""

import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

DB_NAME = "inventory_v2.db"

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT,
            current_stock INTEGER,
            reorder_point INTEGER,
            unit_cost REAL,
            selling_price REAL
        )
    ''')

    # Create Sales History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            sale_date DATE,
            quantity_sold INTEGER,
            FOREIGN KEY (product_id) REFERENCES inventory (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    if is_db_empty():
        mock_data()

def is_db_empty():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM inventory")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def mock_data():
    """Generates 15 premium office equipment items."""
    print("Generating premium mock data...")
    products = [
        ("Herman Miller Aeron Chair", "Furniture", 12, 15, 800.00, 1450.00),
        ("MacBook Pro M3 Max", "Computers", 8, 10, 2200.00, 3199.00),
        ("Dell UltraSharp 32 4K Monitor", "Displays", 25, 12, 600.00, 950.00),
        ("Logitech MX Master 3S", "Accessories", 45, 20, 60.00, 99.00),
        ("Keychron Q1 Pro Mechanical Keyboard", "Accessories", 30, 10, 140.00, 220.00),
        ("Sony WH-1000XM5 Headphones", "Audio", 18, 15, 250.00, 399.00),
        ("iPad Pro 12.9-inch", "Tablets", 14, 10, 900.00, 1199.00),
        ("Standing Desk Pro (Walnut)", "Furniture", 20, 8, 450.00, 850.00),
        ("CalDigit TS4 Docking Station", "Accessories", 15, 10, 280.00, 400.00),
        ("Fujitsu ScanSnap iX1600", "Office", 10, 5, 350.00, 500.00),
        ("Epson EcoTank Pro ET-5850", "Printers", 8, 4, 600.00, 899.00),
        ("Ubiquiti UniFi Dream Machine", "Networking", 12, 8, 300.00, 450.00),
        ("Samsung 2TB T7 Shield SSD", "Storage", 50, 25, 110.00, 180.00),
        ("Poly Studio P15 Video Bar", "Conferencing", 16, 6, 400.00, 599.00),
        ("Dyson Purifier Cool Gen1", "Office Environment", 10, 5, 350.00, 550.00)
    ]
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for prod in products:
        cursor.execute('''
            INSERT INTO inventory (product_name, category, current_stock, reorder_point, unit_cost, selling_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', prod)
        
        product_id = cursor.lastrowid
        
        # Mock sales for last 60 days
        for i in range(60):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            # Random sales, slightly higher for accessories
            max_qty = 8 if prod[1] == "Accessories" else 3
            qty = random.randint(0, max_qty)
            if random.random() > 0.7: # 30% chance of 0 sales
                qty = 0
                
            cursor.execute('''
                INSERT INTO sales (product_id, sale_date, quantity_sold)
                VALUES (?, ?, ?)
            ''', (product_id, date, qty))
            
    conn.commit()
    conn.close()

def get_inventory_df():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()
    return df

def get_sales_df():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    return df

def update_stock_batch(edited_df):
    """Updates stock levels from an edited DataFrame."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Inefficient but simple for demo: iterate and update
    # Better: use executemany with a list of tuples
    for index, row in edited_df.iterrows():
        cursor.execute("UPDATE inventory SET current_stock = ? WHERE id = ?", (row['current_stock'], row['id']))
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
