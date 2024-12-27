from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
)
from database import get_connection

class EnterpriseExpensesForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Финансовый учёт: Расходы предприятия")

        layout_main = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Дата", "Категория", "Сумма"])

        form_layout = QHBoxLayout()
        self.edit_date = QLineEdit()
        self.combo_category = QComboBox()
        self.edit_amount = QLineEdit()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Дата (yyyy-mm-dd):"))
        form_layout.addWidget(self.edit_date)
        form_layout.addWidget(QLabel("Категория:"))
        form_layout.addWidget(self.combo_category)
        form_layout.addWidget(QLabel("Сумма:"))
        form_layout.addWidget(self.edit_amount)
        form_layout.addWidget(self.btn_add)
        form_layout.addWidget(self.btn_edit)
        form_layout.addWidget(self.btn_delete)

        layout_main.addWidget(self.table)
        layout_main.addLayout(form_layout)
        self.setLayout(layout_main)

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        self.load_categories()
        self.load_data()

    def load_categories(self):
        self.combo_category.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM ExpenseCategories ORDER BY name")
        rows = cursor.fetchall()
        conn.close()

        for (cat_id, cat_name) in rows:
            self.combo_category.addItem(cat_name, cat_id)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, expense_date, category_id, amount FROM EnterpriseExpenses ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, (eid, edate, cat_id, amount) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(eid)))
            self.table.setItem(i, 1, QTableWidgetItem(edate))
            self.table.setItem(i, 2, QTableWidgetItem(str(cat_id)))
            self.table.setItem(i, 3, QTableWidgetItem(str(amount)))
        conn.close()

    def add_record(self):
        date_str = self.edit_date.text().strip()
        cat_id = self.combo_category.currentData()
        amount_str = self.edit_amount.text().strip()

        if not date_str or not amount_str:
            QMessageBox.warning(self, "Ошибка", "Введите дату и сумму!")
            return
        try:
            amount_val = float(amount_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Сумма должна быть числом!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO EnterpriseExpenses (expense_date, category_id, amount)
            VALUES (?, ?, ?)
        """, (date_str, cat_id, amount_val))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return
        record_id = int(self.table.item(row, 0).text())

        date_str = self.edit_date.text().strip()
        cat_id = self.combo_category.currentData()
        amount_str = self.edit_amount.text().strip()
        if not date_str or not amount_str:
            QMessageBox.warning(self, "Ошибка", "Введите дату и сумму!")
            return
        try:
            amount_val = float(amount_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Сумма должна быть числом!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE EnterpriseExpenses
            SET expense_date=?, category_id=?, amount=?
            WHERE id=?
        """, (date_str, cat_id, amount_val, record_id))
        conn.commit()
        conn.close()
        self.load_data()

    def delete_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return
        record_id = int(self.table.item(row, 0).text())

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM EnterpriseExpenses WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()