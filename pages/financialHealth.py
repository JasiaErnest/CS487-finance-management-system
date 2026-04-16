from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QMessageBox, QCheckBox
)

class financialHealth:
    def __init__(self, parent):
        self.parent = parent
        self.conn = parent.conn
        self.widget = None
    
    def get_widget(self):
        """Return the financial health widget"""
        return self.widget
    
    def create_financial_health_tab(self):
        self.widget = QWidget()
        layout = QVBoxLayout()

        self.health_label = QLabel()
        layout.addWidget(self.health_label)
        self.update_health()

        # Insights
        self.insights_text = QTextEdit()
        layout.addWidget(self.insights_text)
        self.update_insights()

        self.widget.setLayout(layout)

    def update_health(self):
        c = self.conn.cursor()
        c.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
        expenses = c.fetchone()[0] or 0
        savings_rate = (income - expenses) / income if income > 0 else 0

        score = 30  # base
        if savings_rate > 0.2: score += 40
        elif savings_rate > 0.1: score += 20

        c.execute("SELECT category, amount FROM budgets")
        budgets = c.fetchall()
        overspend = 0
        for cat, amt in budgets:
            c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense' AND category=?", (cat,))
            exp = c.fetchone()[0] or 0
            if exp > amt: overspend += 1
        if overspend == 0: score += 30
        elif overspend < len(budgets)/2: score += 15

        self.health_label.setText(f"Financial Health Score: {score}/100")

    def update_insights(self):
        c = self.conn.cursor()
        c.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
        expenses = c.fetchone()[0] or 0
        #text = f"Total Income: {income:.2f}\nTotal Expenses: {expenses:.2f}\nSavings Rate: {(income-expenses)/income:.1%} if income else 'N/A'\n"
        #self.insights_text.setTextplt.textt)