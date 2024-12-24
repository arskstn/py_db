# forms/warehouse_order_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
from database import get_connection

class WarehouseOrderForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Склад: Заказ")

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Номер заказа", "Дата", "Заказчик ID"])

        self.edit_order_num = QLineEdit()
        self.edit_date = QLineEdit()
        self.combo_client = QComboBox()

        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_view = QPushButton("Просмотр")

        layout_form = QHBoxLayout()
        layout_form.addWidget(QLabel("Номер:"))
        layout_form.addWidget(self.edit_order_num)
        layout_form.addWidget(QLabel("Дата:"))
        layout_form.addWidget(self.edit_date)
        layout_form.addWidget(QLabel("Заказчик:"))
        layout_form.addWidget(self.combo_client)
        layout_form.addWidget(self.btn_add)
        layout_form.addWidget(self.btn_edit)
        layout_form.addWidget(self.btn_delete)
        layout_form.addWidget(self.btn_view)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.table)
        layout_main.addLayout(layout_form)
        self.setLayout(layout_main)

        self.load_clients()
        self.load_data()

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_view.clicked.connect(self.view_order)

    def load_clients(self):
        self.combo_client.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Clients ORDER BY name")
        rows = cursor.fetchall()
        for r in rows:
            client_id, client_name = r
            self.combo_client.addItem(client_name, client_id)
        conn.close()

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, order_number, date, client_id FROM WarehouseOrders ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()

    def add_record(self):
        order_num = self.edit_order_num.text().strip()
        date = self.edit_date.text().strip()
        client_id = self.combo_client.currentData()

        if not order_num or not date:
            QMessageBox.warning(self, "Ошибка", "Введите номер и дату заказа!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WarehouseOrders (order_number, date, client_id)
            VALUES (?, ?, ?)
        """, (order_num, date, client_id))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return
        record_id = int(self.table.item(current_row, 0).text())

        order_num = self.edit_order_num.text().strip()
        date = self.edit_date.text().strip()
        client_id = self.combo_client.currentData()

        if not order_num or not date:
            QMessageBox.warning(self, "Ошибка", "Введите номер и дату заказа!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE WarehouseOrders
            SET order_number = ?, date = ?, client_id = ?
            WHERE id = ?
        """, (order_num, date, client_id, record_id))
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
        cursor.execute("DELETE FROM WarehouseOrders WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()

    def view_order(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "Просмотр", "Выберите заказ для просмотра.")
            return
        order_id = int(self.table.item(current_row, 0).text())
        QMessageBox.information(self, "Просмотр заказа", f"Здесь можно показать детальную информацию о заказе ID={order_id}.")
