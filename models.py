from database import get_connection

class MenuItem:
    def __init__(self, id, parent_id, name, dll_name, func_name, display_order):
        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.dll_name = dll_name
        self.func_name = func_name
        self.display_order = display_order

    @staticmethod
    def create_initial_menu_items():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM MenuItems")
        count = cursor.fetchone()[0]
        if count > 0:
            conn.close()
            return

        menu_items = [
            (1,0,"Разное",None,None,1),
            (2,0,"Сотрудники",None,None,2),
            (3,0,"Справочники",None,None,3),
            (4,0,"Склад",None,None,4),
            (5,0,"Финансовый учёт",None,None,5),
            (6,0,"Документы",None,None,6),
            (7,0,"Окно",None,None,7),
            (8,0,"Справка",None,None,8),

            (9,1,"Настройка","settings_module","SettingsForm",1),
            (10,1,"Сменить пароль","change_password_module","ChangePasswordForm",2),

            (11,2,"Выдача прав доступа","user_rights_module","UserRightsForm",1),

            (12,3,"Страны","reference_countries_module","ReferenceCountriesForm",1),
            (13,3,"Банки","reference_banks_module","ReferenceBanksForm",2),
            (14,3,"Категории расходов","reference_expense_categories_module","ReferenceExpenseCategoriesForm",3),
            (15,3,"Транспортные расходы","reference_transport_expenses_module","ReferenceTransportExpensesForm",4),
            (16,3,"Поставщики","reference_suppliers_module","ReferenceSuppliersForm",5),
            (17,3,"Заказчики","reference_clients_module","ReferenceClientsForm",6),
            (18,3,"Товары","reference_products_module","ReferenceProductsForm",7),
            (19,3,"Учётные единицы","reference_units_module","ReferenceUnitsForm",8),

            (20,4,"Накладная","warehouse_invoice_module","WarehouseInvoiceForm",1),
            (21,4,"Заказ","warehouse_order_module","WarehouseOrderForm",2),

            (22,5,"Расходы предприятия","enterprise_expenses_module","EnterpriseExpensesForm",1),
            (23,5,"Расчёт стоимости товара","product_cost_calculation_module","ProductCostCalculationForm",2),

            (24,6,"Накладные","doc_invoices_module","DocInvoicesForm",1),
            (25,6,"Заказы","doc_orders_module","DocOrdersForm",2),
            (26,6,"Финансовая отчётность","doc_fin_reports_module","DocFinReportsForm",3),

            (27,7,"Каскадом","window_module","CascadeWindowsAction",1),
            (28,7,"Свернуть все","window_module","MinimizeAllAction",2),
            (29,7,"Развернуть все","window_module","RestoreAllAction",3),

            (30,8,"Содержание","help_content_module","HelpContentForm",1),
            (31,8,"О программе","about_module","AboutForm",2),
        ]

        cursor.executemany("""
            INSERT INTO MenuItems (id, parent_id, name, dll_name, func_name, display_order)
            VALUES (?,?,?,?,?,?)
        """, menu_items)

        conn.commit()
        conn.close()

class User:
    def __init__(self, id, username, password, is_superuser):
        self.id = id
        self.username = username
        self.password = password
        self.is_superuser = is_superuser

    @staticmethod
    def create_superuser_if_not_exists():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=?",("admin",))
        row = cursor.fetchone()
        if not row:
            cursor.execute("""
                INSERT INTO Users (username, password, is_superuser) 
                VALUES ('admin','admin',1)
            """)
        conn.commit()
        conn.close()
