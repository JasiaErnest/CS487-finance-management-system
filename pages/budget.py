from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QMessageBox, QCheckBox
)

class budget:
    def __init__(self, parent):
        self.parent = parent
        self.tabs = parent.tabs
        self.conn = parent.conn

    def create_budget_management_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Set Budget
        set_layout = QHBoxLayout()
        self.budget_cat = QLineEdit()
        self.budget_amt = QLineEdit()
        self.budget_period = QComboBox()
        self.budget_period.addItems(["Monthly", "Yearly"])
        set_btn = QPushButton("Set Budget")
        set_btn.clicked.connect(self.set_budget)

        set_layout.addWidget(QLabel("Category:"))
        set_layout.addWidget(self.budget_cat)
        set_layout.addWidget(QLabel("Amount:"))
        set_layout.addWidget(self.budget_amt)
        set_layout.addWidget(QLabel("Period:"))
        set_layout.addWidget(self.budget_period)
        set_layout.addWidget(set_btn)
        layout.addLayout(set_layout)

        # Budgets Table
        self.budget_table = QTableWidget()
        self.load_budgets()
        layout.addWidget(self.budget_table)

        # Progress
        self.progress_label = QLabel()
        layout.addWidget(self.progress_label)
        self.update_progress()

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Budget Management")

    def set_budget(self):
        try:
            cat = self.budget_cat.text()
            amt = float(self.budget_amt.text())
            period = self.budget_period.currentText()
            c = self.conn.cursor()
            c.execute("INSERT OR REPLACE INTO budgets (category, amount, period) VALUES (?, ?, ?)", (cat, amt, period))
            self.conn.commit()
            self.load_budgets()
            self.update_progress()
            QMessageBox.information(self.parent, "Success", "Budget set!")
        except ValueError:
            QMessageBox.warning(self.parent, "Error", "Invalid amount")

    def load_budgets(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM budgets")
        rows = c.fetchall()
        self.budget_table.setRowCount(len(rows))
        self.budget_table.setColumnCount(4)
        self.budget_table.setHorizontalHeaderLabels(["ID", "Category", "Amount", "Period"])
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.budget_table.setItem(i, j, QTableWidgetItem(str(val)))

    def update_progress(self):
        c = self.conn.cursor()
        c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
        exp = dict(c.fetchall())
        c.execute("SELECT category, amount FROM budgets")
        budgets = c.fetchall()
        text = ""
        for cat, b_amt in budgets:
            e_amt = exp.get(cat, 0)
            progress = (e_amt / b_amt) * 100 if b_amt > 0 else 0
            text += f"{cat}: {e_amt:.2f}/{b_amt:.2f} ({progress:.1f}%)\n"
            if progress > 100:
                text += "Overspending!\n"
        self.progress_label.setText(text)
