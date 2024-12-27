# forms/about_module.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class AboutForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Финансовый учет.\nАвтор: Елена Жукова.\nВерсия 1.0."))
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        self.setLayout(layout)
