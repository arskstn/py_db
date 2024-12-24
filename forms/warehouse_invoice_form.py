# forms/warehouse_invoice_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
from database import get_connection

class WarehouseInvoiceForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Склад: Накладная")

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Номер накладной", "Дата", "Поставщик ID"])

        self.edit_invoice_num = QLineEdit()
        self.edit_date = QLineEdit()
        self.combo_supplier = QComboBox()  # Выбор поставщика

        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_view = QPushButton("Просмотр")

        layout_form = QHBoxLayout()
        layout_form.addWidget(QLabel("Номер:"))
        layout_form.addWidget(self.edit_invoice_num)
        layout_form.addWidget(QLabel("Дата:"))
        layout_form.addWidget(self.edit_date)
        layout_form.addWidget(QLabel("Поставщик:"))
        layout_form.addWidget(self.combo_supplier)
        layout_form.addWidget(self.btn_add)
        layout_form.addWidget(self.btn_edit)
        layout_form.addWidget(self.btn_delete)
        layout_form.addWidget(self.btn_view)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.table)
        layout_main.addLayout(layout_form)
        self.setLayout(layout_main)

        self.load_suppliers()
        self.load_data()

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_view.clicked.connect(self.view_invoice)

    def load_suppliers(self):
        self.combo_supplier.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Suppliers ORDER BY name")
        rows = cursor.fetchall()
        for r in rows:
            supplier_id, supplier_name = r
            self.combo_supplier.addItem(supplier_name, supplier_id)
        conn.close()

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, invoice_number, date, supplier_id FROM WarehouseInvoices ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()

    def add_record(self):
        invoice_num = self.edit_invoice_num.text().strip()
        date = self.edit_date.text().strip()
        supplier_id = self.combo_supplier.currentData()

        if not invoice_num or not date:
            QMessageBox.warning(self, "Ошибка", "Введите номер и дату накладной!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WarehouseInvoices (invoice_number, date, supplier_id)
            VALUES (?, ?, ?)
        """, (invoice_num, date, supplier_id))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return
        record_id = int(self.table.item(current_row, 0).text())

        invoice_num = self.edit_invoice_num.text().strip()
        date = self.edit_date.text().strip()
        supplier_id = self.combo_supplier.currentData()

        if not invoice_num or not date:
            QMessageBox.warning(self, "Ошибка", "Введите номер и дату накладной!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE WarehouseInvoices
            SET invoice_number = ?, date = ?, supplier_id = ?
            WHERE id = ?
        """, (invoice_num, date, supplier_id, record_id))
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
        cursor.execute("DELETE FROM WarehouseInvoices WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()

    def view_invoice(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "Просмотр", "Выберите накладную для просмотра.")
            return
        invoice_id = int(self.table.item(current_row, 0).text())
        # Здесь можно открыть отдельное окно просмотра накладной
        QMessageBox.information(self, "Просмотр накладной", f"Здесь можно показать детальную информацию о накладной ID={invoice_id}.")
