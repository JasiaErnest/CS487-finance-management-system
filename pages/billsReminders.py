from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QMessageBox, QCheckBox
)
from PyQt6.QtCore import QDate
    
class bills_reminders:
    def __init__(self, parent):
        self.parent = parent
        self.tabs = parent.tabs
        self.conn = parent.conn
    
    def create_bills_reminders_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Add Bill
        add_layout = QHBoxLayout()
        self.bill_name = QLineEdit()
        self.bill_amt = QLineEdit()
        self.bill_date = QDateEdit()
        self.bill_date.setDate(QDate.currentDate())
        self.auto_deduct = QCheckBox("Auto Deduct")
        add_bill_btn = QPushButton("Add Bill")
        add_bill_btn.clicked.connect(self.add_bill)

        add_layout.addWidget(QLabel("Name:"))
        add_layout.addWidget(self.bill_name)
        add_layout.addWidget(QLabel("Amount:"))
        add_layout.addWidget(self.bill_amt)
        add_layout.addWidget(QLabel("Due Date:"))
        add_layout.addWidget(self.bill_date)
        add_layout.addWidget(self.auto_deduct)
        add_layout.addWidget(add_bill_btn)
        layout.addLayout(add_layout)

        # Bills Table
        self.bills_table = QTableWidget()
        self.load_bills()
        layout.addWidget(self.bills_table)

        # Reminders
        self.reminder_label = QLabel()
        layout.addWidget(self.reminder_label)
        self.check_reminders()

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Bills & Reminders")

    def add_bill(self):
        try:
            name = self.bill_name.text()
            amt = float(self.bill_amt.text())
            date = self.bill_date.date().toString("yyyy-MM-dd")
            auto = 1 if self.auto_deduct.isChecked() else 0
            c = self.conn.cursor()
            c.execute("INSERT INTO bills (name, amount, due_date, auto_deduct) VALUES (?, ?, ?, ?)", (name, amt, date, auto))
            self.conn.commit()
            self.load_bills()
            self.check_reminders()
            QMessageBox.information(self.parent, "Success", "Bill added!")
        except ValueError:
            QMessageBox.warning(self.parent, "Error", "Invalid amount")

    def load_bills(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM bills")
        rows = c.fetchall()
        self.bills_table.setRowCount(len(rows))
        self.bills_table.setColumnCount(5)
        self.bills_table.setHorizontalHeaderLabels(["ID", "Name", "Amount", "Due Date", "Auto Deduct"])
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.bills_table.setItem(i, j, QTableWidgetItem(str(val)))

    def check_reminders(self):
        c = self.conn.cursor()
        c.execute("SELECT name, amount, due_date FROM bills WHERE date(due_date) <= date('now', '+7 days')")
        bills = c.fetchall()
        text = "Upcoming Bills:\n"
        for bill in bills:
            text += f"{bill[0]}: {bill[1]} due {bill[2]}\n"
        self.reminder_label.setText(text)