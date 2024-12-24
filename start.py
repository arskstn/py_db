import os

def create_project_structure():
    # Корневой каталог проекта
    root_dir = "py_db"

    # Список файлов в корневом каталоге
    root_files = [
        "database.py",
        "models.py",
        "user_management.py",
        "login.py",
        "main_window.py",
        "run.py",
    ]

    # Каталог forms и его файлы
    forms_dir = os.path.join(root_dir, "forms")
    forms_files = [
        "__init__.py",
        "settings_form.py",
        "change_password_form.py",
        "user_rights_form.py",
        "reference_countries.py",
        "reference_banks.py",
        "reference_expense_categories.py",
        "reference_transport_expenses.py",
        "reference_suppliers.py",
        "reference_clients.py",
        "reference_products.py",
        "reference_units.py",
        "warehouse_invoice_form.py",
        "warehouse_order_form.py",
        "enterprise_expenses_form.py",
        "product_cost_calculation_form.py",
        "doc_invoices_form.py",
        "doc_orders_form.py",
        "doc_fin_reports_form.py",
        "window_actions.py",
        "help_content_form.py",
        "about_form.py",
    ]

    # Создание корневого каталога
    os.makedirs(root_dir, exist_ok=True)

    # Создание файлов в корневом каталоге
    for file_name in root_files:
        file_path = os.path.join(root_dir, file_name)
        with open(file_path, "w") as f:
            f.write("# " + file_name + "\n")

    # Создание каталога forms
    os.makedirs(forms_dir, exist_ok=True)

    # Создание файлов в каталоге forms
    for file_name in forms_files:
        file_path = os.path.join(forms_dir, file_name)
        with open(file_path, "w") as f:
            f.write("# " + file_name + "\n")

    print(f"Project structure created successfully in '{root_dir}'")

if __name__ == "__main__":
    create_project_structure()
