# forms/change_password_form.py
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from user_management import change_password

class ChangePasswordForm(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Сменить пароль")

        self.label_old = QLabel("Старый пароль:")
        self.edit_old = QLineEdit()
        self.edit_old.setEchoMode(QLineEdit.Password)

        self.label_new1 = QLabel("Новый пароль:")
        self.edit_new1 = QLineEdit()
        self.edit_new1.setEchoMode(QLineEdit.Password)

        self.label_new2 = QLabel("Повторите новый пароль:")
        self.edit_new2 = QLineEdit()
        self.edit_new2.setEchoMode(QLineEdit.Password)

        self.btn_change = QPushButton("Изменить пароль")
        self.btn_change.clicked.connect(self.handle_change)

        layout = QVBoxLayout()
        layout.addWidget(self.label_old)
        layout.addWidget(self.edit_old)
        layout.addWidget(self.label_new1)
        layout.addWidget(self.edit_new1)
        layout.addWidget(self.label_new2)
        layout.addWidget(self.edit_new2)
        layout.addWidget(self.btn_change)
        self.setLayout(layout)

    def handle_change(self):
        old_pass = self.edit_old.text().strip()
        new_pass1 = self.edit_new1.text().strip()
        new_pass2 = self.edit_new2.text().strip()

        if not old_pass or not new_pass1 or not new_pass2:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        if new_pass1 != new_pass2:
            QMessageBox.warning(self, "Ошибка", "Новые пароли не совпадают.")
            return

        success, msg = change_password(self.user_id, old_pass, new_pass1)
        if success:
            QMessageBox.information(self, "Успех", msg)
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", msg)
