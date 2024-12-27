from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
)
from database import get_connection

class ReferenceSuppliersForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочник: Поставщики")

        layout_main = QVBoxLayout()

        self.table = QTableWidget()
        # Добавим колонки:
        # ID, name, country_id, bank_id, inn, address, zip_code, email
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "СтранаID", "БанкID",
            "ИНН", "Адрес", "Индекс", "Email"
        ])
        layout_main.addWidget(self.table)

        form_layout = QHBoxLayout()

        self.edit_name = QLineEdit()
        self.combo_country = QComboBox()  # для country_id
        self.combo_bank = QComboBox()     # для bank_id
        self.edit_inn = QLineEdit()
        self.edit_address = QLineEdit()
        self.edit_zip = QLineEdit()
        self.edit_email = QLineEdit()

        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.edit_name)

        form_layout.addWidget(QLabel("Страна:"))
        form_layout.addWidget(self.combo_country)

        form_layout.addWidget(QLabel("Банк:"))
        form_layout.addWidget(self.combo_bank)

        form_layout.addWidget(QLabel("ИНН:"))
        form_layout.addWidget(self.edit_inn)

        # Можно вынести в другую строку, если слишком тесно
        form_layout2 = QHBoxLayout()
        form_layout2.addWidget(QLabel("Адрес:"))
        form_layout2.addWidget(self.edit_address)
        form_layout2.addWidget(QLabel("Индекс:"))
        form_layout2.addWidget(self.edit_zip)
        form_layout2.addWidget(QLabel("Email:"))
        form_layout2.addWidget(self.edit_email)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.btn_add)
        layout_buttons.addWidget(self.btn_edit)
        layout_buttons.addWidget(self.btn_delete)

        layout_main.addLayout(form_layout)
        layout_main.addLayout(form_layout2)
        layout_main.addLayout(layout_buttons)
        self.setLayout(layout_main)

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        self.load_countries()
        self.load_banks()
        self.load_data()

    def load_countries(self):
        self.combo_country.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Countries ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        for (cid, cname) in rows:
            self.combo_country.addItem(cname, cid)

    def load_banks(self):
        self.combo_bank.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Banks ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        for (bid, bname) in rows:
            self.combo_bank.addItem(bname, bid)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        # Получаем все поля
        cursor.execute("""
            SELECT id, name, country_id, bank_id, inn, address, zip_code, email
            FROM Suppliers
            ORDER BY id ASC
        """)
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val) if val else "")
                self.table.setItem(i, j, item)
        conn.close()

    def add_record(self):
        name = self.edit_name.text().strip()
        country_id = self.combo_country.currentData()
        bank_id = self.combo_bank.currentData()
        inn = self.edit_inn.text().strip()
        address = self.edit_address.text().strip()
        zip_code = self.edit_zip.text().strip()
        email = self.edit_email.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название поставщика!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Suppliers (name, country_id, bank_id, inn, address, zip_code, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, country_id, bank_id, inn, address, zip_code, email))
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
        country_id = self.combo_country.currentData()
        bank_id = self.combo_bank.currentData()
        inn = self.edit_inn.text().strip()
        address = self.edit_address.text().strip()
        zip_code = self.edit_zip.text().strip()
        email = self.edit_email.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название поставщика!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Suppliers
            SET name=?, country_id=?, bank_id=?, inn=?, address=?, zip_code=?, email=?
            WHERE id=?
        """, (name, country_id, bank_id, inn, address, zip_code, email, record_id))
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
        cursor.execute("DELETE FROM Suppliers WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data()
