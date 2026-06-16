from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QComboBox, QFrame, QGroupBox, QGridLayout,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QDoubleSpinBox, QDateEdit, QTextEdit, QWidget, QProgressBar,
    QTabWidget, QSpinBox, QDateTimeEdit
)
from PySide6.QtCore import Qt, QDate, QDateTime, QTimer
from PySide6.QtGui import QColor, QFont

from ui.modules.base_page import BasePage, BaseDialog
from data.mock_data import MockData
from ui.styles import AppStyles


class SafetyMonitorPage(BasePage):
    def __init__(self):
        super().__init__("安全监测")
        self.detectors = MockData.get_gas_detectors()
        self.tanks = MockData.get_storage_tanks()
        self.hot_works = MockData.get_hot_work_permits()
        self._build_ui()
        self._load_data()
    
    def _build_ui(self):
        main_layout = self.layout()
        
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)
        
        alarm_count = sum(1 for d in self.detectors if d.status == "报警")
        warning_count = sum(1 for d in self.detectors if d.status == "预警")
        normal_count = sum(1 for d in self.detectors if d.status == "正常")
        pending_hotwork = sum(1 for h in self.hot_works if h.status in ["待审批", "进行中"])
        
        card1 = self.create_stat_card("气体探测器", f"{len(self.detectors)} 台", "监测设备总数", AppStyles.PRIMARY_COLOR)
        card2 = self.create_stat_card("正常运行", f"{normal_count} 台", "状态正常", AppStyles.SUCCESS_COLOR)
        card3 = self.create_stat_card("预警/报警", f"{warning_count + alarm_count} 台", "需关注", AppStyles.ERROR_COLOR)
        card4 = self.create_stat_card("动火作业", f"{pending_hotwork} 项", "进行中/待审批", AppStyles.WARNING_COLOR)
        
        stats_row.addWidget(card1, 1)
        stats_row.addWidget(card2, 1)
        stats_row.addWidget(card3, 1)
        stats_row.addWidget(card4, 1)
        
        main_layout.addLayout(stats_row)
        
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                background-color: white;
                top: -1px;
            }}
            QTabBar::tab {{
                background-color: #fafafa;
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 20px;
                margin-right: 2px;
                color: {AppStyles.TEXT_SECONDARY};
            }}
            QTabBar::tab:selected {{
                background-color: white;
                color: {AppStyles.PRIMARY_COLOR};
                border-bottom: 2px solid {AppStyles.PRIMARY_COLOR};
            }}
        """)
        
        level_tab = QWidget()
        level_layout = QVBoxLayout(level_tab)
        level_layout.setContentsMargins(0, 0, 0, 0)
        self._build_level_tab(level_layout)
        tabs.addTab(level_tab, "液位温度监控")
        
        gas_tab = QWidget()
        gas_layout = QVBoxLayout(gas_tab)
        gas_layout.setContentsMargins(0, 0, 0, 0)
        self._build_gas_tab(gas_layout)
        tabs.addTab(gas_tab, "可燃气体检测")
        
        hotwork_tab = QWidget()
        hotwork_layout = QVBoxLayout(hotwork_tab)
        hotwork_layout.setContentsMargins(0, 0, 0, 0)
        self._build_hotwork_tab(hotwork_layout)
        tabs.addTab(hotwork_tab, "动火作业许可")
        
        main_layout.addWidget(tabs)
    
    def _build_level_tab(self, layout):
        card, card_layout = self.create_card("储罐液位温度实时监控")
        
        grid = QGridLayout()
        grid.setSpacing(16)
        
        for i, tank in enumerate(self.tanks):
            row = i // 3
            col = i % 3
            panel = self._create_level_panel(tank)
            grid.addWidget(panel, row, col)
        
        card_layout.addLayout(grid)
        layout.addWidget(card)
    
    def _create_level_panel(self, tank):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        header = QHBoxLayout()
        
        name_label = QLabel(tank.name)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        header.addWidget(name_label)
        
        header.addStretch()
        
        status_type = "normal" if tank.status == "正常" else "warning"
        status_label = QLabel(tank.status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        status_label.setFixedHeight(22)
        status_label.setFixedWidth(60)
        header.addWidget(status_label)
        
        layout.addLayout(header)
        
        medium_label = QLabel(f"介质：{tank.medium}")
        medium_label.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 12px;")
        layout.addWidget(medium_label)
        
        level_container = QHBoxLayout()
        level_container.setSpacing(20)
        
        level_bar_container = QVBoxLayout()
        level_bar_container.setSpacing(4)
        
        level_text_layout = QHBoxLayout()
        level_text_layout.addWidget(QLabel("液位"))
        level_text_layout.addStretch()
        level_value = QLabel(f"{tank.current_level:.2f} m")
        level_value.setStyleSheet(f"font-weight: bold; color: {AppStyles.PRIMARY_COLOR};")
        level_text_layout.addWidget(level_value)
        level_bar_container.addLayout(level_text_layout)
        
        level_bar = QProgressBar()
        level_bar.setOrientation(Qt.Horizontal)
        level_percent = (tank.current_level / tank.height) * 100
        level_bar.setValue(int(level_percent))
        level_bar.setTextVisible(False)
        level_bar.setFixedHeight(16)
        
        color = AppStyles.SUCCESS_COLOR
        if level_percent > 85:
            color = AppStyles.WARNING_COLOR
        if level_percent > 95:
            color = AppStyles.ERROR_COLOR
        
        level_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 8px;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                border-radius: 8px;
                background-color: {color};
            }}
        """)
        level_bar_container.addWidget(level_bar)
        
        level_container.addLayout(level_bar_container, 2)
        
        info_widget = QWidget()
        info_grid = QGridLayout(info_widget)
        info_grid.setSpacing(4)
        info_grid.setContentsMargins(0, 0, 0, 0)
        
        info_items = [
            ("体积", f"{tank.current_volume:.0f} m³"),
            ("温度", f"{tank.current_temperature:.1f} ℃"),
            ("压力", f"{tank.current_pressure:.3f} MPa"),
            ("容量", f"{tank.capacity:.0f} m³"),
        ]
        
        for i, (label, value) in enumerate(info_items):
            row = i // 2
            col = (i % 2) * 2
            l = QLabel(f"{label}:")
            l.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 11px;")
            v = QLabel(value)
            v.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY}; font-size: 12px; font-weight: bold;")
            info_grid.addWidget(l, row, col)
            info_grid.addWidget(v, row, col + 1)
        
        level_container.addWidget(info_widget, 1)
        
        layout.addLayout(level_container)
        
        return panel
    
    def _build_gas_tab(self, layout):
        card, card_layout = self.create_card("可燃/有毒气体检测")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        self.search_gas = self.create_search_input("搜索位置、类型...")
        self.search_gas.setFixedWidth(240)
        self.search_gas.textChanged.connect(self._on_search_gas)
        toolbar_layout.addWidget(self.search_gas)
        
        self.filter_gas = QComboBox()
        self.filter_gas.addItems(["全部状态", "正常", "预警", "报警"])
        self.filter_gas.setFixedHeight(32)
        self.filter_gas.currentIndexChanged.connect(self._on_filter_gas)
        toolbar_layout.addWidget(self.filter_gas)
        
        toolbar_layout.addStretch()
        
        calibrate_btn = self.create_secondary_button("校准记录")
        calibrate_btn.clicked.connect(lambda: QMessageBox.information(self, "提示", "校准记录功能开发中..."))
        toolbar_layout.addWidget(calibrate_btn)
        
        card_layout.addWidget(toolbar)
        
        detector_grid = QGridLayout()
        detector_grid.setSpacing(12)
        
        for i, detector in enumerate(self.detectors):
            row = i // 4
            col = i % 4
            panel = self._create_detector_panel(detector)
            detector_grid.addWidget(panel, row, col)
        
        card_layout.addLayout(detector_grid)
        
        layout.addWidget(card)
    
    def _create_detector_panel(self, detector):
        panel = QFrame()
        
        border_color = AppStyles.SUCCESS_COLOR
        if detector.status == "预警":
            border_color = AppStyles.WARNING_COLOR
        elif detector.status == "报警":
            border_color = AppStyles.ERROR_COLOR
        
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {border_color}40;
                border-left: 4px solid {border_color};
                border-radius: 6px;
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)
        
        header = QHBoxLayout()
        
        icon = "✅"
        if detector.status == "预警":
            icon = "⚠️"
        elif detector.status == "报警":
            icon = "🚨"
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px;")
        header.addWidget(icon_label)
        
        name_label = QLabel(detector.gas_type)
        name_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        header.addWidget(name_label)
        
        header.addStretch()
        
        status_type = "normal"
        if detector.status == "预警":
            status_type = "warning"
        elif detector.status == "报警":
            status_type = "error"
        
        status_label = QLabel(detector.status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        status_label.setFixedHeight(20)
        status_label.setFixedWidth(56)
        header.addWidget(status_label)
        
        layout.addLayout(header)
        
        value_layout = QHBoxLayout()
        
        value_label = QLabel(f"{detector.current_value:.1f}")
        value_color = AppStyles.SUCCESS_COLOR
        if detector.status == "预警":
            value_color = AppStyles.WARNING_COLOR
        elif detector.status == "报警":
            value_color = AppStyles.ERROR_COLOR
        value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {value_color};")
        value_layout.addWidget(value_label)
        
        unit_label = QLabel(detector.unit)
        unit_label.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 12px; padding-top: 8px;")
        value_layout.addWidget(unit_label)
        
        value_layout.addStretch()
        layout.addLayout(value_layout)
        
        bar = QProgressBar()
        percent = min(detector.current_value / detector.alarm_threshold * 100, 100)
        bar.setValue(int(percent))
        bar.setTextVisible(False)
        bar.setFixedHeight(4)
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 2px;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                border-radius: 2px;
                background-color: {value_color};
            }}
        """)
        layout.addWidget(bar)
        
        info = QLabel(f"{detector.location}")
        info.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 11px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        return panel
    
    def _build_hotwork_tab(self, layout):
        card, card_layout = self.create_card("动火作业许可管理")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        self.search_hw = self.create_search_input("搜索作业编号、地点、作业类型...")
        self.search_hw.setFixedWidth(280)
        self.search_hw.textChanged.connect(self._on_search_hw)
        toolbar_layout.addWidget(self.search_hw)
        
        self.filter_hw = QComboBox()
        self.filter_hw.addItems(["全部状态", "待审批", "进行中", "已完成", "已取消"])
        self.filter_hw.setFixedHeight(32)
        self.filter_hw.currentIndexChanged.connect(self._on_filter_hw)
        toolbar_layout.addWidget(self.filter_hw)
        
        toolbar_layout.addStretch()
        
        apply_btn = self.create_primary_button("+ 申请作业")
        apply_btn.clicked.connect(self._on_apply_hw)
        toolbar_layout.addWidget(apply_btn)
        
        approve_btn = self.create_secondary_button("审批")
        approve_btn.clicked.connect(self._on_approve_hw)
        toolbar_layout.addWidget(approve_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["许可证号", "作业地点", "作业类型", "作业内容", "申请人", 
                   "申请日期", "开始时间", "结束时间", "监护人", "状态"]
        self.hw_table = self.create_table(headers)
        self.hw_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.hw_table.doubleClicked.connect(self._on_hw_detail)
        card_layout.addWidget(self.hw_table)
        
        layout.addWidget(card)
    
    def _load_data(self):
        self.hw_table.setRowCount(0)
        hw_status_map = {
            "待审批": "warning",
            "进行中": "info",
            "已完成": "normal",
            "已取消": "error",
            "已驳回": "error",
        }
        
        for hw in self.hot_works:
            row_data = [
                hw.permit_no,
                hw.work_location,
                hw.work_type,
                hw.work_content,
                hw.applicant,
                hw.apply_date,
                hw.start_time,
                hw.end_time,
                hw.guardian,
                hw.status,
            ]
            self.add_table_row(self.hw_table, row_data, status_col=9, status_type_map=hw_status_map)
    
    def _on_search_gas(self, text):
        pass
    
    def _on_filter_gas(self):
        pass
    
    def _on_search_hw(self, text):
        text = text.lower()
        for row in range(self.hw_table.rowCount()):
            match = False
            for col in range(self.hw_table.columnCount()):
                item = self.hw_table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
            self.hw_table.setRowHidden(row, not match)
    
    def _on_filter_hw(self):
        filter_text = self.filter_hw.currentText()
        for row in range(self.hw_table.rowCount()):
            if filter_text == "全部状态":
                self.hw_table.setRowHidden(row, False)
            else:
                item = self.hw_table.item(row, 9)
                if item and item.text() == filter_text:
                    self.hw_table.setRowHidden(row, False)
                else:
                    self.hw_table.setRowHidden(row, True)
    
    def _on_apply_hw(self):
        dialog = HotWorkDialog(self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "提示", "动火作业申请提交成功！")
    
    def _on_approve_hw(self):
        current_row = self.hw_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一条待审批的记录")
            return
        item = self.hw_table.item(current_row, 9)
        if item and item.text() != "待审批":
            QMessageBox.warning(self, "提示", "只能审批状态为'待审批'的记录")
            return
        reply = QMessageBox.question(self, "审批", "确认批准该动火作业许可？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "提示", "审批通过！")
    
    def _on_hw_detail(self):
        current_row = self.hw_table.currentRow()
        if current_row < 0:
            return
        hw = self.hot_works[current_row]
        dialog = HotWorkDetailDialog(hw, self)
        dialog.exec()


class HotWorkDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("申请动火作业许可", parent)
        self._build_form()
    
    def _build_form(self):
        self.location_edit = QLineEdit()
        self.location_edit.setFixedHeight(32)
        self.add_field("作业地点", self.location_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["动火作业-焊接", "动火作业-切割", "动火作业-打磨", "动火作业-其他"])
        self.type_combo.setFixedHeight(32)
        self.add_field("作业类型", self.type_combo)
        
        self.content_edit = QTextEdit()
        self.content_edit.setFixedHeight(60)
        self.add_field("作业内容", self.content_edit)
        
        self.applicant_edit = QLineEdit()
        self.applicant_edit.setFixedHeight(32)
        self.add_field("申请人", self.applicant_edit)
        
        self.start_time = QDateTimeEdit()
        self.start_time.setCalendarPopup(True)
        self.start_time.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.start_time.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.start_time.setFixedHeight(32)
        self.add_field("开始时间", self.start_time)
        
        self.end_time = QDateTimeEdit()
        self.end_time.setCalendarPopup(True)
        self.end_time.setDateTime(QDateTime.currentDateTime().addDays(1).addSecs(8*3600))
        self.end_time.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.end_time.setFixedHeight(32)
        self.add_field("结束时间", self.end_time)
        
        self.guardian_edit = QLineEdit()
        self.guardian_edit.setFixedHeight(32)
        self.add_field("现场监护人", self.guardian_edit)


class HotWorkDetailDialog(QDialog):
    def __init__(self, hw, parent=None):
        super().__init__(parent)
        self.hw = hw
        self.setWindowTitle(f"动火作业详情 - {hw.permit_no}")
        self.setMinimumSize(550, 550)
        self.setModal(True)
        self._build_ui()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        status_type_map = {
            "待审批": "warning",
            "进行中": "info",
            "已完成": "normal",
            "已取消": "error",
        }
        status_type = status_type_map.get(self.hw.status, "normal")
        status_label = QLabel(self.hw.status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        status_label.setFixedHeight(28)
        status_label.setFixedWidth(100)
        
        title_layout = QHBoxLayout()
        title_label = QLabel(f"动火作业许可证：{self.hw.permit_no}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(status_label)
        layout.addLayout(title_layout)
        
        info_group = QGroupBox("基本信息")
        info_group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }}
        """)
        info_grid = QGridLayout(info_group)
        info_grid.setSpacing(12)
        info_grid.setContentsMargins(16, 12, 16, 12)
        
        info_items = [
            ("作业地点", self.hw.work_location),
            ("作业类型", self.hw.work_type),
            ("申请人", self.hw.applicant),
            ("申请日期", self.hw.apply_date),
            ("开始时间", self.hw.start_time),
            ("结束时间", self.hw.end_time),
            ("现场监护人", self.hw.guardian),
            ("审批人", self.hw.approver or "待审批"),
        ]
        
        for i, (label, value) in enumerate(info_items):
            row = i // 2
            col = (i % 2) * 2
            label_w = QLabel(f"{label}：")
            label_w.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY};")
            value_w = QLabel(str(value))
            value_w.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY};")
            info_grid.addWidget(label_w, row, col)
            info_grid.addWidget(value_w, row, col + 1)
        
        layout.addWidget(info_group)
        
        content_group = QGroupBox("作业内容")
        content_group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }}
        """)
        content_layout = QVBoxLayout(content_group)
        content_layout.setContentsMargins(16, 12, 16, 12)
        
        content_label = QLabel(self.hw.work_content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY};")
        content_layout.addWidget(content_label)
        
        layout.addWidget(content_group)
        
        if self.hw.remark:
            remark_group = QGroupBox("备注")
            remark_group.setStyleSheet(f"""
                QGroupBox {{
                    border: 1px solid {AppStyles.BORDER_COLOR};
                    border-radius: 4px;
                    margin-top: 12px;
                    padding-top: 10px;
                    background-color: white;
                    font-weight: bold;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 8px;
                }}
            """)
            remark_layout = QVBoxLayout(remark_group)
            remark_layout.setContentsMargins(16, 12, 16, 12)
            
            remark_label = QLabel(self.hw.remark)
            remark_label.setWordWrap(True)
            remark_label.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY};")
            remark_layout.addWidget(remark_label)
            
            layout.addWidget(remark_group)
        
        layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.setFixedHeight(32)
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #40a9ff;
            }}
        """)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
