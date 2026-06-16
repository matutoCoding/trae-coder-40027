from PySide6.QtGui import QColor


class AppStyles:
    PRIMARY_COLOR = "#1890ff"
    SUCCESS_COLOR = "#52c41a"
    WARNING_COLOR = "#faad14"
    ERROR_COLOR = "#f5222d"
    INFO_COLOR = "#13c2c2"
    
    SIDEBAR_BG = "#001529"
    SIDEBAR_TEXT = "#ffffffb3"
    SIDEBAR_ACTIVE_BG = "#1890ff"
    SIDEBAR_HOVER_BG = "#ffffff1a"
    
    HEADER_BG = "#ffffff"
    CONTENT_BG = "#f0f2f5"
    CARD_BG = "#ffffff"
    
    TEXT_PRIMARY = "#000000d9"
    TEXT_SECONDARY = "#00000073"
    
    BORDER_COLOR = "#d9d9d9"
    
    @classmethod
    def get_global_style(cls):
        return f"""
        QWidget {{
            color: {cls.TEXT_PRIMARY};
            font-family: "Microsoft YaHei", "SimHei", sans-serif;
        }}
        
        QMainWindow, QDialog {{
            background-color: {cls.CONTENT_BG};
        }}
        
        QPushButton {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 13px;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background-color: #40a9ff;
        }}
        
        QPushButton:pressed {{
            background-color: #096dd9;
        }}
        
        QPushButton:disabled {{
            background-color: #d9d9d9;
            color: #ffffffa6;
        }}
        
        QLineEdit, QComboBox, QDateEdit, QDateTimeEdit, QSpinBox, QDoubleSpinBox, QTextEdit {{
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            padding: 5px 8px;
            background-color: white;
            min-height: 20px;
            selection-background-color: {cls.PRIMARY_COLOR};
        }}
        
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDateTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {{
            border-color: {cls.PRIMARY_COLOR};
            outline: none;
        }}
        
        QTableWidget {{
            background-color: white;
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            gridline-color: #f0f0f0;
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        QTableWidget::item:selected {{
            background-color: #e6f7ff;
            color: {cls.TEXT_PRIMARY};
        }}
        
        QHeaderView::section {{
            background-color: #fafafa;
            color: {cls.TEXT_PRIMARY};
            padding: 10px 8px;
            border: none;
            border-bottom: 1px solid {cls.BORDER_COLOR};
            font-weight: bold;
        }}
        
        QTabWidget::pane {{
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            background-color: white;
            top: -1px;
        }}
        
        QTabBar::tab {{
            background-color: #fafafa;
            border: 1px solid {cls.BORDER_COLOR};
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 8px 20px;
            margin-right: 2px;
            color: {cls.TEXT_SECONDARY};
        }}
        
        QTabBar::tab:selected {{
            background-color: white;
            color: {cls.PRIMARY_COLOR};
            border-bottom: 2px solid {cls.PRIMARY_COLOR};
        }}
        
        QTabBar::tab:hover {{
            color: {cls.PRIMARY_COLOR};
        }}
        
        QGroupBox {{
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            margin-top: 16px;
            padding-top: 10px;
            background-color: white;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
            color: {cls.TEXT_PRIMARY};
        }}
        
        QScrollBar:vertical {{
            background: #f5f5f5;
            width: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical {{
            background: #bfbfbf;
            border-radius: 4px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: #8c8c8c;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background: #f5f5f5;
            height: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: #bfbfbf;
            border-radius: 4px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: #8c8c8c;
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        QProgressBar {{
            border: none;
            border-radius: 4px;
            background-color: #f0f0f0;
            text-align: center;
            color: white;
            font-weight: bold;
            height: 16px;
        }}
        
        QProgressBar::chunk {{
            border-radius: 4px;
            background-color: {cls.PRIMARY_COLOR};
        }}
        
        QMenu {{
            background-color: white;
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            padding: 4px 0;
        }}
        
        QMenu::item {{
            padding: 6px 24px;
        }}
        
        QMenu::item:selected {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        QToolTip {{
            background-color: #262626;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 10px;
        }}
        """
    
    @classmethod
    def get_sidebar_style(cls):
        return f"""
        QWidget#sidebar {{
            background-color: {cls.SIDEBAR_BG};
        }}
        
        QLabel#logoLabel {{
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 20px 16px;
            border-bottom: 1px solid #ffffff1a;
        }}
        
        QPushButton.navButton {{
            background-color: transparent;
            color: {cls.SIDEBAR_TEXT};
            border: none;
            border-radius: 0;
            padding: 12px 20px;
            text-align: left;
            font-size: 14px;
        }}
        
        QPushButton.navButton:hover {{
            background-color: {cls.SIDEBAR_HOVER_BG};
            color: white;
        }}
        
        QPushButton.navButton:checked {{
            background-color: {cls.SIDEBAR_ACTIVE_BG};
            color: white;
        }}
        """
    
    @classmethod
    def get_card_style(cls):
        return f"""
        QWidget#card {{
            background-color: {cls.CARD_BG};
            border-radius: 8px;
        }}
        """
    
    @classmethod
    def get_status_badge_style(cls, status_type="normal"):
        colors = {
            "normal": (cls.SUCCESS_COLOR, "#f6ffed"),
            "warning": (cls.WARNING_COLOR, "#fffbe6"),
            "error": (cls.ERROR_COLOR, "#fff2f0"),
            "info": (cls.INFO_COLOR, "#e6fffb"),
            "primary": (cls.PRIMARY_COLOR, "#e6f7ff"),
        }
        text_color, bg_color = colors.get(status_type, colors["normal"])
        return f"""
        QLabel {{
            background-color: {bg_color};
            color: {text_color};
            border: 1px solid {text_color}40;
            border-radius: 10px;
            padding: 2px 12px;
            font-size: 12px;
        }}
        """
