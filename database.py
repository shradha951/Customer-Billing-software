import sqlite3
import os

class BillingDatabase:
    def __init__(self, db_name='billing_system.db'):
        """Initialize the database connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        # Customers table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Bills table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_number TEXT UNIQUE,
            customer_id INTEGER,
            total_amount REAL,
            cosmetic_total REAL,
            grocery_total REAL,
            drinks_total REAL,
            cosmetic_tax REAL,
            grocery_tax REAL,
            drinks_tax REAL,
            bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
        ''')
        
        # Products table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER,
            category TEXT,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (bill_id) REFERENCES bills (id)
        )
        ''')
        
        self.conn.commit()
    
    def add_customer(self, name, phone):
        """Add a customer to the database or return existing customer."""
        self.cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]  # Return existing customer ID
        
        self.cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_bill(self, bill_data):
        """Add a bill to the database."""
        customer_id = self.add_customer(bill_data['customer_name'], bill_data['customer_phone'])
        
        self.cursor.execute("""
        INSERT INTO bills (bill_number, customer_id, total_amount, 
                          cosmetic_total, grocery_total, drinks_total,
                          cosmetic_tax, grocery_tax, drinks_tax)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            bill_data['bill_number'],
            customer_id,
            bill_data['total_bill'],
            bill_data['cosmetic_price'],
            bill_data['grocery_price'],
            bill_data['drinks_price'],
            bill_data['cosmetic_tax'],
            bill_data['grocery_tax'],
            bill_data['drinks_tax']
        ))
        
        bill_id = self.cursor.lastrowid
        
        # Add products
        for product in bill_data['products']:
            self.cursor.execute("""
            INSERT INTO products (bill_id, category, product_name, quantity, price)
            VALUES (?, ?, ?, ?, ?)
            """, (
                bill_id,
                product['category'],
                product['name'],
                product['quantity'],
                product['price']
            ))
        
        self.conn.commit()
        return bill_id
    
    def get_bill(self, bill_number):
        """Retrieve bill data by bill number."""
        self.cursor.execute("""
        SELECT b.*, c.name, c.phone 
        FROM bills b 
        JOIN customers c ON b.customer_id = c.id 
        WHERE b.bill_number = ?
        """, (bill_number,))
        
        bill = self.cursor.fetchone()
        
        if not bill:
            return None
        
        # Get bill columns
        columns = [desc[0] for desc in self.cursor.description]
        bill_dict = dict(zip(columns, bill))
        
        # Get products for this bill
        self.cursor.execute("SELECT * FROM products WHERE bill_id = ?", (bill_dict['id'],))
        products = []
        
        product_columns = [desc[0] for desc in self.cursor.description]
        for product in self.cursor.fetchall():
            product_dict = dict(zip(product_columns, product))
            products.append(product_dict)
        
        bill_dict['products'] = products
        return bill_dict
    
    def get_all_bills(self):
        """Get all bills with basic information."""
        self.cursor.execute("""
        SELECT b.bill_number, c.name, b.total_amount, b.bill_date 
        FROM bills b 
        JOIN customers c ON b.customer_id = c.id 
        ORDER BY b.bill_date DESC
        """)
        
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, bill)) for bill in self.cursor.fetchall()]
    
    def get_total_sales(self):
        """Get total sales statistics."""
        self.cursor.execute("SELECT SUM(total_amount) FROM bills")
        total_sales = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute("SELECT COUNT(*) FROM bills")
        total_bills = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute("""
        SELECT SUM(cosmetic_total), SUM(grocery_total), SUM(drinks_total),
               SUM(cosmetic_tax), SUM(grocery_tax), SUM(drinks_tax)
        FROM bills
        """)
        category_totals = self.cursor.fetchone()
        
        return {
            'total_sales': total_sales,
            'total_bills': total_bills,
            'cosmetic_total': category_totals[0] or 0,
            'grocery_total': category_totals[1] or 0,
            'drinks_total': category_totals[2] or 0,
            'cosmetic_tax': category_totals[3] or 0,
            'grocery_tax': category_totals[4] or 0,
            'drinks_tax': category_totals[5] or 0
        }
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()