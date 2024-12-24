# forms/product_cost_calculation_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
from database import get_connection
import datetime

class ProductCostCalculationForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Финансовый учёт: Расчёт стоимости товара")

        self.combo_product = QComboBox()
        self.btn_calculate = QPushButton("Рассчитать стоимость на ед.")
        self.table_results = QTableWidget()
        self.table_results.setColumnCount(3)
        self.table_results.setHorizontalHeaderLabels(["ID", "Товар", "Стоимость/ед."])

        layout_top = QHBoxLayout()
        layout_top.addWidget(QLabel("Выберите товар:"))
        layout_top.addWidget(self.combo_product)
        layout_top.addWidget(self.btn_calculate)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_top)
        layout_main.addWidget(self.table_results)
        self.setLayout(layout_main)

        self.load_products()
        self.load_existing_calculations()

        self.btn_calculate.clicked.connect(self.calculate_cost)

    def load_products(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Products ORDER BY name")
        rows = cursor.fetchall()
        conn.close()

        self.combo_product.clear()
        for r in rows:
            prod_id, prod_name = r
            self.combo_product.addItem(prod_name, prod_id)

    def load_existing_calculations(self):
        """
        Показывает ранее сохранённые результаты расчёта.
        """
        self.table_results.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT pcc.id, p.name, pcc.cost_per_unit
            FROM ProductCostCalculation pcc
            JOIN Products p ON p.id = pcc.product_id
            ORDER BY pcc.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        self.table_results.setRowCount(len(rows))
        for i, (calc_id, prod_name, cost) in enumerate(rows):
            self.table_results.setItem(i, 0, QTableWidgetItem(str(calc_id)))
            self.table_results.setItem(i, 1, QTableWidgetItem(prod_name))
            self.table_results.setItem(i, 2, QTableWidgetItem(str(cost)))
        conn.close()

    def calculate_cost(self):
        """
        Условная логика расчёта стоимости для товара.
        Допустим, просто случайно генерируем или ставим фиксированное значение.
        """
        product_id = self.combo_product.currentData()
        if not product_id:
            QMessageBox.warning(self, "Ошибка", "Выберите товар.")
            return

        # Допустим, на основе каких-то данных вычисляем себестоимость = 100.5
        # (в реальности надо бы анализировать расходы, закупки и т.д.)
        cost_per_unit = 100.5

        # Сохраним в таблицу
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ProductCostCalculation (product_id, cost_per_unit, calc_date)
            VALUES (?, ?, ?)
        """, (product_id, cost_per_unit, datetime.date.today().isoformat()))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Результат", f"Себестоимость/ед. для товара ID={product_id} = {cost_per_unit}")
        self.load_existing_calculations()
