from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QMessageBox, QScrollArea
)
from PyQt6.QtCore import QDate, Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import sqlite3
import matplotlib.pyplot as plt


class financial:
    def __init__(self, parent):
        self.parent = parent
        self.conn = parent.conn
        self.widget = None

    def get_widget(self):
        """Return the financial tracking widget"""
        return self.widget

    def create_financial_tracking_tab(self):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #f9f9f9;")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Header with title
        header_layout = QHBoxLayout()
        title = QLabel("Transactions")
        title.setStyleSheet("color: #31572c; font-family: Helvetica; font-weight: 700; font-size: 24px;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Add Entry")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.show_add_transaction_dialog)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)

        # Search and Filter bar
        search_filter_layout = QHBoxLayout()
        search_filter_layout.setSpacing(15)
        
        search = QLineEdit()
        search.setPlaceholderText("Search category...")
        search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: white;
                color: #1a1a1a;
            }
        """)
        search.setMinimumWidth(400)
        search_filter_layout.addWidget(search)
        
        search_filter_layout.addStretch()
        
        # Filter buttons
        filter_buttons = ["All", "Income", "Expense"]
        self.filter_btn_group = {}
        for filt in filter_buttons:
            btn = QPushButton(filt)
            is_all = filt == "All"
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {'#aacc00' if is_all else '#f0f0f0'};
                    color: {'white' if is_all else '#666666'};
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: 600;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {'#aacc00' if is_all else '#e0e0e0'};
                }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, f=filt: self.filter_transactions(f))
            search_filter_layout.addWidget(btn)
            self.filter_btn_group[filt] = btn
        
        self.current_filter = "All"
        layout.addLayout(search_filter_layout)

        # Transactions Table
        self.trans_table = QTableWidget()
        self.trans_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QHeaderView::section {
                background-color: white;
                color: #666666;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: 600;
                font-size: 12px;
                text-transform: uppercase;
            }
        """)
        self.trans_table.setColumnCount(5)
        self.trans_table.setHorizontalHeaderLabels(["DATE", "MERCHANT / NOTES", "CATEGORY", "AMOUNT", ""])
        self.trans_table.horizontalHeader().setStretchLastSection(False)
        self.trans_table.setColumnWidth(0, 197)
        self.trans_table.setColumnWidth(1, 300)
        self.trans_table.setColumnWidth(2, 200)
        self.trans_table.setColumnWidth(3, 200)
        self.trans_table.setColumnWidth(4, 40)
        self.load_transactions()
        layout.addWidget(self.trans_table)
        layout.addStretch()
        self.widget.setLayout(layout)

    def show_add_transaction_dialog(self):
        """Show dialog to add a new transaction"""
        # For now, just show a placeholder - can be expanded later
        QMessageBox.information(self.parent, "Add Transaction", "Add transaction feature coming soon!")

    def filter_transactions(self, filter_type):
        """Filter transactions by type"""
        self.current_filter = filter_type
        
        # Update button styles
        for btn_name, btn in self.filter_btn_group.items():
            if btn_name == filter_type:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #aacc00;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 20px;
                        font-weight: 600;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #aacc00;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #666666;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 20px;
                        font-weight: 600;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
        
        self.load_transactions()

    def load_transactions(self):
        """Load and display transactions"""
        try:
            c = self.conn.cursor()
            
            if self.current_filter == "All":
                c.execute("SELECT id, date, description, category, type, amount FROM transactions ORDER BY date DESC")
            else:
                c.execute("SELECT id, date, description, category, type, amount FROM transactions WHERE type = ? ORDER BY date DESC", 
                         (self.current_filter,))
            
            rows = c.fetchall()
            self.trans_table.setRowCount(len(rows))
            
            for i, row in enumerate(rows):
                trans_id, date, desc, category, trans_type, amount = row
                
                # Date
                date_item = QTableWidgetItem(date)
                date_item.setForeground(Qt.GlobalColor.black)
                self.trans_table.setItem(i, 0, date_item)
                
                # Description
                desc_item = QTableWidgetItem(desc if desc else "-")
                self.trans_table.setItem(i, 1, desc_item)
                
                # Category
                cat_item = QTableWidgetItem(category.upper() if category else "-")
                cat_item.setForeground(Qt.GlobalColor.gray)
                cat_font = QFont()
                cat_font.setPointSize(9)
                cat_item.setFont(cat_font)
                self.trans_table.setItem(i, 2, cat_item)
                
                # Amount
                amount_str = f"{amount:.2f}"
                if trans_type == "Income":
                    amount_item = QTableWidgetItem(f"+${amount_str}")
                    amount_item.setForeground(Qt.GlobalColor.green)
                else:
                    amount_item = QTableWidgetItem(f"-${amount_str}")
                    amount_item.setForeground(Qt.GlobalColor.red)
                
                amount_font = QFont()
                amount_font.setBold(True)
                amount_item.setFont(amount_font)
                self.trans_table.setItem(i, 3, amount_item)
                
                # Delete button
                delete_btn = QPushButton("🗑")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: #999999;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        color: #e74c3c;
                    }
                """)
                delete_btn.setMaximumWidth(40)
                delete_btn.clicked.connect(lambda checked, tid=trans_id: self.delete_transaction(tid))
                self.trans_table.setCellWidget(i, 4, delete_btn)
                
        except Exception as e:
            print(f"Error loading transactions: {e}")

    def add_transaction(self, trans_type, amount, category, desc, date):
        """Add a transaction to the database"""
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO transactions (type, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
                      (trans_type, amount, category, desc, date))
            self.conn.commit()
            self.load_transactions()
            QMessageBox.information(self.parent, "Success", "Transaction added!")
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Invalid data: {e}")

    def delete_transaction(self, trans_id):
        """Delete a transaction"""
        reply = QMessageBox.question(self.parent, "Confirm Delete", "Delete this transaction?")
        if reply == QMessageBox.StandardButton.Yes:
            try:
                c = self.conn.cursor()
                c.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
                self.conn.commit()
                self.load_transactions()
            except Exception as e:
                QMessageBox.warning(self.parent, "Error", f"Could not delete: {e}")

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