# forms/doc_invoices_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
from database import get_connection

class DocInvoicesForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Документы: Накладные")

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Doc ID", "Invoice ID"])

        self.btn_export_word = QPushButton("Вывод в MS Word")

        layout_top = QHBoxLayout()
        layout_top.addWidget(self.btn_export_word)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.table)
        layout_main.addLayout(layout_top)
        self.setLayout(layout_main)

        self.load_data()
        self.btn_export_word.clicked.connect(self.export_to_word)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, invoice_id FROM DocInvoices ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()

    def export_to_word(self):
        QMessageBox.information(self, "Экспорт", "Здесь будет экспорт накладных в MS Word.")
