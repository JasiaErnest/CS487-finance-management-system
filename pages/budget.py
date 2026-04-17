from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QFrame, QScrollArea, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sqlite3


class budget:
    def __init__(self, parent):
        self.parent = parent
        self.conn = parent.conn
        self.widget = None

    def get_widget(self):
        """Return the budget management widget"""
        return self.widget

    def create_budget_management_tab(self):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #f5f5f5;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        title = QLabel("Monthly Budgets")
        title.setStyleSheet("color: #31572c; font-family: Helvetica; font-size: 24px; font-weight: 600;")
        
        subtitle = QLabel("Plan your spending and track limits")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666666;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # Scroll area for budget cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: transparent;")
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        
        # Get budgets and display as cards
        c = self.conn.cursor()
        c.execute("SELECT id, category, amount FROM budgets")
        budgets = c.fetchall()
        
        for budget_id, category, amount in budgets:
            card = self.create_budget_card(category, amount, budget_id)
            cards_layout.addWidget(card)
        
        cards_layout.addStretch()
        scroll_widget.setLayout(cards_layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        # Add Category Budget Button
        add_btn_layout = QHBoxLayout()
        add_btn_layout.setContentsMargins(0, 20, 0, 0)
        
        add_btn = QPushButton("+ Add Category Budget")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #31662c;
                border: 2px dashed #31662c;
                border-radius: 12px;
                padding: 40px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f0f2ff;
            }
        """)
        add_btn.setMinimumHeight(100)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.show_add_budget_dialog)
        add_btn_layout.addWidget(add_btn)
        
        main_layout.addLayout(add_btn_layout)
        main_layout.addStretch()
        
        self.widget.setLayout(main_layout)

    def create_budget_card(self, category, amount, budget_id):
        """Create a single budget card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)
        card.setMinimumWidth(280)
        card.setMaximumWidth(280)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Header with icon and edit button
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("🎯")
        icon_label.setStyleSheet("font-size: 24px;")
        
        category_label = QLabel(category)
        cat_font = QFont()
        cat_font.setPointSize(13)
        cat_font.setBold(True)
        category_label.setFont(cat_font)
        category_label.setStyleSheet("color: #1a1a1a;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(category_label)
        header_layout.addStretch()
        
        edit_btn = QPushButton("✏️")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #6366f1;
            }
        """)
        edit_btn.setMaximumWidth(30)
        header_layout.addWidget(edit_btn)
        
        layout.addLayout(header_layout)
        
        # Amount display
        amount_label = QLabel(f"${amount:.0f}")
        amount_font = QFont()
        amount_font.setPointSize(14)
        amount_font.setBold(True)
        amount_label.setFont(amount_font)
        amount_label.setStyleSheet("color: #1a1a1a;")
        layout.addWidget(amount_label)
        
        # Usage section
        usage_label = QLabel("USAGE")
        usage_font = QFont()
        usage_font.setPointSize(9)
        usage_label.setFont(usage_font)
        usage_label.setStyleSheet("color: #6366f1; font-weight: 600;")
        layout.addWidget(usage_label)
        
        # Progress bar
        progress = QProgressBar()
        progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #f0f0f0;
                border-radius: 4px;
                height: 6px;
            }
            QProgressBar::chunk {
                background-color: #6366f1;
                border-radius: 4px;
            }
        """)
        
        # Calculate usage percentage
        c = self.conn.cursor()
        c.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='Expense' AND category=?", (category,))
        spent = c.fetchone()[0]
        usage_percent = int((spent / amount * 100)) if amount > 0 else 0
        progress.setValue(min(usage_percent, 100))
        
        layout.addWidget(progress)
        
        # Set limit text
        limit_label = QLabel(f"SET LIMIT: ${amount:.0f}")
        limit_font = QFont()
        limit_font.setPointSize(9)
        limit_label.setFont(limit_font)
        limit_label.setStyleSheet("color: #999999;")
        layout.addWidget(limit_label)
        
        # Historical data message
        history_label = QLabel("Historical data shows you usually use ~85% of this budget.")
        history_font = QFont()
        history_font.setPointSize(8)
        history_label.setFont(history_font)
        history_label.setStyleSheet("color: #999999; font-style: italic;")
        history_label.setWordWrap(True)
        layout.addWidget(history_label)
        
        layout.addStretch()
        card.setLayout(layout)
        return card

    def show_add_budget_dialog(self):
        """Show dialog to add a new budget"""
        QMessageBox.information(self.parent, "Add Budget", "Add budget feature coming soon!")

    def set_budget(self, category, amount):
        """Set a budget for a category"""
        try:
            c = self.conn.cursor()
            c.execute("INSERT OR REPLACE INTO budgets (category, amount, period) VALUES (?, ?, ?)", 
                     (category, amount, "Monthly"))
            self.conn.commit()
            QMessageBox.information(self.parent, "Success", "Budget set!")
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Invalid data: {e}")

    def load_budgets(self):
        """Load all budgets from database"""
        c = self.conn.cursor()
        c.execute("SELECT * FROM budgets")
        rows = c.fetchall()
        return rows

    def update_progress(self):
        """Update progress bars for all budgets"""
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

