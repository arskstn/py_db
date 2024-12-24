# forms/enterprise_expenses_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
from database import get_connection

class EnterpriseExpensesForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Финансовый учёт: Расходы предприятия")

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Дата", "КатегорияID", "Сумма"])

        self.edit_date = QLineEdit()
        self.combo_category = QComboBox()
        self.edit_amount = QLineEdit()

        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_view = QPushButton("Просмотр")

        layout_form = QHBoxLayout()
        layout_form.addWidget(QLabel("Дата:"))
        layout_form.addWidget(self.edit_date)
        layout_form.addWidget(QLabel("Категория:"))
        layout_form.addWidget(self.combo_category)
        layout_form.addWidget(QLabel("Сумма:"))
        layout_form.addWidget(self.edit_amount)
        layout_form.addWidget(self.btn_add)
        layout_form.addWidget(self.btn_edit)
        layout_form.addWidget(self.btn_delete)
        layout_form.addWidget(self.btn_view)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.table)
        layout_main.addLayout(layout_form)
        self.setLayout(layout_main)

        self.load_categories()
        self.load_data()

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_view.clicked.connect(self.view_expense)

    def load_categories(self):
        self.combo_category.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM ExpenseCategories ORDER BY name")
        rows = cursor.fetchall()
        for r in rows:
            cat_id, cat_name = r
            self.combo_category.addItem(cat_name, cat_id)
        conn.close()

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, expense_date, category_id, amount FROM EnterpriseExpenses ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()

    def add_record(self):
        date = self.edit_date.text().strip()
        category_id = self.combo_category.currentData()
        amount_str = self.edit_amount.text().strip()

        if not date or not amount_str:
            QMessageBox.warning(self, "Ошибка", "Введите дату и сумму расходов!")
            return

        try:
            amount = float(amount_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Некорректная сумма.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO EnterpriseExpenses (expense_date, category_id, amount)
            VALUES (?, ?, ?)
        """, (date, category_id, amount))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return
        record_id = int(self.table.item(current_row, 0).text())

        date = self.edit_date.text().strip()
        category_id = self.combo_category.currentData()
        amount_str = self.edit_amount.text().strip()

        if not date or not amount_str:
            QMessageBox.warning(self, "Ошибка", "Введите дату и сумму.")
            return

        try:
            amount = float(amount_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Некорректная сумма.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE EnterpriseExpenses
            SET expense_date = ?, category_id = ?, amount = ?
            WHERE id = ?
        """, (date, category_id, amount, record_id))
        conn.commit()
        conn.close()
        self.load_data()

    def delete_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return
        record_id = int(self.table.item(current_row, 0).text())

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM EnterpriseExpenses WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()

    def view_expense(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "Просмотр", "Выберите расход для просмотра.")
            return
        expense_id = int(self.table.item(current_row, 0).text())
        QMessageBox.information(self, "Просмотр", f"Здесь можно показать детальную информацию о расходе ID={expense_id}.")
