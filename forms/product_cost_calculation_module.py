from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSlider, QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from database import get_connection

class ProductCostCalculationForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Расчёт стоимости товара")

        layout_main = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.combo_product = QComboBox()
        self.edit_price = QLineEdit()
        self.slider_quantity = QSlider(Qt.Horizontal)
        self.slider_quantity.setRange(1, 1000)  # например, максимум 1000
        self.slider_quantity.setValue(1)
        self.label_quantity = QLabel("1")
        self.label_result = QLabel("Итог: 0.0")

        top_layout.addWidget(QLabel("Товар:"))
        top_layout.addWidget(self.combo_product)
        top_layout.addWidget(QLabel("Цена за штуку:"))
        top_layout.addWidget(self.edit_price)

        layout_main.addLayout(top_layout)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Количество:"))
        slider_layout.addWidget(self.slider_quantity)
        slider_layout.addWidget(self.label_quantity)
        layout_main.addLayout(slider_layout)

        layout_main.addWidget(self.label_result)

        btn_calculate = QPushButton("Рассчитать")
        layout_main.addWidget(btn_calculate)

        self.setLayout(layout_main)

        self.load_products()

        self.slider_quantity.valueChanged.connect(self.on_slider_changed)
        btn_calculate.clicked.connect(self.on_calculate)

    def load_products(self):
        self.combo_product.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Products ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        for (pid, pname) in rows:
            self.combo_product.addItem(pname, pid)

    def on_slider_changed(self, value):
        self.label_quantity.setText(str(value))

    def on_calculate(self):
        price_str = self.edit_price.text().strip()
        qty = self.slider_quantity.value()

        if not price_str:
            QMessageBox.warning(self, "Ошибка", "Введите цену за штуку!")
            return
        try:
            price_val = float(price_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Цена за штуку должна быть числом.")
            return

        total = price_val * qty
        self.label_result.setText(f"Итог: {total:.2f}")
