from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QDateEdit, QDialog, QFormLayout,
    QDialogButtonBox, QMessageBox, QSpinBox, QDoubleSpinBox,
    QTextEdit, QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QColor, QBrush, QFont

from ui.styles import AppStyles


class BasePage(QWidget):
    def __init__(self, title=""):
        super().__init__()
        self.page_title = title
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)
    
    def create_card(self, title=""):
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(f"""
            QFrame#card {{
                background-color: {AppStyles.CARD_BG};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #000000d9;
                }
            """)
            layout.addWidget(title_label)
        
        return card, layout
    
    def create_status_label(self, text, status_type="normal"):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        label.setFixedHeight(24)
        return label
    
    def create_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                gridline-color: #f0f0f0;
                alternate-background-color: #fafafa;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: #e6f7ff;
                color: {AppStyles.TEXT_PRIMARY};
            }}
        """)
        return table
    
    def create_toolbar(self):
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        return toolbar, toolbar_layout
    
    def create_search_input(self, placeholder="搜索..."):
        search_input = QLineEdit()
        search_input.setPlaceholderText(placeholder)
        search_input.setFixedHeight(32)
        search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                padding: 4px 12px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border-color: {AppStyles.PRIMARY_COLOR};
            }}
        """)
        return search_input
    
    def create_primary_button(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(32)
        btn.setCursor(Qt.PointingHandCursor)
        return btn
    
    def create_secondary_button(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(32)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: {AppStyles.TEXT_PRIMARY};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                padding: 4px 16px;
            }}
            QPushButton:hover {{
                border-color: {AppStyles.PRIMARY_COLOR};
                color: {AppStyles.PRIMARY_COLOR};
            }}
        """)
        return btn
    
    def create_stat_card(self, title, value, subtitle="", color=AppStyles.PRIMARY_COLOR):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {AppStyles.TEXT_PRIMARY};")
        layout.addWidget(value_label)
        
        if subtitle:
            sub_label = QLabel(subtitle)
            sub_label.setStyleSheet(f"font-size: 12px; color: {AppStyles.SUCCESS_COLOR};")
            layout.addWidget(sub_label)
        
        return card
    
    def add_table_row(self, table, row_data, status_col=None, status_type_map=None):
        row = table.rowCount()
        table.insertRow(row)
        
        for col, data in enumerate(row_data):
            if status_col is not None and col == status_col:
                status_type = "normal"
                if status_type_map and data in status_type_map:
                    status_type = status_type_map[data]
                item = self._create_status_item(data, status_type)
                table.setCellWidget(row, col, item)
            else:
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, col, item)
    
    def _create_status_item(self, text, status_type="normal"):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel(text)
        label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(22)
        label.setMinimumWidth(60)
        
        layout.addWidget(label)
        return widget


class BaseDialog(QDialog):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(500)
        self.setModal(True)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(12)
        self.form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addLayout(self.form_layout)
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.button(QDialogButtonBox.Ok).setText("确定")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        ok_btn = button_box.button(QDialogButtonBox.Ok)
        ok_btn.setFixedHeight(32)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                background-color: #40a9ff;
            }}
        """)
        
        cancel_btn = button_box.button(QDialogButtonBox.Cancel)
        cancel_btn.setFixedHeight(32)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: {AppStyles.TEXT_PRIMARY};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                border-color: {AppStyles.PRIMARY_COLOR};
                color: {AppStyles.PRIMARY_COLOR};
            }}
        """)
        
        layout.addWidget(button_box)
    
    def add_field(self, label, widget):
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY}; font-size: 13px;")
        self.form_layout.addRow(label_widget, widget)
