from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
)
from database import get_connection

class WarehouseInvoiceForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Склад: Накладная")

        layout_main = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Номер", "Дата", "Поставщик ID", "Сумма"])

        form_layout = QHBoxLayout()
        self.edit_invoice_num = QLineEdit()
        self.edit_date = QLineEdit()
        self.combo_supplier = QComboBox()
        self.edit_sum = QLineEdit()

        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Номер:"))
        form_layout.addWidget(self.edit_invoice_num)
        form_layout.addWidget(QLabel("Дата:"))
        form_layout.addWidget(self.edit_date)
        form_layout.addWidget(QLabel("Поставщик:"))
        form_layout.addWidget(self.combo_supplier)
        form_layout.addWidget(QLabel("Сумма:"))
        form_layout.addWidget(self.edit_sum)

        form_layout.addWidget(self.btn_add)
        form_layout.addWidget(self.btn_edit)
        form_layout.addWidget(self.btn_delete)

        layout_main.addWidget(self.table)
        layout_main.addLayout(form_layout)
        self.setLayout(layout_main)

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        self.load_suppliers()
        self.load_data()

    def load_suppliers(self):
        self.combo_supplier.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Suppliers ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        for (sup_id, sup_name) in rows:
            self.combo_supplier.addItem(sup_name, sup_id)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, invoice_number, date, supplier_id, total_sum
            FROM WarehouseInvoices
            ORDER BY id ASC
        """)
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, (inv_id, inv_num, inv_date, sup_id, t_sum) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(inv_id)))
            self.table.setItem(i, 1, QTableWidgetItem(str(inv_num)))
            self.table.setItem(i, 2, QTableWidgetItem(str(inv_date)))
            self.table.setItem(i, 3, QTableWidgetItem(str(sup_id)))
            self.table.setItem(i, 4, QTableWidgetItem(str(t_sum) if t_sum else "0"))
        conn.close()

    def add_record(self):
        invoice_num = self.edit_invoice_num.text().strip()
        date_str = self.edit_date.text().strip()
        supplier_id = self.combo_supplier.currentData()
        sum_str = self.edit_sum.text().strip()

        if not invoice_num or not date_str or not sum_str:
            QMessageBox.warning(self, "Ошибка", "Заполните номер, дату и сумму!")
            return
        try:
            total_sum_val = float(sum_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Сумма должна быть числом.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WarehouseInvoices (invoice_number, date, supplier_id, total_sum)
            VALUES (?, ?, ?, ?)
        """, (invoice_num, date_str, supplier_id, total_sum_val))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return

        record_id = int(self.table.item(row, 0).text())
        invoice_num = self.edit_invoice_num.text().strip()
        date_str = self.edit_date.text().strip()
        supplier_id = self.combo_supplier.currentData()
        sum_str = self.edit_sum.text().strip()

        if not invoice_num or not date_str or not sum_str:
            QMessageBox.warning(self, "Ошибка", "Заполните номер, дату и сумму!")
            return
        try:
            total_sum_val = float(sum_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Сумма должна быть числом.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE WarehouseInvoices
            SET invoice_number=?, date=?, supplier_id=?, total_sum=?
            WHERE id=?
        """, (invoice_num, date_str, supplier_id, total_sum_val, record_id))
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
        cursor.execute("DELETE FROM WarehouseInvoices WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()
