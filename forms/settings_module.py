from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QColorDialog
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class SettingsForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки приложения")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Здесь можно сменить размер шрифта и цвет."))

        self.combo_font_size = QComboBox()
        for size in [8, 10, 12, 14, 16, 18, 20]:
            self.combo_font_size.addItem(str(size), size)
        layout.addWidget(QLabel("Размер шрифта:"))
        layout.addWidget(self.combo_font_size)

        self.btn_bg_color = QPushButton("Выбрать цвет фона")
        self.btn_bg_color.clicked.connect(self.choose_bg_color)
        layout.addWidget(self.btn_bg_color)

        self.btn_apply = QPushButton("Сохранить настройки")
        self.btn_apply.clicked.connect(self.apply_settings)
        layout.addWidget(self.btn_apply)

        self.setLayout(layout)

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_bg_color = color
        else:
            self.selected_bg_color = None

    def apply_settings(self):
        font_size = self.combo_font_size.currentData()
        new_font = QFont()
        new_font.setPointSize(font_size)
        self.setFont(new_font)

        if hasattr(self, "selected_bg_color") and self.selected_bg_color:
            pal = self.palette()
            pal.setColor(QPalette.Window, self.selected_bg_color)
            self.setAutoFillBackground(True)
            self.setPalette(pal)

