# forms/settings_form.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class SettingsForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройка")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Здесь настройки приложения (пример)."))
        layout.addWidget(QPushButton("Сохранить настройки"))
        self.setLayout(layout)
