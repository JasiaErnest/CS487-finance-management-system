from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QMessageBox, QCheckBox
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from datetime import datetime, timedelta

class investments:
    def __init__(self, parent):
        self.parent = parent
        self.conn = parent.conn
        self.widget = None
    
    def get_widget(self):
        """Return the investment tracking widget"""
        return self.widget
    
    def create_investment_tracking_tab(self):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #f9f9f9;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Header
        title = QLabel("Investments")
        title.setStyleSheet("color: #31572c; font-family: Helvetica; font-size: 24px; font-weight: 600;")
        
        subtitle = QLabel("Manage your investment portfolio")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666666;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Add Investment
        add_layout = QHBoxLayout()
        self.inv_name = QLineEdit()
        self.inv_amt = QLineEdit()
        self.inv_rate = QLineEdit()
        self.inv_date = QDateEdit()
        self.inv_date.setDate(QDate.currentDate())
        add_inv_btn = QPushButton("+ Add Investment")
        add_inv_btn.clicked.connect(self.add_investment)

        name = QLabel("Name:")
        name.setStyleSheet("color: #666666; font-family: 'Cantarell'; font-size: 14px; font-weight: 500;")
        add_layout.addWidget(name)
        add_layout.addWidget(self.inv_name)
        initial_amount = QLabel("Initial Amount:")
        initial_amount.setStyleSheet("color: #666666; font-family: 'Cantarell'; font-size: 14px; font-weight: 500;")
        add_layout.addWidget(initial_amount)
        add_layout.addWidget(self.inv_amt)
        rate = QLabel("Rate (%):")
        rate.setStyleSheet("color: #666666; font-family: 'Cantarell'; font-size: 14px; font-weight: 500;")
        add_layout.addWidget(rate)
        add_layout.addWidget(self.inv_rate)
        date_label = QLabel("Date:")
        date_label.setStyleSheet("color: #666666; font-family: 'Cantarell'; font-size: 14px; font-weight: 500;")
        add_layout.addWidget(date_label)
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

        self.widget.setLayout(layout)

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
