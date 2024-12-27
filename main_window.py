import importlib
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox
from PyQt5.QtCore import Qt

from database import get_connection
from models import MenuItem

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data  # {"id": int, "username": str, "is_superuser": bool}
        self.setWindowTitle("Финансовый учет")
        self.resize(1000, 700)

        self._opened_windows = []

        self.menubar = self.menuBar()
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
            mi = MenuItem(*row)  # (id, parent_id, name, dll_name, func_name, display_order)
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
                    if parent_menu is None:
                        new_menu = self.menubar.addMenu(child_item.name)
                    else:
                        new_menu = parent_menu.addMenu(child_item.name)
                    create_submenu(child_item.id, new_menu)
                else:
                    action = QAction(child_item.name, self)
                    action.setMenuRole(QAction.NoRole)
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
                QMessageBox.warning(self, "Доступ запрещён", f"Нет прав на {menu_item.name}")
                return

        dll_name = menu_item.dll_name
        func_name = menu_item.func_name

        if dll_name == "window_module":
            self.handle_window_actions(func_name)
            return

        if dll_name and func_name:
            try:
                imported_module = importlib.import_module(f"forms.{dll_name}")
                form_class = getattr(imported_module, func_name, None)
                if not form_class:
                    QMessageBox.warning(self, "Ошибка", f"Класс {func_name} не найден в модуле {dll_name}.py")
                    return

                form_instance = form_class(self)
                form_instance.setWindowFlag(Qt.Window)  
                form_instance.resize(600, 400)
                form_instance.show()
                form_instance.raise_()
                form_instance.activateWindow()

                self._opened_windows.append(form_instance)
            except ImportError as e:
                QMessageBox.warning(self, "Ошибка импорта", str(e))
        else:
            QMessageBox.information(self, "Инфо", "Нет dll_name / func_name у данного пункта меню")

    def handle_window_actions(self, func_name):
        import importlib
        try:
            mod = importlib.import_module("forms.window_module")
            if hasattr(mod, func_name):
                func = getattr(mod, func_name)
                func()  
            else:
                QMessageBox.information(self, "Окно", f"Неизвестное действие: {func_name}")
        except ImportError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def check_user_rights(self, menu_item_id, permission="read"):
        col_map = {"read": "can_read", "write": "can_write", "delete": "can_delete"}
        col_name = col_map.get(permission, "can_read")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT {col_name} FROM UserRights WHERE user_id=? AND menu_item_id=?",
                       (self.user_data["id"], menu_item_id))
        row = cursor.fetchone()
        conn.close()

        return (row and row[0] == 1)
