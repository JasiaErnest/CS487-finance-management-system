import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QMessageBox, QCheckBox
)
from PyQt6.QtCore import QDate, Qt
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from pages.budget import budget
from pages.financial import financial
from pages.financialHealth import financialHealth
from pages.investments import investments
from pages.billsReminders import bills_reminders


class FinanceManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Management System")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize database
        self.init_database()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Instantiate and create tabs for each page
        financial_page = financial(self)
        financial_page.create_financial_tracking_tab()
        
        budget_page = budget(self)
        budget_page.create_budget_management_tab()
        
        bills_page = bills_reminders(self)
        bills_page.create_bills_reminders_tab()
        
        investments_page = investments(self)
        investments_page.create_investment_tracking_tab()
        
        health_page = financialHealth(self)
        health_page.create_financial_health_tab()

    def init_database(self):
        """Initialize SQLite database using schema.sql"""
        # Connect to database
        db_path = os.path.join(os.path.dirname(__file__), "backend", "finance.db")
        self.conn = sqlite3.connect(db_path)
        c = self.conn.cursor()

        try:
            # Read and execute schema
            schema_path = os.path.join(os.path.dirname(__file__), "backend", "schema.sql")
            with open(schema_path, 'r') as f:
                sql_script = f.read()
                c.executescript(sql_script)

            self.conn.commit()
            print("Database initialized successfully")
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            # If database is corrupted, recreate it
            self.conn.close()
            # Delete corrupted file and create new one
            if os.path.exists(db_path):
                os.remove(db_path)
            # Create fresh database
            self.conn = sqlite3.connect(db_path)
            c = self.conn.cursor()
            with open(schema_path, 'r') as f:
                sql_script = f.read()
                c.executescript(sql_script)
            self.conn.commit()
            print("Database recreated successfully")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceManagementSystem()
    window.show()
    sys.exit(app.exec())