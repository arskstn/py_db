# forms/reference_units.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
from database import get_connection

class ReferenceUnitsForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочник: Учётные единицы (Units)")

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Название единицы"])

        self.edit_name = QLineEdit()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_print = QPushButton("Печать")

        layout_form = QHBoxLayout()
        layout_form.addWidget(QLabel("Название:"))
        layout_form.addWidget(self.edit_name)
        layout_form.addWidget(self.btn_add)
        layout_form.addWidget(self.btn_edit)
        layout_form.addWidget(self.btn_delete)
        layout_form.addWidget(self.btn_print)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.table)
        layout_main.addLayout(layout_form)
        self.setLayout(layout_main)

        self.load_data()

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_print.clicked.connect(self.print_data)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Units ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()

    def add_record(self):
        name = self.edit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название учётной единицы.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Units (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return

        record_id = int(self.table.item(current_row, 0).text())
        name = self.edit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название учётной единицы.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Units SET name = ? WHERE id = ?", (name, record_id))
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
        cursor.execute("DELETE FROM Units WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()

    def print_data(self):
        QMessageBox.information(self, "Печать", "Здесь могла бы быть ваша печать списка учётных единиц...")
