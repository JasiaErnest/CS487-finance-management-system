from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.conn = parent.conn
        self.widget = None

    def get_widget(self):
        return self.widget

    def create_dashboard_tab(self):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #fafafa;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header_layout = QVBoxLayout()
        title_label = QLabel("Financial Summary")
        title_label.setStyleSheet("color: #31572c; font-family: Helvetica; font-size: 24px; font-weight: 600;")

        subtitle_label = QLabel("Real-time health monitoring & insights")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #666666;")

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addLayout(header_layout)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        total_balance = self.get_total_balance()
        monthly_income = self.get_monthly_income()
        monthly_spending = self.get_monthly_spending()

        balance_card = self.create_metric_card(
            "Total Balance", f"${total_balance:.2f}", "#e0e7ff"
        )
        income_card = self.create_metric_card(
            "Monthly Income", f"${monthly_income:.2f}", "#dcfce7"
        )
        spending_card = self.create_metric_card(
            "Monthly Spending", f"${monthly_spending:.2f}", "#fee2e2"
        )

        cards_layout.addWidget(balance_card)
        cards_layout.addWidget(income_card)
        cards_layout.addWidget(spending_card)
        layout.addLayout(cards_layout)

        smart_layout = QHBoxLayout()
        smart_layout.setSpacing(20)

        smart_card = self.create_smart_analysis_card()
        trends_card = self.create_trends_card()
        smart_layout.addWidget(smart_card)
        smart_layout.addWidget(trends_card)

        layout.addLayout(smart_layout)
        layout.addStretch()
        self.widget.setLayout(layout)

    def create_metric_card(self, title, value, bg_color):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
        """)
        card.setMinimumHeight(120)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()\

        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(10)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #666666;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #1a1a1a;")

        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        layout.addStretch()
        card.setLayout(layout)
        return card

    def create_smart_analysis_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #31662c;
                border-radius: 12px;
                color: white;
            }
        """)
        card.setMinimumHeight(220)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title_label = QLabel("Smart Analysis")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")

        score_layout = QHBoxLayout()
        score_label = QLabel("60")
        score_font = QFont()
        score_font.setPointSize(28)
        score_font.setBold(True)
        score_label.setFont(score_font)
        score_label.setStyleSheet("color: white;")

        score_text = QLabel("HEALTH SCORE")
        score_text_font = QFont()
        score_text_font.setPointSize(9)
        score_text.setFont(score_text_font)
        score_text.setStyleSheet("color: rgba(255,255,255,0.7);")

        score_layout.addWidget(score_label)
        score_layout.addSpacing(10)
        score_layout.addWidget(score_text, alignment=Qt.AlignmentFlag.AlignBottom)
        score_layout.addStretch()

        layout.addWidget(title_label)
        layout.addLayout(score_layout)

        insights = [
            "✓ Great job! You're well within your budget limits.",
            "✓ 2 upcoming bills remaining this month.",
            "✓ Healthy cash cushion detected.",
        ]
        for item in insights:
            insight_label = QLabel(item)
            insight_font = QFont()
            insight_font.setPointSize(9)
            insight_label.setFont(insight_font)
            insight_label.setStyleSheet("color: rgba(255,255,255,0.9);")
            insight_label.setWordWrap(True)
            layout.addWidget(insight_label)

        layout.addStretch()
        card.setLayout(layout)
        return card

    def create_trends_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        card.setMinimumHeight(220)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title_layout = QHBoxLayout()
        title_label = QLabel("Spending Trends")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1a1a1a;")

        period_label = QLabel("LAST 3 MONTHS")
        period_font = QFont()
        period_font.setPointSize(9)
        period_label.setFont(period_font)
        period_label.setStyleSheet("color: #999999;")

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(period_label)

        chart_placeholder = QLabel("📊")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("font-size: 72px; color: #f0f0f0;")

        months_layout = QHBoxLayout()
        for month in ["FEB", "MAR", "APR"]:
            month_label = QLabel(month)
            month_font = QFont()
            month_font.setPointSize(10)
            month_label.setFont(month_font)
            month_label.setStyleSheet("color: #999999;")
            months_layout.addWidget(month_label)
            months_layout.addStretch()

        layout.addLayout(title_layout)
        layout.addWidget(chart_placeholder)
        layout.addLayout(months_layout)
        card.setLayout(layout)
        return card

    def get_total_balance(self):
        try:
            c = self.conn.cursor()
            c.execute(
                "SELECT SUM(CASE WHEN type = 'Income' THEN amount ELSE -amount END) FROM transactions"
            )
            result = c.fetchone()
            return result[0] if result and result[0] is not None else 0.0
        except Exception:
            return 0.0

    def get_monthly_income(self):
        try:
            c = self.conn.cursor()
            c.execute(
                "SELECT SUM(amount) FROM transactions WHERE type = 'Income' AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')"
            )
            result = c.fetchone()
            return result[0] if result and result[0] is not None else 0.0
        except Exception:
            return 0.0

    def get_monthly_spending(self):
        try:
            c = self.conn.cursor()
            c.execute(
                "SELECT SUM(amount) FROM transactions WHERE type = 'Expense' AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')"
            )
            result = c.fetchone()
            return result[0] if result and result[0] is not None else 0.0
        except Exception:
            return 0.0
