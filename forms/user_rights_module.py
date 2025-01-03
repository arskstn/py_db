from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QCheckBox, QPushButton, 
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from database import get_connection

class UserRightsForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выдача прав доступа")

        self.label_user = QLabel("Выберите пользователя:")
        self.combo_users = QComboBox()

        self.label_menu = QLabel("Выберите пункт меню (или ВСЕ):")
        self.combo_menu = QComboBox()

        self.check_read = QCheckBox("Чтение")
        self.check_write = QCheckBox("Добавление")
        self.check_delete = QCheckBox("Удаление")
        self.check_update = QCheckBox("Изменение")  # <-- новый чекбокс

        self.btn_save = QPushButton("Сохранить права доступа")

        layout_user = QHBoxLayout()
        layout_user.addWidget(self.label_user)
        layout_user.addWidget(self.combo_users)

        layout_menu = QHBoxLayout()
        layout_menu.addWidget(self.label_menu)
        layout_menu.addWidget(self.combo_menu)

        layout_checks = QHBoxLayout()
        layout_checks.addWidget(self.check_read)
        layout_checks.addWidget(self.check_write)
        layout_checks.addWidget(self.check_delete)
        layout_checks.addWidget(self.check_update)  # новый флажок

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_user)
        layout_main.addLayout(layout_menu)
        layout_main.addLayout(layout_checks)
        layout_main.addWidget(self.btn_save)
        self.setLayout(layout_main)

        self.btn_save.clicked.connect(self.save_rights)

        self.load_users()
        self.load_menu_items()

    def load_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM Users ORDER BY username")
        rows = cursor.fetchall()
        conn.close()

        for (user_id, username) in rows:
            self.combo_users.addItem(username, user_id)

    def load_menu_items(self):
        self.combo_menu.clear()
        # Добавим пункт "ВСЕ" с id=-1, как в предыдущих примерах
        self.combo_menu.addItem("ВСЕ", -1)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM MenuItems ORDER BY display_order")
        rows = cursor.fetchall()
        conn.close()

        for (menu_id, name) in rows:
            self.combo_menu.addItem(name, menu_id)

    def save_rights(self):
        user_id = self.combo_users.currentData()
        menu_id = self.combo_menu.currentData()

        can_read = 1 if self.check_read.isChecked() else 0
        can_write = 1 if self.check_write.isChecked() else 0
        can_delete = 1 if self.check_delete.isChecked() else 0
        can_update = 1 if self.check_update.isChecked() else 0  # <-- сохраняем

        conn = get_connection()
        cursor = conn.cursor()

        if menu_id == -1:
            # "ВСЕ": назначаем права для всех пунктов
            cursor.execute("SELECT id FROM MenuItems")
            all_menu_ids = [row[0] for row in cursor.fetchall()]

            for mid in all_menu_ids:
                cursor.execute("SELECT id FROM UserRights WHERE user_id=? AND menu_item_id=?", (user_id, mid))
                row = cursor.fetchone()
                if row:
                    cursor.execute("""
                        UPDATE UserRights
                        SET can_read=?, can_write=?, can_delete=?, can_update=?
                        WHERE id=?
                    """, (can_read, can_write, can_delete, can_update, row[0]))
                else:
                    cursor.execute("""
                        INSERT INTO UserRights (user_id, menu_item_id, can_read, can_write, can_delete, can_update)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (user_id, mid, can_read, can_write, can_delete, can_update))

        else:
            # конкретный пункт
            cursor.execute("SELECT id FROM UserRights WHERE user_id=? AND menu_item_id=?", (user_id, menu_id))
            row = cursor.fetchone()
            if row:
                # update
                cursor.execute("""
                    UPDATE UserRights
                    SET can_read=?, can_write=?, can_delete=?, can_update=?
                    WHERE id=?
                """, (can_read, can_write, can_delete, can_update, row[0]))
            else:
                # insert
                cursor.execute("""
                    INSERT INTO UserRights (user_id, menu_item_id, can_read, can_write, can_delete, can_update)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, menu_id, can_read, can_write, can_delete, can_update))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Права доступа сохранены.")
