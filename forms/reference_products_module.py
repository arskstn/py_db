from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
from database import get_connection

class ReferenceProductsForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочник: Товары")

        layout_main = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Описание"])

        form_layout = QHBoxLayout()
        self.edit_name = QLineEdit()
        self.edit_desc = QLineEdit()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.edit_name)
        form_layout.addWidget(QLabel("Описание:"))
        form_layout.addWidget(self.edit_desc)
        form_layout.addWidget(self.btn_add)
        form_layout.addWidget(self.btn_edit)
        form_layout.addWidget(self.btn_delete)

        layout_main.addWidget(self.table)
        layout_main.addLayout(form_layout)
        self.setLayout(layout_main)

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM Products ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, (pid, pname, pdesc) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(i, 1, QTableWidgetItem(pname))
            self.table.setItem(i, 2, QTableWidgetItem(pdesc or ""))
        conn.close()

    def add_record(self):
        name = self.edit_name.text().strip()
        desc = self.edit_desc.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название товара.")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (name, description) VALUES (?, ?)", (name, desc))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return
        record_id = int(self.table.item(row, 0).text())
        name = self.edit_name.text().strip()
        desc = self.edit_desc.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название товара.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Products SET name=?, description=? WHERE id=?", (name, desc, record_id))
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
        cursor.execute("DELETE FROM Products WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()
