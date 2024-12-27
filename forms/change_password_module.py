# forms/change_password_module.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from user_management import change_password

class ChangePasswordForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Сменить пароль")

        self.user_id = 0
        if parent and hasattr(parent, "user_data"):
            self.user_id = parent.user_data.get("id", 0)

        layout = QVBoxLayout()

        self.lbl_old = QLabel("Старый пароль:")
        self.txt_old = QLineEdit()
        self.txt_old.setEchoMode(QLineEdit.Password)

        self.lbl_new1 = QLabel("Новый пароль:")
        self.txt_new1 = QLineEdit()
        self.txt_new1.setEchoMode(QLineEdit.Password)

        self.lbl_new2 = QLabel("Повтор нового пароля:")
        self.txt_new2 = QLineEdit()
        self.txt_new2.setEchoMode(QLineEdit.Password)

        self.btn_change = QPushButton("Изменить пароль")
        self.btn_change.clicked.connect(self.handle_change)

        layout.addWidget(self.lbl_old)
        layout.addWidget(self.txt_old)
        layout.addWidget(self.lbl_new1)
        layout.addWidget(self.txt_new1)
        layout.addWidget(self.lbl_new2)
        layout.addWidget(self.txt_new2)
        layout.addWidget(self.btn_change)

        self.setLayout(layout)

    def handle_change(self):
        old_pass = self.txt_old.text().strip()
        new_pass1 = self.txt_new1.text().strip()
        new_pass2 = self.txt_new2.text().strip()

        if self.user_id == 0:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить пользователя.")
            return

        if not old_pass or not new_pass1 or not new_pass2:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        if new_pass1 != new_pass2:
            QMessageBox.warning(self, "Ошибка", "Новые пароли не совпадают.")
            return

        success, msg = change_password(self.user_id, old_pass, new_pass1)
        if success:
            QMessageBox.information(self, "OK", msg)
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", msg)
