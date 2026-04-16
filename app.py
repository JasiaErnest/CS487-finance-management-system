import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QScrollArea
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor, QFont
import sqlite3
import matplotlib.pyplot as plt

from pages.budget import budget
from pages.financial import financial
from pages.financialHealth import financialHealth
from pages.investments import investments
from pages.billsReminders import bills_reminders
from pages.dashboard import dashboard


class FinanceManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FM - Financial Management System")
        self.setGeometry(100, 100, 1400, 900)

        # Load and apply stylesheet
        with open("components/styles.css", "r") as style:
            self.setStyleSheet(style.read())

        # Initialize database
        self.init_database()

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create and add pages
        self.dashboard_page = dashboard(self)
        self.dashboard_page.create_dashboard_tab()
        self.stacked_widget.addWidget(self.dashboard_page.get_widget())

        self.financial_page = financial(self)
        self.financial_page.create_financial_tracking_tab()
        self.stacked_widget.addWidget(self.financial_page.get_widget())
        
        self.budget_page = budget(self)
        self.budget_page.create_budget_management_tab()
        self.stacked_widget.addWidget(self.budget_page.get_widget())
        
        self.bills_page = bills_reminders(self)
        self.bills_page.create_bills_reminders_tab()
        self.stacked_widget.addWidget(self.bills_page.get_widget())
        
        self.investments_page = investments(self)
        self.investments_page.create_investment_tracking_tab()
        self.stacked_widget.addWidget(self.investments_page.get_widget())
        
        self.health_page = financialHealth(self)
        self.health_page.create_financial_health_tab()
        self.stacked_widget.addWidget(self.health_page.get_widget())

    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #aacc00;
                border-radius: 5px;
            }
        """)
        sidebar_widget.setMaximumWidth(220)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(0)

        # Logo/Title
        logo_label = QLabel("FinM")
        logo_font = QFont()
        logo_font.setPointSize(18)
        logo_font.setBold(True)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: #fafafa; padding: 10px 20px; font-family: 'Ultra'; font-weight: 700;")
        subtitle_font = QFont()
        subtitle_font.setPointSize(8)
        sidebar_layout.addWidget(logo_label)

        # Navigation buttons
        nav_items = [
            ("Dashboard", 0),
            ("Transactions", 1),
            ("Budgets", 2),
            ("Bills", 3),
            ("Investments", 4),
            ("Financial Health", 5),
            ("Privacy", 5),  # For now, routes to health
        ]

        for label, page_index in nav_items:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #fafafa;
                    text-align: left;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-family: 'Cantarell';
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                    color: #333333;
                }
            """)
            btn.clicked.connect(lambda checked, idx=page_index: self.switch_page(idx))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        sidebar_widget.setLayout(sidebar_layout)
        
        return sidebar_widget

    def switch_page(self, index):
        """Switch to the specified page"""
        self.stacked_widget.setCurrentIndex(index)

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