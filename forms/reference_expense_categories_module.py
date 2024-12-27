from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
from database import get_connection

class ReferenceExpenseCategoriesForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочник: Категории расходов")

        layout_main = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Название категории"])

        form_layout = QHBoxLayout()
        self.edit_name = QLineEdit()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.edit_name)
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
        cursor.execute("SELECT id, name FROM ExpenseCategories ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, (ecid, ecname) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(ecid)))
            self.table.setItem(i, 1, QTableWidgetItem(ecname))
        conn.close()

    def add_record(self):
        name = self.edit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название категории.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ExpenseCategories (name) VALUES (?)", (name,))
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
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название категории.")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ExpenseCategories SET name=? WHERE id=?", (name, record_id))
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
        cursor.execute("DELETE FROM ExpenseCategories WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()
