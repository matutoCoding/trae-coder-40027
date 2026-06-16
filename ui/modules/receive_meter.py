from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QComboBox, QFrame, QGroupBox, QGridLayout,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QDoubleSpinBox, QDateEdit, QTextEdit, QTabWidget, QWidget
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor

from ui.modules.base_page import BasePage, BaseDialog
from data.mock_data import MockData
from data.models import ReceiveRecord
from ui.styles import AppStyles
from datetime import datetime


class ReceiveMeterPage(BasePage):
    def __init__(self):
        super().__init__("收料计量")
        self.records = MockData.get_receive_records()
        self._build_ui()
        self.refresh_all()
    
    def _build_ui(self):
        main_layout = self.layout()
        
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(16)
        main_layout.addLayout(self.stats_row)
        
        card, card_layout = self.create_card("进料计量记录")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        self.search_input = self.create_search_input("搜索单号、罐号、车牌号、供应商...")
        self.search_input.setFixedWidth(280)
        self.search_input.textChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.search_input)
        
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        self.date_from.setFixedHeight(32)
        self.date_from.setStyleSheet(f"""
            QDateEdit {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                padding: 4px 8px;
                background-color: white;
            }}
        """)
        self.date_from.dateChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(QLabel("从："))
        toolbar_layout.addWidget(self.date_from)
        
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        self.date_to.setFixedHeight(32)
        self.date_to.setStyleSheet(f"""
            QDateEdit {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                padding: 4px 8px;
                background-color: white;
            }}
        """)
        self.date_to.dateChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(QLabel("至："))
        toolbar_layout.addWidget(self.date_to)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部状态", "待检斤", "已完成", "待复核"])
        self.filter_combo.setFixedHeight(32)
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                padding: 4px 12px;
                background-color: white;
            }}
        """)
        self.filter_combo.currentIndexChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.filter_combo)
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 新增收料")
        add_btn.clicked.connect(self._on_add)
        toolbar_layout.addWidget(add_btn)
        
        detail_btn = self.create_secondary_button("查看详情")
        detail_btn.clicked.connect(self._on_detail)
        toolbar_layout.addWidget(detail_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["记录编号", "储罐", "介质", "供应商", "车牌号", "收料日期", 
                   "收料量(m³)", "温度(℃)", "密度", "操作人", "状态"]
        self.table = self.create_table(headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self._on_detail)
        card_layout.addWidget(self.table)
        
        main_layout.addWidget(card)
    
    def _rebuild_stats(self):
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        today = QDate.currentDate().toString("yyyy-MM-dd")
        total_volume = sum(r.receive_volume for r in self.records if r.status == "已完成")
        completed = sum(1 for r in self.records if r.status == "已完成")
        pending = sum(1 for r in self.records if r.status in ["待检斤", "待复核"])
        today_count = sum(1 for r in self.records if r.receive_date == today)
        
        card1 = self.create_stat_card("今日收料", f"{today_count} 笔", "今日收料次数", AppStyles.PRIMARY_COLOR)
        card2 = self.create_stat_card("本月累计", f"{total_volume:.1f} m³", "累计收料量", AppStyles.INFO_COLOR)
        card3 = self.create_stat_card("已完成", f"{completed} 笔", "历史记录", AppStyles.SUCCESS_COLOR)
        card4 = self.create_stat_card("待处理", f"{pending} 笔", "需要处理", AppStyles.WARNING_COLOR)
        
        self.stats_row.addWidget(card1, 1)
        self.stats_row.addWidget(card2, 1)
        self.stats_row.addWidget(card3, 1)
        self.stats_row.addWidget(card4, 1)
    
    def _rebuild_table(self):
        self.table.setRowCount(0)
        status_map = {
            "已完成": "normal",
            "待检斤": "warning",
            "待复核": "info",
            "已取消": "error",
        }
        
        for record in self.records:
            row_data = [
                record.id,
                record.tank_name,
                record.medium,
                record.supplier,
                record.vehicle_no,
                record.receive_date,
                f"{record.receive_volume:.1f}",
                f"{record.temperature:.1f}",
                f"{record.density:.3f}",
                record.operator,
                record.status,
            ]
            self.add_table_row(self.table, row_data, status_col=10, status_type_map=status_map)
    
    def refresh_all(self):
        self._rebuild_stats()
        self._rebuild_table()
        self._apply_filters()
    
    def _apply_filters(self):
        search_text = self.search_input.text().lower()
        status_filter = self.filter_combo.currentText()
        date_from = self.date_from.date().toString("yyyy-MM-dd")
        date_to = self.date_to.date().toString("yyyy-MM-dd")
        
        for row in range(self.table.rowCount()):
            status_match = True
            if status_filter != "全部状态":
                status_widget = self.table.cellWidget(row, 10)
                if status_widget:
                    status_label = status_widget.findChild(QLabel)
                    if status_label and status_label.text() != status_filter:
                        status_match = False
                else:
                    status_match = False
            
            date_match = True
            date_item = self.table.item(row, 5)
            if date_item:
                rec_date = date_item.text()
                if rec_date < date_from or rec_date > date_to:
                    date_match = False
            
            search_match = True
            if search_text:
                found = False
                for col in range(self.table.columnCount()):
                    if col == 10:
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
            
            self.table.setRowHidden(row, not (status_match and date_match and search_match))
    
    def _get_selected_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return None
        orig_indices = []
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                orig_indices.append(row)
        sorted_idx = sorted(orig_indices)
        if current_row in sorted_idx:
            real_idx = sorted_idx.index(current_row)
            if real_idx < len(self.records):
                return self.records[real_idx]
        if current_row < len(self.records):
            return self.records[current_row]
        return None
    
    def _on_add(self):
        dialog = ReceiveDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                rec = ReceiveRecord(**data)
                self.records.insert(0, rec)
                self.refresh_all()
                QMessageBox.information(self, "提示", "收料记录添加成功！")
    
    def _on_detail(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一条记录")
            return
        record = self._get_selected_record()
        if record is None:
            QMessageBox.warning(self, "提示", "未找到选中的记录")
            return
        dialog = ReceiveDetailDialog(record, self)
        dialog.exec()


class ReceiveDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("新增收料记录", parent)
        self.tanks = MockData.get_storage_tanks()
        self._build_form()
    
    def _build_form(self):
        self.tank_combo = QComboBox()
        for t in self.tanks:
            self.tank_combo.addItem(f"{t.id} - {t.name}", t)
        self.tank_combo.setFixedHeight(32)
        self.add_field("目标储罐", self.tank_combo)
        
        self.supplier_edit = QLineEdit()
        self.supplier_edit.setFixedHeight(32)
        self.add_field("供应商", self.supplier_edit)
        
        self.vehicle_edit = QLineEdit()
        self.vehicle_edit.setFixedHeight(32)
        self.add_field("车牌号", self.vehicle_edit)
        
        self.driver_edit = QLineEdit()
        self.driver_edit.setFixedHeight(32)
        self.add_field("司机", self.driver_edit)
        
        self.operator_edit = QLineEdit()
        self.operator_edit.setFixedHeight(32)
        self.add_field("操作人", self.operator_edit)
        
        self.before_spin = QDoubleSpinBox()
        self.before_spin.setRange(0, 100000)
        self.before_spin.setSuffix(" m³")
        self.before_spin.setDecimals(2)
        self.before_spin.setFixedHeight(32)
        self.add_field("收前体积", self.before_spin)
        
        self.after_spin = QDoubleSpinBox()
        self.after_spin.setRange(0, 100000)
        self.after_spin.setSuffix(" m³")
        self.after_spin.setDecimals(2)
        self.after_spin.setFixedHeight(32)
        self.add_field("收后体积", self.after_spin)
        
        self.temp_spin = QDoubleSpinBox()
        self.temp_spin.setRange(-50, 200)
        self.temp_spin.setSuffix(" ℃")
        self.temp_spin.setDecimals(1)
        self.temp_spin.setFixedHeight(32)
        self.add_field("温度", self.temp_spin)
        
        self.density_spin = QDoubleSpinBox()
        self.density_spin.setRange(0.5, 2.0)
        self.density_spin.setSuffix(" g/cm³")
        self.density_spin.setDecimals(3)
        self.density_spin.setFixedHeight(32)
        self.add_field("密度", self.density_spin)
        
        self.remark_edit = QTextEdit()
        self.remark_edit.setFixedHeight(60)
        self.add_field("备注", self.remark_edit)
    
    def get_data(self):
        tank_data = self.tank_combo.currentData()
        if tank_data is None:
            QMessageBox.warning(self, "提示", "请选择目标储罐")
            return None
        if not self.supplier_edit.text().strip():
            QMessageBox.warning(self, "提示", "请输入供应商")
            return None
        
        now = datetime.now()
        before = self.before_spin.value()
        after = self.after_spin.value()
        receive_vol = max(0.0, after - before)
        
        return {
            "id": f"RC-{now.strftime('%Y%m%d%H%M%S')}",
            "tank_id": tank_data.id,
            "tank_name": tank_data.name,
            "medium": tank_data.medium,
            "supplier": self.supplier_edit.text().strip(),
            "vehicle_no": self.vehicle_edit.text().strip(),
            "driver": self.driver_edit.text().strip(),
            "receive_date": now.strftime("%Y-%m-%d"),
            "receive_time": now.strftime("%H:%M"),
            "before_volume": before,
            "after_volume": after,
            "receive_volume": receive_vol,
            "before_level": 0.0,
            "after_level": 0.0,
            "temperature": self.temp_spin.value(),
            "density": self.density_spin.value(),
            "operator": self.operator_edit.text().strip() or "当前操作员",
            "inspector": "",
            "status": "待检斤",
            "remark": self.remark_edit.toPlainText().strip(),
        }


class ReceiveDetailDialog(QDialog):
    def __init__(self, record, parent=None):
        super().__init__(parent)
        self.record = record
        self.setWindowTitle(f"收料详情 - {record.id}")
        self.setMinimumSize(550, 500)
        self.setModal(True)
        self._build_ui()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        status_type_map = {"已完成": "normal", "待检斤": "warning", "待复核": "info", "已取消": "error"}
        status_type = status_type_map.get(self.record.status, "warning")
        status_label = QLabel(self.record.status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(AppStyles.get_status_badge_style(status_type))
        status_label.setFixedHeight(28)
        status_label.setFixedWidth(100)
        
        title_layout = QHBoxLayout()
        title_label = QLabel(f"收料记录：{self.record.id}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(status_label)
        layout.addLayout(title_layout)
        
        basic_group = QGroupBox("基本信息")
        basic_group.setStyleSheet(f"""
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
        grid = QGridLayout(basic_group)
        grid.setSpacing(12)
        grid.setContentsMargins(16, 12, 16, 12)
        
        basic_items = [
            ("储罐", self.record.tank_name),
            ("介质", self.record.medium),
            ("供应商", self.record.supplier),
            ("车牌号", self.record.vehicle_no),
            ("司机", self.record.driver),
            ("收料日期", f"{self.record.receive_date} {self.record.receive_time}"),
        ]
        
        for i, (label, value) in enumerate(basic_items):
            row = i // 2
            col = (i % 2) * 2
            label_w = QLabel(f"{label}：")
            label_w.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY};")
            value_w = QLabel(str(value))
            value_w.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY};")
            grid.addWidget(label_w, row, col)
            grid.addWidget(value_w, row, col + 1)
        
        layout.addWidget(basic_group)
        
        meter_group = QGroupBox("计量信息")
        meter_group.setStyleSheet(f"""
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
        meter_grid = QGridLayout(meter_group)
        meter_grid.setSpacing(12)
        meter_grid.setContentsMargins(16, 12, 16, 12)
        
        meter_items = [
            ("收前体积", f"{self.record.before_volume:.1f} m³"),
            ("收后体积", f"{self.record.after_volume:.1f} m³"),
            ("收料量", f"{self.record.receive_volume:.1f} m³"),
            ("收前液位", f"{self.record.before_level:.2f} m"),
            ("收后液位", f"{self.record.after_level:.2f} m"),
            ("温度", f"{self.record.temperature:.1f} ℃"),
            ("密度", f"{self.record.density:.3f} g/cm³"),
        ]
        
        for i, (label, value) in enumerate(meter_items):
            row = i // 3
            col = (i % 3) * 2
            label_w = QLabel(f"{label}：")
            label_w.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY};")
            value_w = QLabel(str(value))
            value_w.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY}; font-weight: bold;")
            meter_grid.addWidget(label_w, row, col)
            meter_grid.addWidget(value_w, row, col + 1)
        
        layout.addWidget(meter_group)
        
        op_group = QGroupBox("操作信息")
        op_group.setStyleSheet(f"""
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
        op_grid = QGridLayout(op_group)
        op_grid.setSpacing(12)
        op_grid.setContentsMargins(16, 12, 16, 12)
        
        op_items = [
            ("操作人", self.record.operator),
            ("复核人", self.record.inspector),
            ("备注", self.record.remark or "无"),
        ]
        
        for i, (label, value) in enumerate(op_items):
            label_w = QLabel(f"{label}：")
            label_w.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY};")
            value_w = QLabel(str(value))
            value_w.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY};")
            op_grid.addWidget(label_w, i, 0)
            op_grid.addWidget(value_w, i, 1)
        
        layout.addWidget(op_group)
        
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
