# login.py
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox)
from user_management import register_user, login_user

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.user_data = None
        self.init_ui()

    def init_ui(self):
        self.label_username = QLabel("Логин:")
        self.label_password = QLabel("Пароль:")
        self.edit_username = QLineEdit()
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)

        self.check_superuser = QCheckBox("Суперпользователь?")

        self.btn_login = QPushButton("Войти")
        self.btn_register = QPushButton("Регистрация")

        h_layout_username = QHBoxLayout()
        h_layout_username.addWidget(self.label_username)
        h_layout_username.addWidget(self.edit_username)

        h_layout_password = QHBoxLayout()
        h_layout_password.addWidget(self.label_password)
        h_layout_password.addWidget(self.edit_password)

        h_layout_buttons = QHBoxLayout()
        h_layout_buttons.addWidget(self.btn_login)
        h_layout_buttons.addWidget(self.btn_register)

        layout = QVBoxLayout()
        layout.addLayout(h_layout_username)
        layout.addLayout(h_layout_password)
        layout.addWidget(self.check_superuser)
        layout.addLayout(h_layout_buttons)

        self.setLayout(layout)

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register.clicked.connect(self.handle_register)

    def handle_login(self):
        username = self.edit_username.text().strip()
        password = self.edit_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        user_data, message = login_user(username, password)
        if user_data is None:
            QMessageBox.warning(self, "Ошибка входа", message)
        else:
            self.user_data = user_data
            self.accept()

    def handle_register(self):
        username = self.edit_username.text().strip()
        password = self.edit_password.text().strip()
        is_superuser = 1 if self.check_superuser.isChecked() else 0

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        success, message = register_user(username, password, is_superuser)
        if success:
            QMessageBox.information(self, "Успех", message)
        else:
            QMessageBox.warning(self, "Ошибка регистрации", message)
