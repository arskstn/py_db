from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
from database import get_connection

class ReferenceCountriesForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочник: Страны")

        layout_main = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Код"])

        # Форма для добавления/редактирования
        form_layout = QHBoxLayout()
        self.edit_name = QLineEdit()
        self.edit_code = QLineEdit()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.edit_name)
        form_layout.addWidget(QLabel("Код:"))
        form_layout.addWidget(self.edit_code)
        form_layout.addWidget(self.btn_add)
        form_layout.addWidget(self.btn_edit)
        form_layout.addWidget(self.btn_delete)

        layout_main.addWidget(self.table)
        layout_main.addLayout(form_layout)

        self.setLayout(layout_main)

        self.load_data()

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, code FROM Countries ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, (cid, cname, ccode) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(cid)))
            self.table.setItem(i, 1, QTableWidgetItem(cname))
            self.table.setItem(i, 2, QTableWidgetItem(str(ccode) if ccode else ""))
        conn.close()

    def add_record(self):
        name = self.edit_name.text().strip()
        code = self.edit_code.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название страны")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Countries (name, code) VALUES (?, ?)", (name, code))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
            return
        record_id = int(self.table.item(row, 0).text())
        name = self.edit_name.text().strip()
        code = self.edit_code.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название страны")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Countries SET name=?, code=? WHERE id=?", (name, code, record_id))
        conn.commit()
        conn.close()
        self.load_data()

    def delete_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return
        record_id = int(self.table.item(row, 0).text())

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Countries WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()
