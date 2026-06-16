from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QComboBox, QFrame, QGroupBox, QGridLayout,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QDoubleSpinBox, QDateEdit, QTextEdit, QWidget, QProgressBar,
    QTabWidget, QSpinBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor

from ui.modules.base_page import BasePage, BaseDialog
from data.mock_data import MockData
from ui.styles import AppStyles


class FireControlPage(BasePage):
    def __init__(self):
        super().__init__("消防联动")
        self.equipment = MockData.get_fire_equipment()
        self.drills = MockData.get_emergency_drills()
        self.cofferdams = MockData.get_cofferdam_records()
        self._build_ui()
        self._load_data()
    
    def _build_ui(self):
        main_layout = self.layout()
        
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)
        
        total_eq = sum(e.quantity for e in self.equipment)
        normal_eq = sum(e.quantity for e in self.equipment if e.status == "正常")
        completed_drills = sum(1 for d in self.drills if d.status == "已完成")
        pending_coffer = sum(1 for c in self.cofferdams if c.status != "正常")
        
        card1 = self.create_stat_card("消防设备", f"{total_eq} 件", "设备总数", AppStyles.PRIMARY_COLOR)
        card2 = self.create_stat_card("设备完好", f"{normal_eq} 件", "正常运行", AppStyles.SUCCESS_COLOR)
        card3 = self.create_stat_card("应急演练", f"{completed_drills} 次", "本年度", AppStyles.INFO_COLOR)
        card4 = self.create_stat_card("围堰异常", f"{pending_coffer} 个", "需关注", AppStyles.WARNING_COLOR)
        
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
        
        foam_tab = QWidget()
        foam_layout = QVBoxLayout(foam_tab)
        foam_layout.setContentsMargins(0, 0, 0, 0)
        self._build_foam_tab(foam_layout)
        tabs.addTab(foam_tab, "消防泡沫联动")
        
        coffer_tab = QWidget()
        coffer_layout = QVBoxLayout(coffer_tab)
        coffer_layout.setContentsMargins(0, 0, 0, 0)
        self._build_coffer_tab(coffer_layout)
        tabs.addTab(coffer_tab, "围堰积液排放")
        
        drill_tab = QWidget()
        drill_layout = QVBoxLayout(drill_tab)
        drill_layout.setContentsMargins(0, 0, 0, 0)
        self._build_drill_tab(drill_layout)
        tabs.addTab(drill_tab, "应急预案演练")
        
        main_layout.addWidget(tabs)
    
    def _build_foam_tab(self, layout):
        card, card_layout = self.create_card("消防设备管理")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        self.search_eq = self.create_search_input("搜索设备名称、位置...")
        self.search_eq.setFixedWidth(240)
        self.search_eq.textChanged.connect(self._on_search_eq)
        toolbar_layout.addWidget(self.search_eq)
        
        self.filter_eq = QComboBox()
        self.filter_eq.addItems(["全部状态", "正常", "不足", "待检"])
        self.filter_eq.setFixedHeight(32)
        self.filter_eq.currentIndexChanged.connect(self._on_filter_eq)
        toolbar_layout.addWidget(self.filter_eq)
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 添加设备")
        add_btn.clicked.connect(self._on_add_eq)
        toolbar_layout.addWidget(add_btn)
        
        check_btn = self.create_secondary_button("检查记录")
        check_btn.clicked.connect(self._on_check_eq)
        toolbar_layout.addWidget(check_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["设备编号", "设备名称", "类型", "位置", "数量", "安装日期", "上次检查", "状态"]
        self.eq_table = self.create_table(headers)
        self.eq_table.setSelectionBehavior(QTableWidget.SelectRows)
        card_layout.addWidget(self.eq_table)
        
        layout.addWidget(card)
    
    def _build_coffer_tab(self, layout):
        card, card_layout = self.create_card("围堰积液排放记录")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 新增记录")
        add_btn.clicked.connect(self._on_add_coffer)
        toolbar_layout.addWidget(add_btn)
        
        drain_btn = self.create_secondary_button("排放处理")
        drain_btn.clicked.connect(self._on_drain_coffer)
        toolbar_layout.addWidget(drain_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["记录编号", "记录日期", "位置", "液位(m)", "液体类型", "排放状态", "操作人", "状态"]
        self.coffer_table = self.create_table(headers)
        self.coffer_table.setSelectionBehavior(QTableWidget.SelectRows)
        card_layout.addWidget(self.coffer_table)
        
        layout.addWidget(card)
    
    def _build_drill_tab(self, layout):
        card, card_layout = self.create_card("应急预案演练")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 新增演练")
        add_btn.clicked.connect(self._on_add_drill)
        toolbar_layout.addWidget(add_btn)
        
        detail_btn = self.create_secondary_button("查看详情")
        detail_btn.clicked.connect(self._on_drill_detail)
        toolbar_layout.addWidget(detail_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["演练编号", "演练名称", "类型", "演练日期", "地点", "组织部门", "参与人数", "时长(h)", "状态"]
        self.drill_table = self.create_table(headers)
        self.drill_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.drill_table.doubleClicked.connect(self._on_drill_detail)
        card_layout.addWidget(self.drill_table)
        
        layout.addWidget(card)
    
    def _load_data(self):
        self.eq_table.setRowCount(0)
        eq_status_map = {
            "正常": "normal",
            "不足": "warning",
            "待检": "info",
            "故障": "error",
        }
        
        for eq in self.equipment:
            row_data = [
                eq.id,
                eq.name,
                eq.type,
                eq.location,
                f"{eq.quantity}",
                eq.install_date,
                eq.last_check_date,
                eq.status,
            ]
            self.add_table_row(self.eq_table, row_data, status_col=7, status_type_map=eq_status_map)
        
        self.coffer_table.setRowCount(0)
        coffer_status_map = {
            "正常": "normal",
            "待处理": "warning",
            "已排放": "info",
        }
        
        for c in self.cofferdams:
            row_data = [
                c.id,
                c.record_date,
                c.location,
                f"{c.liquid_level:.2f}",
                c.liquid_type,
                c.discharge_status,
                c.operator,
                c.status,
            ]
            self.add_table_row(self.coffer_table, row_data, status_col=7, status_type_map=coffer_status_map)
        
        self.drill_table.setRowCount(0)
        drill_status_map = {
            "已完成": "normal",
            "计划中": "warning",
            "进行中": "info",
            "取消": "error",
        }
        
        for d in self.drills:
            row_data = [
                d.id,
                d.drill_name,
                d.drill_type,
                d.drill_date,
                d.location,
                d.organizer,
                f"{d.participants}",
                f"{d.duration:.1f}",
                d.status,
            ]
            self.add_table_row(self.drill_table, row_data, status_col=8, status_type_map=drill_status_map)
    
    def _on_search_eq(self, text):
        text = text.lower()
        for row in range(self.eq_table.rowCount()):
            match = False
            for col in range(self.eq_table.columnCount()):
                item = self.eq_table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
            self.eq_table.setRowHidden(row, not match)
    
    def _on_filter_eq(self):
        filter_text = self.filter_eq.currentText()
        for row in range(self.eq_table.rowCount()):
            if filter_text == "全部状态":
                self.eq_table.setRowHidden(row, False)
            else:
                item = self.eq_table.item(row, 7)
                if item and item.text() == filter_text:
                    self.eq_table.setRowHidden(row, False)
                else:
                    self.eq_table.setRowHidden(row, True)
    
    def _on_add_eq(self):
        dialog = EquipmentDialog(self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "提示", "设备添加成功！")
    
    def _on_check_eq(self):
        QMessageBox.information(self, "提示", "检查记录功能开发中...")
    
    def _on_add_coffer(self):
        dialog = CofferDialog(self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "提示", "记录添加成功！")
    
    def _on_drain_coffer(self):
        current_row = self.coffer_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一条记录")
            return
        reply = QMessageBox.question(self, "确认", "确认进行围堰积液排放处理？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "提示", "排放处理操作成功！")
    
    def _on_add_drill(self):
        dialog = DrillDialog(self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "提示", "演练计划添加成功！")
    
    def _on_drill_detail(self):
        current_row = self.drill_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一条记录")
            return
        drill = self.drills[current_row]
        dialog = DrillDetailDialog(drill, self)
        dialog.exec()


class EquipmentDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("添加消防设备", parent)
        self._build_form()
    
    def _build_form(self):
        self.name_edit = QLineEdit()
        self.name_edit.setFixedHeight(32)
        self.add_field("设备名称", self.name_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["泡沫灭火系统", "消防水泵", "手提式灭火器", "推车式灭火器", 
                                  "消防沙箱", "个人防护装备", "应急物资"])
        self.type_combo.setFixedHeight(32)
        self.add_field("设备类型", self.type_combo)
        
        self.location_edit = QLineEdit()
        self.location_edit.setFixedHeight(32)
        self.add_field("放置位置", self.location_edit)
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 1000)
        self.quantity_spin.setFixedHeight(32)
        self.add_field("数量", self.quantity_spin)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setFixedHeight(32)
        self.add_field("安装日期", self.date_edit)


class CofferDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("新增围堰记录", parent)
        self._build_form()
    
    def _build_form(self):
        self.location_combo = QComboBox()
        self.location_combo.addItems(["A罐区围堰", "B罐区围堰", "C罐区围堰", "应急事故池", "装卸区围堰"])
        self.location_combo.setFixedHeight(32)
        self.add_field("位置", self.location_combo)
        
        self.level_spin = QDoubleSpinBox()
        self.level_spin.setRange(0, 5.0)
        self.level_spin.setSuffix(" m")
        self.level_spin.setDecimals(2)
        self.level_spin.setFixedHeight(32)
        self.add_field("积液液位", self.level_spin)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["无", "雨水", "应急收集液", "含油污水", "未知液体"])
        self.type_combo.setFixedHeight(32)
        self.add_field("液体类型", self.type_combo)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["正常", "待处理"])
        self.status_combo.setFixedHeight(32)
        self.add_field("状态", self.status_combo)
        
        self.operator_edit = QLineEdit()
        self.operator_edit.setFixedHeight(32)
        self.add_field("操作人", self.operator_edit)


class DrillDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("新增应急演练", parent)
        self._build_form()
    
    def _build_form(self):
        self.name_edit = QLineEdit()
        self.name_edit.setFixedHeight(32)
        self.add_field("演练名称", self.name_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["泄漏演练", "消防演练", "综合演练", "急救演练", "疏散演练"])
        self.type_combo.setFixedHeight(32)
        self.add_field("演练类型", self.type_combo)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate().addDays(30))
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setFixedHeight(32)
        self.add_field("演练日期", self.date_edit)
        
        self.location_edit = QLineEdit()
        self.location_edit.setFixedHeight(32)
        self.add_field("演练地点", self.location_edit)
        
        self.organizer_edit = QLineEdit()
        self.organizer_edit.setFixedHeight(32)
        self.add_field("组织部门", self.organizer_edit)
        
        self.participants_spin = QSpinBox()
        self.participants_spin.setRange(1, 500)
        self.participants_spin.setFixedHeight(32)
        self.add_field("预计参与人数", self.participants_spin)


