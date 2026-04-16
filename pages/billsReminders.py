from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFrame, QMessageBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import sqlite3
    

class bills_reminders:
    def __init__(self, parent):
        self.parent = parent
        self.conn = parent.conn
        self.widget = None
    
    def get_widget(self):
        """Return the bills and reminders widget"""
        return self.widget
    
    def create_bills_reminders_tab(self):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #f5f5f5;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Header
        title = QLabel("Recurring Bills")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a1a1a;")
        
        subtitle = QLabel("Manage subscriptions and automated payments")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666666;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Bills list
        bills_container = QVBoxLayout()
        bills_container.setSpacing(12)
        
        c = self.conn.cursor()
        c.execute("SELECT id, name, amount, due_date, auto_deduct FROM bills ORDER BY due_date")
        bills = c.fetchall()
        
        for bill_id, name, amount, due_date, auto_deduct in bills:
            bill_item = self.create_bill_item(bill_id, name, amount, due_date, auto_deduct)
            bills_container.addWidget(bill_item)
        
        bills_container.addStretch()
        layout.addLayout(bills_container)

        self.widget.setLayout(layout)

    def create_bill_item(self, bill_id, name, amount, due_date, auto_deduct):
        """Create a single bill display item"""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
            }
        """)
        item.setMinimumHeight(80)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(20)
        
        # Status icon
        status_icon = QLabel("✓" if auto_deduct else "📅")
        status_icon.setStyleSheet("font-size: 20px; color: #10b981;")
        layout.addWidget(status_icon)
        
        # Bill name and due date
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name_label = QLabel(name)
        name_font = QFont()
        name_font.setPointSize(13)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setStyleSheet("color: #1a1a1a;")
        
        # Parse due date to determine renewal info
        due_day = due_date.split('-')[-1] if due_date else "1st"
        due_text = f"Due every month on the {due_day}"
        
        due_label = QLabel(due_text)
        due_font = QFont()
        due_font.setPointSize(9)
        due_label.setFont(due_font)
        due_label.setStyleSheet("color: #666666;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(due_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Amount
        amount_label = QLabel(f"${amount:.2f}")
        amount_font = QFont()
        amount_font.setPointSize(14)
        amount_font.setBold(True)
        amount_label.setFont(amount_font)
        amount_label.setStyleSheet("color: #1a1a1a;")
        layout.addWidget(amount_label)
        
        # Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(6)
        
        if auto_deduct:
            status_btn = QPushButton("AUTOMATIC ON")
            status_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e7ff;
                    color: #6366f1;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                    font-size: 11px;
                    font-weight: 600;
                }
            """)
        else:
            status_btn = QPushButton("AUTOMATIC OFF")
            status_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #666666;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                    font-size: 11px;
                    font-weight: 600;
                }
            """)
            status_btn.clicked.connect(lambda: self.toggle_automatic(bill_id))
        
        status_btn.setMaximumWidth(140)
        btn_layout.addWidget(status_btn)
        
        # Second button
        if auto_deduct:
            paid_btn = QPushButton("Paid")
            paid_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #666666;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    padding: 6px 14px;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
        else:
            paid_btn = QPushButton("Mark as Paid")
            paid_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #666666;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    padding: 6px 14px;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            paid_btn.clicked.connect(lambda: self.mark_as_paid(bill_id))
        
        paid_btn.setMaximumWidth(140)
        btn_layout.addWidget(paid_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        item.setLayout(layout)
        return item

    def toggle_automatic(self, bill_id):
        """Toggle automatic payment status"""
        try:
            c = self.conn.cursor()
            c.execute("SELECT auto_deduct FROM bills WHERE id = ?", (bill_id,))
            current = c.fetchone()[0]
            c.execute("UPDATE bills SET auto_deduct = ? WHERE id = ?", (1 - current, bill_id))
            self.conn.commit()
            self.recreate_widget()
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Could not update: {e}")

    def mark_as_paid(self, bill_id):
        """Mark a bill as paid"""
        QMessageBox.information(self.parent, "Paid", "Bill marked as paid!")

    def recreate_widget(self):
        """Recreate the widget to reflect changes"""
        self.create_bills_reminders_tab()
        parent_widget = self.parent.stacked_widget
        parent_widget.removeWidget(self.widget)
        self.create_bills_reminders_tab()
        parent_widget.addWidget(self.widget)

    def add_bill(self):
        try:
            name = self.bill_name.text()
            amt = float(self.bill_amt.text())
            date = self.bill_date.date().toString("yyyy-MM-dd")
            auto = 1 if self.auto_deduct.isChecked() else 0
            c = self.conn.cursor()
            c.execute("INSERT INTO bills (name, amount, due_date, auto_deduct) VALUES (?, ?, ?, ?)", (name, amt, date, auto))
            self.conn.commit()
            self.create_bills_reminders_tab()
            QMessageBox.information(self.parent, "Success", "Bill added!")
        except ValueError:
            QMessageBox.warning(self.parent, "Error", "Invalid amount")

    def load_bills(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM bills")
        rows = c.fetchall()
        return rows

    def check_reminders(self):
        c = self.conn.cursor()
        c.execute("SELECT name, amount, due_date FROM bills WHERE date(due_date) <= date('now', '+7 days')")
        bills = c.fetchall()
        text = "Upcoming Bills:\n"
        for bill in bills:
            text += f"{bill[0]}: {bill[1]} due {bill[2]}\n"
        return text
