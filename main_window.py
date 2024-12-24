# main_window.py
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QMessageBox
from PyQt5.QtCore import Qt

from database import get_connection
from models import MenuItem

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Эксперимент - Главное окно")
        self.resize(1000, 700)

        self.menubar = self.menuBar()
        self.menu_dict = {}

        self.create_menu_structure()

    def create_menu_structure(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, parent_id, name, dll_name, func_name, display_order FROM MenuItems ORDER BY display_order ASC")
        items = cursor.fetchall()
        conn.close()

        menu_items = {}
        for row in items:
            mi = MenuItem(*row)
            menu_items[mi.id] = mi

        children_map = {}
        for mi_id, mi in menu_items.items():
            pid = mi.parent_id
            if pid not in children_map:
                children_map[pid] = []
            children_map[pid].append(mi)

        def create_submenu(parent_id, parent_menu=None):
            if parent_id not in children_map:
                return
            for child_item in children_map[parent_id]:
                if child_item.dll_name is None and child_item.func_name is None:
                    new_menu = self.menubar.addMenu(child_item.name) if parent_menu is None else parent_menu.addMenu(child_item.name)
                    self.menu_dict[child_item.id] = new_menu
                    create_submenu(child_item.id, new_menu)
                else:
                    action = QAction(child_item.name, self)
                    action.triggered.connect(lambda checked, mi=child_item: self.handle_menu_action(mi))
                    if parent_menu is None:
                        self.menubar.addAction(action)
                    else:
                        parent_menu.addAction(action)

        create_submenu(0, None)

    def handle_menu_action(self, menu_item):
        # Проверка прав доступа (чтение хотя бы)
        if not self.user_data["is_superuser"]:
            if not self.check_user_rights(menu_item.id, "read"):
                QMessageBox.warning(self, "Доступ запрещён", "У вас нет прав к этому пункту меню.")
                return

        # Для упрощения: выводим QMessageBox, что "здесь будет вызов формы"
        # Но можно сделать реальную загрузку формы по dll_name и func_name
        QMessageBox.information(self, "Действие", 
            f"Здесь будет вызов модуля '{menu_item.dll_name}', класса '{menu_item.func_name}'.")

    def check_user_rights(self, menu_item_id, permission="read"):
        col_map = {"read": "can_read", "write": "can_write", "delete": "can_delete"}
        col_name = col_map.get(permission, "can_read")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT {col_name} FROM UserRights WHERE user_id = ? AND menu_item_id = ?", 
                       (self.user_data["id"], menu_item_id))
        row = cursor.fetchone()
        conn.close()

        if row and row[0] == 1:
            return True
        return False