class DrillDetailDialog(QDialog):
    def __init__(self, drill, parent=None):
        super().__init__(parent)
        self.drill = drill
        self.setWindowTitle(f"演练详情 - {drill.drill_name}")
        self.setMinimumSize(500, 450)
        self.setModal(True)
        self._build_ui()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        status_type = "normal" if self.drill.status == "已完成" else "warning"
        status_label = QLabel(self.drill.status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        status_label.setFixedHeight(28)
        status_label.setFixedWidth(100)
        
        title_layout = QHBoxLayout()
        title_label = QLabel(self.drill.drill_name)
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
            ("演练编号", self.drill.id),
            ("演练类型", self.drill.drill_type),
            ("演练日期", self.drill.drill_date),
            ("演练地点", self.drill.location),
            ("组织部门", self.drill.organizer),
            ("参与人数", f"{self.drill.participants} 人"),
            ("演练时长", f"{self.drill.duration} 小时"),
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
        
        if self.drill.summary:
            summary_group = QGroupBox("演练总结")
            summary_group.setStyleSheet(f"""
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
            summary_layout = QVBoxLayout(summary_group)
            summary_layout.setContentsMargins(16, 12, 16, 12)
            
            summary_label = QLabel(self.drill.summary)
            summary_label.setWordWrap(True)
            summary_label.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY}; line-height: 1.6;")
            summary_layout.addWidget(summary_label)
            
            layout.addWidget(summary_group)
        
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
