from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class HelpContentForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка: Содержание")

        layout = QVBoxLayout()
        label = QLabel("Оглавление справочной системы:")
        text = QTextEdit()
        text.setReadOnly(True)
        text.setText("Здесь может быть подробное оглавление справки...\n1. Введение\n2. Как работать...\nи т.д.")
        layout.addWidget(label)
        layout.addWidget(text)
        self.setLayout(layout)
