from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
from database import get_connection

class ReferenceBanksForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочник: Банки")

        layout_main = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "SWIFT"])

        form_layout = QHBoxLayout()
        self.edit_name = QLineEdit()
        self.edit_swift = QLineEdit()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.edit_name)
        form_layout.addWidget(QLabel("SWIFT:"))
        form_layout.addWidget(self.edit_swift)
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
        cursor.execute("SELECT id, name, swift_code FROM Banks ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, (bid, bname, swift) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(bid)))
            self.table.setItem(i, 1, QTableWidgetItem(bname))
            self.table.setItem(i, 2, QTableWidgetItem(swift or ""))
        conn.close()

    def add_record(self):
        name = self.edit_name.text().strip()
        swift = self.edit_swift.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название банка.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Banks (name, swift_code) VALUES (?, ?)", (name, swift))
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
        swift = self.edit_swift.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название банка.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Banks SET name=?, swift_code=? WHERE id=?", (name, swift, record_id))
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
        cursor.execute("DELETE FROM Banks WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()
