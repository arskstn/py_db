import sqlite3

DB_NAME = "app_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_superuser INTEGER DEFAULT 0
        );
    """)

    # Таблица прав доступа
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserRights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            can_read INTEGER DEFAULT 0,
            can_write INTEGER DEFAULT 0,
            can_delete INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(menu_item_id) REFERENCES MenuItems(id)
        );
    """)

    # Таблица структуры меню
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MenuItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER NOT NULL DEFAULT 0,
            name TEXT NOT NULL,
            dll_name TEXT,
            func_name TEXT,
            display_order INTEGER NOT NULL,
            FOREIGN KEY(parent_id) REFERENCES MenuItems(id)
        );
    """)

    # Остальные таблицы для справочников, склада, финансов, документов

    # Countries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT
        );
    """)

    # Banks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Banks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            swift_code TEXT
        );
    """)

    # ExpenseCategories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ExpenseCategories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    # TransportExpenses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TransportExpenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    # Suppliers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    # Clients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    # Products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        );
    """)

    # Units
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    # Склад: WarehouseInvoices
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS WarehouseInvoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL,
            date TEXT NOT NULL,
            supplier_id INTEGER,
            FOREIGN KEY(supplier_id) REFERENCES Suppliers(id)
        );
    """)

    # Склад: WarehouseOrders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS WarehouseOrders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT NOT NULL,
            date TEXT NOT NULL,
            client_id INTEGER,
            FOREIGN KEY(client_id) REFERENCES Clients(id)
        );
    """)

    # Финансовый учёт: EnterpriseExpenses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EnterpriseExpenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL,
            category_id INTEGER,
            amount REAL,
            FOREIGN KEY(category_id) REFERENCES ExpenseCategories(id)
        );
    """)

    # Фин. учёт: ProductCostCalculation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProductCostCalculation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            cost_per_unit REAL,
            calc_date TEXT,
            FOREIGN KEY(product_id) REFERENCES Products(id)
        );
    """)

    # Документы: DocInvoices
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DocInvoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            FOREIGN KEY(invoice_id) REFERENCES WarehouseInvoices(id)
        );
    """)

    # Документы: DocOrders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DocOrders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            FOREIGN KEY(order_id) REFERENCES WarehouseOrders(id)
        );
    """)

    # Документы: DocFinReports
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DocFinReports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_name TEXT,
            report_date TEXT
        );
    """)

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
