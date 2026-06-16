from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon

from ui.styles import AppStyles
from ui.modules.tank_ledger import TankLedgerPage
from ui.modules.receive_meter import ReceiveMeterPage
from ui.modules.dispatch_load import DispatchLoadPage
from ui.modules.inspection import InspectionPage
from ui.modules.nitrogen_seal import NitrogenSealPage
from ui.modules.fire_control import FireControlPage
from ui.modules.safety_monitor import SafetyMonitorPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("危化品罐区储运业务管理系统")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 680)
        
        self._init_ui()
        self._setup_connections()
    
    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self._create_sidebar()
        self._create_content_area()
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_frame)
    
    def _create_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet(AppStyles.get_sidebar_style())
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        logo_label = QLabel("🏭 危化品罐区管理")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)
        
        nav_menu = QVBoxLayout()
        nav_menu.setContentsMargins(0, 10, 0, 10)
        nav_menu.setSpacing(2)
        
        self.nav_buttons = []
        
        nav_items = [
            ("📋", "储罐台账", "tank"),
            ("📥", "收料计量", "receive"),
            ("📤", "发料装车", "dispatch"),
            ("🔍", "罐区巡检", "inspection"),
            ("💨", "氮封惰化", "nitrogen"),
            ("🚒", "消防联动", "fire"),
            ("🛡️", "安全监测", "safety"),
        ]
        
        for icon, text, page_key in nav_items:
            btn = QPushButton(f"  {icon}  {text}")
            btn.setObjectName(f"nav_{page_key}")
            btn.setProperty("class", "navButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ffffffb3;
                    border: none;
                    border-radius: 0;
                    padding: 12px 20px;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #ffffff1a;
                    color: white;
                }
                QPushButton:checked {
                    background-color: #1890ff;
                    color: white;
                    border-left: 3px solid white;
                }
            """)
            btn.page_key = page_key
            self.nav_buttons.append(btn)
            nav_menu.addWidget(btn)
        
        nav_menu.addStretch()
        
        sidebar_layout.addLayout(nav_menu)
        
        user_label = QLabel("👤 管理员")
        user_label.setStyleSheet("""
            QLabel {
                color: #ffffffb3;
                padding: 16px 20px;
                border-top: 1px solid #ffffff1a;
                font-size: 13px;
            }
        """)
        sidebar_layout.addWidget(user_label)
    
    def _create_content_area(self):
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet(f"background-color: {AppStyles.CONTENT_BG};")
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self._create_header()
        
        self.pages = QStackedWidget()
        self.pages.setObjectName("contentPages")
        
        self.tank_page = TankLedgerPage()
        self.receive_page = ReceiveMeterPage()
        self.dispatch_page = DispatchLoadPage()
        self.inspection_page = InspectionPage()
        self.nitrogen_page = NitrogenSealPage()
        self.fire_page = FireControlPage()
        self.safety_page = SafetyMonitorPage()
        
        self.pages.addWidget(self.tank_page)
        self.pages.addWidget(self.receive_page)
        self.pages.addWidget(self.dispatch_page)
        self.pages.addWidget(self.inspection_page)
        self.pages.addWidget(self.nitrogen_page)
        self.pages.addWidget(self.fire_page)
        self.pages.addWidget(self.safety_page)
        
        self.page_map = {
            "tank": 0,
            "receive": 1,
            "dispatch": 2,
            "inspection": 3,
            "nitrogen": 4,
            "fire": 5,
            "safety": 6,
        }
        
        content_layout.addWidget(self.header)
        content_layout.addWidget(self.pages)
    
    def _create_header(self):
        self.header = QFrame()
        self.header.setObjectName("header")
        self.header.setFixedHeight(60)
        self.header.setStyleSheet(f"""
            QFrame#header {{
                background-color: {AppStyles.HEADER_BG};
                border-bottom: 1px solid #e8e8e8;
            }}
        """)
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        
        self.page_title = QLabel("储罐台账")
        self.page_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #000000d9;
            }
        """)
        header_layout.addWidget(self.page_title)
        
        header_layout.addStretch()
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #00000073; font-size: 13px;")
        header_layout.addWidget(self.time_label)
    
    def _setup_connections(self):
        for btn in self.nav_buttons:
            btn.clicked.connect(self._on_nav_clicked)
        
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
            self._switch_page("tank")
    
    def _on_nav_clicked(self):
        clicked_btn = self.sender()
        for btn in self.nav_buttons:
            btn.setChecked(btn == clicked_btn)
        self._switch_page(clicked_btn.page_key)
    
    def _switch_page(self, page_key):
        page_index = self.page_map.get(page_key, 0)
        self.pages.setCurrentIndex(page_index)
        
        title_map = {
            "tank": "储罐台账",
            "receive": "收料计量",
            "dispatch": "发料装车",
            "inspection": "罐区巡检",
            "nitrogen": "氮封惰化",
            "fire": "消防联动",
            "safety": "安全监测",
        }
        self.page_title.setText(title_map.get(page_key, ""))
