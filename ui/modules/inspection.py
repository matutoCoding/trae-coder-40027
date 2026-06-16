from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QComboBox, QFrame, QGroupBox, QGridLayout,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QDoubleSpinBox, QDateEdit, QTextEdit, QWidget, QCheckBox,
    QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor

from ui.modules.base_page import BasePage, BaseDialog
from data.mock_data import MockData
from data.models import InspectionRecord
from ui.styles import AppStyles
from datetime import datetime


class InspectionPage(BasePage):
    def __init__(self):
        super().__init__("罐区巡检")
        self.records = MockData.get_inspection_records()
        self.lightning_checks = MockData.get_lightning_checks()
        self._build_ui()
        self.refresh_all()
    
    def _build_ui(self):
        main_layout = self.layout()
        
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(16)
        main_layout.addLayout(self.stats_row)
        
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
                padding: 8px 24px;
                margin-right: 2px;
                color: {AppStyles.TEXT_SECONDARY};
            }}
            QTabBar::tab:selected {{
                background-color: white;
                color: {AppStyles.PRIMARY_COLOR};
                border-bottom: 2px solid {AppStyles.PRIMARY_COLOR};
            }}
        """)
        
        routine_tab = QWidget()
        routine_layout = QVBoxLayout(routine_tab)
        routine_layout.setContentsMargins(0, 0, 0, 0)
        self._build_routine_tab(routine_layout)
        tabs.addTab(routine_tab, "罐区定点巡检")
        
        lightning_tab = QWidget()
        lightning_layout = QVBoxLayout(lightning_tab)
        lightning_layout.setContentsMargins(0, 0, 0, 0)
        self._build_lightning_tab(lightning_layout)
        tabs.addTab(lightning_tab, "防雷防静电检查")
        
        main_layout.addWidget(tabs)
    
    def _build_routine_tab(self, layout):
        card, card_layout = self.create_card("巡检记录")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        self.search_input = self.create_search_input("搜索巡检地点、巡检员...")
        self.search_input.setFixedWidth(280)
        self.search_input.textChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.search_input)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部状态", "正常", "异常", "进行中"])
        self.filter_combo.setFixedHeight(32)
        self.filter_combo.currentIndexChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.filter_combo)
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 新增巡检")
        add_btn.clicked.connect(self._on_add_inspection)
        toolbar_layout.addWidget(add_btn)
        
        detail_btn = self.create_secondary_button("查看详情")
        detail_btn.clicked.connect(self._on_inspection_detail)
        toolbar_layout.addWidget(detail_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["记录编号", "巡检日期", "巡检时间", "巡检员", "巡检地点", 
                   "检查项数", "异常项数", "状态"]
        self.table = self.create_table(headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self._on_inspection_detail)
        card_layout.addWidget(self.table)
        
        layout.addWidget(card)
    
    def _build_lightning_tab(self, layout):
        card, card_layout = self.create_card("防雷防静电检查记录")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 新增检查")
        add_btn.clicked.connect(self._on_add_lightning)
        toolbar_layout.addWidget(add_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["记录编号", "检查日期", "检查地点", "检测人员", 
                   "接地电阻(Ω)", "标准电阻(Ω)", "设备状态", "检查结果"]
        self.lightning_table = self.create_table(headers)
        self.lightning_table.setSelectionBehavior(QTableWidget.SelectRows)
        card_layout.addWidget(self.lightning_table)
        
        layout.addWidget(card)
    
    def _rebuild_stats(self):
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        total = len(self.records)
        normal = sum(1 for r in self.records if r.status == "正常")
        abnormal = sum(1 for r in self.records if r.status == "异常")
        ongoing = sum(1 for r in self.records if r.status == "进行中")
        
        card1 = self.create_stat_card("巡检次数", f"{total} 次", "本月巡检", AppStyles.PRIMARY_COLOR)
        card2 = self.create_stat_card("正常", f"{normal} 次", "无异常", AppStyles.SUCCESS_COLOR)
        card3 = self.create_stat_card("异常", f"{abnormal} 次", "需处理", AppStyles.ERROR_COLOR)
        card4 = self.create_stat_card("进行中", f"{ongoing} 次", "当前巡检", AppStyles.WARNING_COLOR)
        
        self.stats_row.addWidget(card1, 1)
        self.stats_row.addWidget(card2, 1)
        self.stats_row.addWidget(card3, 1)
        self.stats_row.addWidget(card4, 1)
    
    def _rebuild_table(self):
        self.table.setRowCount(0)
        status_map = {
            "正常": "normal",
            "异常": "error",
            "进行中": "warning",
        }
        
        for record in self.records:
            row_data = [
                record.id,
                record.inspection_date,
                record.inspection_time,
                record.inspector,
                record.location,
                f"{len(record.check_items)} 项",
                f"{len(record.abnormal_items)} 项",
                record.status,
            ]
            self.add_table_row(self.table, row_data, status_col=7, status_type_map=status_map)
        
        self.lightning_table.setRowCount(0)
        lt_status_map = {
            "合格": "normal",
            "不合格": "error",
        }
        
        for check in self.lightning_checks:
            row_data = [
                check.id,
                check.check_date,
                check.check_location,
                check.inspector,
                f"{check.grounding_resistance:.1f}",
                f"{check.standard_resistance:.1f}",
                check.equipment_status,
                check.status,
            ]
            self.add_table_row(self.lightning_table, row_data, status_col=7, status_type_map=lt_status_map)
    
    def refresh_all(self):
        self._rebuild_stats()
        self._rebuild_table()
        self._apply_filters()
    
    def _apply_filters(self):
        search_text = self.search_input.text().lower()
        status_filter = self.filter_combo.currentText()
        
        for row in range(self.table.rowCount()):
            status_match = True
            if status_filter != "全部状态":
                status_widget = self.table.cellWidget(row, 7)
                if status_widget:
                    status_label = status_widget.findChild(QLabel)
                    if status_label and status_label.text() != status_filter:
                        status_match = False
                else:
                    status_match = False
            
            search_match = True
            if search_text:
                found = False
                for col in range(self.table.columnCount()):
                    if col == 7:
                        w = self.table.cellWidget(row, col)
                        if w:
                            lbl = w.findChild(QLabel)
                            if lbl and search_text in lbl.text().lower():
                                found = True
                                break
                    else:
                        item = self.table.item(row, col)
                        if item and search_text in item.text().lower():
                            found = True
                            break
                search_match = found
            
            self.table.setRowHidden(row, not (status_match and search_match))
    
    def _get_selected_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return None
        visible_rows = [r for r in range(self.table.rowCount()) if not self.table.isRowHidden(r)]
        sorted_visible = sorted(visible_rows)
        if current_row in sorted_visible:
            orig_idx = sorted_visible.index(current_row)
            if orig_idx < len(self.records):
                return self.records[orig_idx]
        if current_row < len(self.records):
            return self.records[current_row]
        return None
    
    def _on_add_inspection(self):
        dialog = InspectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                now = datetime.now()
                record = InspectionRecord(
                    id=f"XJ{now.strftime('%Y%m%d%H%M%S')}",
                    inspection_date=now.strftime("%Y-%m-%d"),
                    inspection_time=now.strftime("%H:%M:%S"),
                    inspector=data["inspector"],
                    location=data["location"],
                    check_items=["设备外观", "阀门状态", "压力仪表", "液位计", "消防设施", "安全附件"],
                    abnormal_items=[],
                    status="正常",
                    remark=data["remark"]
                )
                self.records.append(record)
                self.refresh_all()
                QMessageBox.information(self, "提示", "巡检记录添加成功！")
    
    def _on_inspection_detail(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一条记录")
            return
        record = self._get_selected_record()
        if record is None:
            QMessageBox.warning(self, "提示", "未找到选中的记录")
            return
        dialog = InspectionDetailDialog(record, self)
        dialog.exec()
    
    def _on_add_lightning(self):
        QMessageBox.information(self, "提示", "功能开发中...")


class InspectionDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("新增巡检记录", parent)
        self._build_form()
    
    def _build_form(self):
        self.location_combo = QComboBox()
        self.location_combo.addItems(["A罐区", "B罐区", "C罐区", "装卸站台", "全厂", "消防泵房"])
        self.location_combo.setFixedHeight(32)
        self.add_field("巡检地点", self.location_combo)
        
        self.inspector_edit = QLineEdit()
        self.inspector_edit.setFixedHeight(32)
        self.add_field("巡检员", self.inspector_edit)
        
        self.remark_edit = QTextEdit()
        self.remark_edit.setFixedHeight(80)
        self.add_field("备注", self.remark_edit)
    
    def get_data(self):
        if not self.inspector_edit.text().strip():
            QMessageBox.warning(self, "提示", "巡检员不能为空")
            return None
        return {
            "location": self.location_combo.currentText(),
            "inspector": self.inspector_edit.text().strip(),
            "remark": self.remark_edit.toPlainText().strip(),
        }


class InspectionDetailDialog(QDialog):
    def __init__(self, record, parent=None):
        super().__init__(parent)
        self.record = record
        self.setWindowTitle(f"巡检详情 - {record.id}")
        self.setMinimumSize(500, 550)
        self.setModal(True)
        self._build_ui()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        status_type = "normal" if self.record.status == "正常" else ("error" if self.record.status == "异常" else "warning")
        status_label = QLabel(self.record.status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        status_label.setFixedHeight(28)
        status_label.setFixedWidth(100)
        
        title_layout = QHBoxLayout()
        title_label = QLabel(f"巡检记录：{self.record.id}")
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
            ("巡检地点", self.record.location),
            ("巡检员", self.record.inspector),
            ("巡检日期", self.record.inspection_date),
            ("巡检时间", self.record.inspection_time),
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
        
        check_group = QGroupBox(f"检查项目 ({len(self.record.check_items)}项)")
        check_group.setStyleSheet(f"""
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
        check_layout = QVBoxLayout(check_group)
        check_layout.setSpacing(8)
        check_layout.setContentsMargins(16, 12, 16, 12)
        
        for item in self.record.check_items:
            item_layout = QHBoxLayout()
            is_abnormal = item in self.record.abnormal_items
            icon = "⚠️" if is_abnormal else "✓"
            color = AppStyles.ERROR_COLOR if is_abnormal else AppStyles.SUCCESS_COLOR
            
            icon_label = QLabel(icon)
            icon_label.setFixedWidth(24)
            
            text_label = QLabel(item)
            text_label.setStyleSheet(f"color: {color};" if is_abnormal else f"color: {AppStyles.TEXT_PRIMARY};")
            
            status_text = "异常" if is_abnormal else "正常"
            status_type = "error" if is_abnormal else "normal"
            status_l = QLabel(status_text)
            status_l.setAlignment(Qt.AlignCenter)
            status_l.setStyleSheet(AppStyles.get_status_badge_style(status_type))
            status_l.setFixedHeight(22)
            status_l.setFixedWidth(60)
            
            item_layout.addWidget(icon_label)
            item_layout.addWidget(text_label)
            item_layout.addStretch()
            item_layout.addWidget(status_l)
            
            check_layout.addLayout(item_layout)
        
        layout.addWidget(check_group)
        
        if self.record.remark:
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
            
            remark_label = QLabel(self.record.remark)
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
