from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QMessageBox, QCheckBox
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import QDate, Qt
from datetime import datetime, timedelta

class investments:
    def __init__(self, parent):
        self.parent = parent
        self.tabs = parent.tabs
        self.conn = parent.conn
    
    def create_investment_tracking_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Add Investment
        add_layout = QHBoxLayout()
        self.inv_name = QLineEdit()
        self.inv_amt = QLineEdit()
        self.inv_rate = QLineEdit()
        self.inv_date = QDateEdit()
        self.inv_date.setDate(QDate.currentDate())
        add_inv_btn = QPushButton("Add Investment")
        add_inv_btn.clicked.connect(self.add_investment)

        add_layout.addWidget(QLabel("Name:"))
        add_layout.addWidget(self.inv_name)
        add_layout.addWidget(QLabel("Initial Amount:"))
        add_layout.addWidget(self.inv_amt)
        add_layout.addWidget(QLabel("Rate (%):"))
        add_layout.addWidget(self.inv_rate)
        add_layout.addWidget(QLabel("Date:"))
        add_layout.addWidget(self.inv_date)
        add_layout.addWidget(add_inv_btn)
        layout.addLayout(add_layout)

        # Investments Table
        self.inv_table = QTableWidget()
        self.load_investments()
        layout.addWidget(self.inv_table)

        # Graph
        self.inv_figure = plt.figure()
        self.inv_canvas = FigureCanvas(self.inv_figure)
        layout.addWidget(self.inv_canvas)
        self.plot_investments()

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Investment Tracking")

    def add_investment(self):
        try:
            name = self.inv_name.text()
            amt = float(self.inv_amt.text())
            rate = float(self.inv_rate.text())
            date = self.inv_date.date().toString("yyyy-MM-dd")
            c = self.conn.cursor()
            c.execute("INSERT INTO investments (name, initial_amount, current_value, rate, date) VALUES (?, ?, ?, ?, ?)", (name, amt, amt, rate, date))
            self.conn.commit()
            self.load_investments()
            self.plot_investments()
            QMessageBox.information(self.parent, "Success", "Investment added!")
        except ValueError:
            QMessageBox.warning(self.parent, "Error", "Invalid input")

    def load_investments(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM investments")
        rows = c.fetchall()
        self.inv_table.setRowCount(len(rows))
        self.inv_table.setColumnCount(6)
        self.inv_table.setHorizontalHeaderLabels(["ID", "Name", "Initial", "Current", "Rate", "Date"])
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.inv_table.setItem(i, j, QTableWidgetItem(str(val)))

    def plot_investments(self):
        c = self.conn.cursor()
        c.execute("SELECT name, initial_amount, rate, date FROM investments")
        data = c.fetchall()
        self.inv_figure.clear()
        ax = self.inv_figure.add_subplot(111)
        for name, init, rate, date in data:
            years = (datetime.now() - datetime.strptime(date, "%Y-%m-%d")).days / 365
            projected = init * (1 + rate/100) ** years
            ax.plot([0, years], [init, projected], label=name)
        ax.set_title("Investment Growth")
        ax.legend()
        self.inv_canvas.draw()
