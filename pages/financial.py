from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QMessageBox, QCheckBox
)
from PyQt6.QtCore import QDate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import QDate, Qt

class financial:
    def __init__(self, parent):
        self.parent = parent
        self.tabs = parent.tabs
        self.conn = parent.conn

    def create_financial_tracking_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Add Transaction
        add_layout = QHBoxLayout()
        self.trans_type = QComboBox()
        self.trans_type.addItems(["Income", "Expense"])
        self.amount_edit = QLineEdit()
        self.category_edit = QLineEdit()
        self.desc_edit = QLineEdit()
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        add_btn = QPushButton("Add Transaction")
        add_btn.clicked.connect(self.add_transaction)

        add_layout.addWidget(QLabel("Type:"))
        add_layout.addWidget(self.trans_type)
        add_layout.addWidget(QLabel("Amount:"))
        add_layout.addWidget(self.amount_edit)
        add_layout.addWidget(QLabel("Category:"))
        add_layout.addWidget(self.category_edit)
        add_layout.addWidget(QLabel("Description:"))
        add_layout.addWidget(self.desc_edit)
        add_layout.addWidget(QLabel("Date:"))
        add_layout.addWidget(self.date_edit)
        add_layout.addWidget(add_btn)

        layout.addLayout(add_layout)

        # Transactions Table
        self.trans_table = QTableWidget()
        self.load_transactions()
        layout.addWidget(self.trans_table)

        # Edit/Delete
        edit_layout = QHBoxLayout()
        self.edit_id = QLineEdit()
        edit_btn = QPushButton("Edit Selected")
        delete_btn = QPushButton("Delete Selected")
        edit_btn.clicked.connect(self.edit_transaction)
        delete_btn.clicked.connect(self.delete_transaction)

        edit_layout.addWidget(QLabel("ID to edit/delete:"))
        edit_layout.addWidget(self.edit_id)
        edit_layout.addWidget(edit_btn)
        edit_layout.addWidget(delete_btn)
        layout.addLayout(edit_layout)

        # Trends
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.plot_trends()

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Financial Tracking")

    def add_transaction(self):
        try:
            trans_type = self.trans_type.currentText()
            amount = float(self.amount_edit.text())
            category = self.category_edit.text()
            desc = self.desc_edit.text()
            date = self.date_edit.date().toString("yyyy-MM-dd")

            c = self.conn.cursor()
            c.execute("INSERT INTO transactions (type, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
                      (trans_type, amount, category, desc, date))
            self.conn.commit()
            self.load_transactions()
            self.plot_trends()
            QMessageBox.information(self.parent, "Success", "Transaction added!")
        except ValueError:
            QMessageBox.warning(self.parent, "Error", "Invalid amount")

    def load_transactions(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM transactions")
        rows = c.fetchall()
        self.trans_table.setRowCount(len(rows))
        self.trans_table.setColumnCount(6)
        self.trans_table.setHorizontalHeaderLabels(["ID", "Type", "Amount", "Category", "Description", "Date"])
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.trans_table.setItem(i, j, QTableWidgetItem(str(val)))

    def edit_transaction(self):
        # For simplicity, not implemented fully
        QMessageBox.information(self.parent, "Info", "Edit not implemented")

    def delete_transaction(self):
        try:
            id_ = int(self.edit_id.text())
            c = self.conn.cursor()
            c.execute("DELETE FROM transactions WHERE id = ?", (id_,))
            self.conn.commit()
            self.load_transactions()
            self.plot_trends()
            QMessageBox.information(self.parent, "Success", "Deleted!")
        except:
            QMessageBox.warning(self.parent, "Error", "Invalid ID")

    def plot_trends(self):
        c = self.conn.cursor()
        c.execute("SELECT date, amount FROM transactions WHERE type='Expense' ORDER BY date")
        data = c.fetchall()
        if data:
            dates = [row[0] for row in data]
            amounts = [row[1] for row in data]
            self.figure.clear()
            plt.plot(dates, amounts)
            plt.title("Expense Trends")
            self.canvas.draw()