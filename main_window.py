import importlib
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QMessageBox
from PyQt5.QtCore import Qt

from database import get_connection
from models import MenuItem

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data  # {id, username, is_superuser}
        self.setWindowTitle("Эксперимент - Главное окно")
        self.resize(1000, 700)

        self.menubar = self.menuBar()
        self.menu_dict = {}

        self.create_menu_structure()

    def create_menu_structure(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, parent_id, name, dll_name, func_name, display_order 
            FROM MenuItems 
            ORDER BY display_order ASC
        """)
        items = cursor.fetchall()
        conn.close()

        menu_items = {}
        for row in items:
            # row = (id, parent_id, name, dll_name, func_name, display_order)
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
        # Проверка прав
        if not self.user_data.get("is_superuser", False):
            if not self.check_user_rights(menu_item.id, "read"):
                QMessageBox.warning(self, "Доступ запрещён", f"У вас нет прав на пункт меню '{menu_item.name}'.")
                return

        dll_name = menu_item.dll_name
        func_name = menu_item.func_name

        # Отдельный случай: пункты 'Окно' (window_module)
        if dll_name == "window_module":
            self.handle_window_actions(func_name)
            return

        # Динамический импорт модуля
        if dll_name and func_name:
            try:
                imported_module = importlib.import_module(f"forms.{dll_name}")
                form_class = getattr(imported_module, func_name, None)
                if form_class:
                    form_instance = form_class(self)
                    form_instance.show()
                else:
                    QMessageBox.warning(self, "Ошибка", f"Класс {func_name} не найден в модуле forms.{dll_name}.")
            except ImportError as e:
                QMessageBox.warning(self, "Ошибка импорта", str(e))
        else:
            QMessageBox.information(self, "Информация", "Этот пункт меню не привязан к форме.")

    def handle_window_actions(self, func_name):
        try:
            imported_module = importlib.import_module("forms.window_module")
            if hasattr(imported_module, func_name):
                func = getattr(imported_module, func_name)
                func(self)
            else:
                QMessageBox.information(self, "Окно", "Неизвестное действие.")
        except ImportError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def check_user_rights(self, menu_item_id, permission="read"):
        col_map = {"read": "can_read", "write": "can_write", "delete": "can_delete"}
        col_name = col_map.get(permission, "can_read")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT {col_name} FROM UserRights WHERE user_id = ? AND menu_item_id = ?",
                       (self.user_data.get('id'), menu_item_id))
        row = cursor.fetchone()
        conn.close()

        if row and row[0] == 1:
            return True
        return False
