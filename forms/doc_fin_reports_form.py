# forms/doc_fin_reports_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
from database import get_connection

class DocFinReportsForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Документы: Финансовая отчётность")

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Doc ID", "Название отчёта", "Дата"])

        self.btn_export_excel = QPushButton("Вывод в MS Excel")

        layout_top = QHBoxLayout()
        layout_top.addWidget(self.btn_export_excel)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.table)
        layout_main.addLayout(layout_top)
        self.setLayout(layout_main)

        self.load_data()
        self.btn_export_excel.clicked.connect(self.export_to_excel)

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, report_name, report_date FROM DocFinReports ORDER BY id ASC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()

    def export_to_excel(self):
        QMessageBox.information(self, "Экспорт", "Здесь будет экспорт фин. отчётности в MS Excel.")
