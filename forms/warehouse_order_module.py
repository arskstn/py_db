from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
)
from database import get_connection

class WarehouseOrderForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Склад: Заказ")

        layout_main = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Номер заказа", "Дата", "Заказчик ID", "Сумма"])

        form_layout = QHBoxLayout()
        self.edit_order_num = QLineEdit()
        self.edit_date = QLineEdit()
        self.combo_client = QComboBox()
        self.edit_sum = QLineEdit()

        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Номер:"))
        form_layout.addWidget(self.edit_order_num)
        form_layout.addWidget(QLabel("Дата:"))
        form_layout.addWidget(self.edit_date)
        form_layout.addWidget(QLabel("Заказчик:"))
        form_layout.addWidget(self.combo_client)
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

        self.load_clients()
        self.load_data()

    def load_clients(self):
        self.combo_client.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Clients ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        for (client_id, client_name) in rows:
            self.combo_client.addItem(client_name, client_id)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, order_number, date, client_id, total_sum
            FROM WarehouseOrders
            ORDER BY id ASC
        """)
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, (oid, onum, odate, cid, tsum) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(oid)))
            self.table.setItem(i, 1, QTableWidgetItem(str(onum)))
            self.table.setItem(i, 2, QTableWidgetItem(str(odate)))
            self.table.setItem(i, 3, QTableWidgetItem(str(cid)))
            self.table.setItem(i, 4, QTableWidgetItem(str(tsum) if tsum else "0"))
        conn.close()

    def add_record(self):
        order_num = self.edit_order_num.text().strip()
        date_str = self.edit_date.text().strip()
        client_id = self.combo_client.currentData()
        sum_str = self.edit_sum.text().strip()

        if not order_num or not date_str or not sum_str:
            QMessageBox.warning(self, "Ошибка", "Введите номер, дату и сумму!")
            return
        try:
            total_sum_val = float(sum_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Сумма должна быть числом.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WarehouseOrders (order_number, date, client_id, total_sum)
            VALUES (?, ?, ?, ?)
        """, (order_num, date_str, client_id, total_sum_val))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return

        record_id = int(self.table.item(row, 0).text())
        order_num = self.edit_order_num.text().strip()
        date_str = self.edit_date.text().strip()
        client_id = self.combo_client.currentData()
        sum_str = self.edit_sum.text().strip()

        if not order_num or not date_str or not sum_str:
            QMessageBox.warning(self, "Ошибка", "Введите номер, дату и сумму!")
            return
        try:
            total_sum_val = float(sum_str)
        except:
            QMessageBox.warning(self, "Ошибка", "Сумма должна быть числом.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE WarehouseOrders
            SET order_number=?, date=?, client_id=?, total_sum=?
            WHERE id=?
        """, (order_num, date_str, client_id, total_sum_val, record_id))
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
        cursor.execute("DELETE FROM WarehouseOrders WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()
