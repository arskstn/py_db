# forms/about_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Эксперимент - Пример приложения на Python + PyQt5.\nАвтор: Вася Пупкин.\nВерсия 1.0."))
        self.setLayout(layout)
