from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QComboBox, QFrame, QGroupBox, QGridLayout,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QDoubleSpinBox, QDateEdit, QTextEdit, QWidget, QProgressBar,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QColor, QFont

from ui.modules.base_page import BasePage, BaseDialog
from data.mock_data import MockData
from data.models import NitrogenSealRecord
from ui.styles import AppStyles
from datetime import datetime


class NitrogenSealPage(BasePage):
    def __init__(self):
        super().__init__("氮封惰化")
        self.records = MockData.get_nitrogen_seal_records()
        self.tanks = MockData.get_storage_tanks()
        self._build_ui()
        self.refresh_all()
    
    def _build_ui(self):
        main_layout = self.layout()
        
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(16)
        main_layout.addLayout(self.stats_row)
        
        monitor_card, monitor_layout = self.create_card("氮封压力实时监控")
        
        self.tank_panels = []
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(16)
        
        nitrogen_tanks_list = [t for t in self.tanks if t.nitrogen_pressure > 0]
        for i, tank in enumerate(nitrogen_tanks_list[:4]):
            panel = self._create_tank_panel(tank)
            panels_layout.addWidget(panel, 1)
            self.tank_panels.append(panel)
        
        monitor_layout.addLayout(panels_layout)
        main_layout.addWidget(monitor_card)
        
        card, card_layout = self.create_card("氮封压力控制记录")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        self.search_input = self.create_search_input("搜索储罐名称...")
        self.search_input.setFixedWidth(240)
        self.search_input.textChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.search_input)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部状态", "正常", "调整中", "异常"])
        self.filter_combo.setFixedHeight(32)
        self.filter_combo.currentIndexChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.filter_combo)
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 记录压力")
        add_btn.clicked.connect(self._on_add_record)
        toolbar_layout.addWidget(add_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["记录编号", "储罐", "记录日期", "记录时间", "进口压力(MPa)", 
                   "罐内压力(MPa)", "设定压力(MPa)", "阀门状态", "操作人", "状态"]
        self.table = self.create_table(headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        card_layout.addWidget(self.table)
        
        main_layout.addWidget(card)
    
    def _create_tank_panel(self, tank):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border-color: {AppStyles.PRIMARY_COLOR};
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        name_label = QLabel(tank.name)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        medium_label = QLabel(tank.medium)
        medium_label.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 12px;")
        medium_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(medium_label)
        
        pressure_bar_container = QWidget()
        bar_layout = QVBoxLayout(pressure_bar_container)
        bar_layout.setContentsMargins(0, 10, 0, 10)
        bar_layout.setSpacing(8)
        
        pressure_value = QLabel(f"{tank.nitrogen_pressure:.4f}")
        pressure_value.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {AppStyles.PRIMARY_COLOR};")
        pressure_value.setAlignment(Qt.AlignCenter)
        bar_layout.addWidget(pressure_value)
        
        pressure_unit = QLabel("MPa")
        pressure_unit.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 12px;")
        pressure_unit.setAlignment(Qt.AlignCenter)
        bar_layout.addWidget(pressure_unit)
        
        layout.addWidget(pressure_bar_container)
        
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_percent = min(tank.nitrogen_pressure / 0.01 * 100, 100)
        progress_bar.setValue(int(progress_percent))
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(6)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 3px;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                border-radius: 3px;
                background-color: {AppStyles.SUCCESS_COLOR};
            }}
        """)
        layout.addWidget(progress_bar)
        
        info_grid = QGridLayout()
        info_grid.setSpacing(6)
        
        labels = ["设定值", "进口压", "状态"]
        values = [
            "0.005 MPa",
            "0.45 MPa",
            "正常"
        ]
        
        for i in range(3):
            label = QLabel(labels[i])
            label.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY}; font-size: 11px;")
            label.setAlignment(Qt.AlignCenter)
            value = QLabel(values[i])
            value.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY}; font-size: 11px; font-weight: bold;")
            value.setAlignment(Qt.AlignCenter)
            info_grid.addWidget(label, 0, i)
            info_grid.addWidget(value, 1, i)
        
        layout.addLayout(info_grid)
        
        return panel
    
    def _rebuild_stats(self):
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        nitrogen_tanks = [t for t in self.tanks if t.nitrogen_pressure > 0]
        normal_count = sum(1 for r in self.records if r.status == "正常")
        adjust_count = sum(1 for r in self.records if r.status == "调整中")
        avg_pressure = sum(r.tank_pressure for r in self.records) / len(self.records) if self.records else 0
        
        card1 = self.create_stat_card("氮封储罐", f"{len(nitrogen_tanks)} 个", "需氮封保护", AppStyles.PRIMARY_COLOR)
        card2 = self.create_stat_card("压力正常", f"{normal_count} 个", "氮封系统正常", AppStyles.SUCCESS_COLOR)
        card3 = self.create_stat_card("调节中", f"{adjust_count} 个", "正在调整压力", AppStyles.WARNING_COLOR)
        card4 = self.create_stat_card("平均压力", f"{avg_pressure:.4f} MPa", "罐内平均压力", AppStyles.INFO_COLOR)
        
        self.stats_row.addWidget(card1, 1)
        self.stats_row.addWidget(card2, 1)
        self.stats_row.addWidget(card3, 1)
        self.stats_row.addWidget(card4, 1)
    
    def _rebuild_table(self):
        self.table.setRowCount(0)
        status_map = {
            "正常": "normal",
            "调整中": "warning",
            "异常": "error",
        }
        
        for record in self.records:
            row_data = [
                record.id,
                record.tank_name,
                record.record_date,
                record.record_time,
                f"{record.inlet_pressure:.2f}",
                f"{record.tank_pressure:.4f}",
                f"{record.set_pressure:.4f}",
                record.valve_status,
                record.operator,
                record.status,
            ]
            self.add_table_row(self.table, row_data, status_col=9, status_type_map=status_map)
    
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
                status_widget = self.table.cellWidget(row, 9)
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
                    if col == 9:
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
    
    def _on_add_record(self):
        dialog = NitrogenRecordDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                now = datetime.now()
                tank = next((t for t in self.tanks if t.id == data["tank_id"]), None)
                tank_name = tank.name if tank else data["tank_id"]
                record = NitrogenSealRecord(
                    id=f"NF{now.strftime('%Y%m%d%H%M%S')}",
                    tank_id=data["tank_id"],
                    tank_name=tank_name,
                    record_date=now.strftime("%Y-%m-%d"),
                    record_time=now.strftime("%H:%M:%S"),
                    inlet_pressure=data["inlet_pressure"],
                    tank_pressure=data["tank_pressure"],
                    set_pressure=data["set_pressure"],
                    valve_status=data["valve_status"],
                    operator=data["operator"],
                    status="正常" if data["valve_status"] == "正常" else "调整中"
                )
                self.records.append(record)
                self.refresh_all()
                QMessageBox.information(self, "提示", "压力记录添加成功！")


class NitrogenRecordDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("新增氮封压力记录", parent)
        self._build_form()
    
    def _build_form(self):
        self.tank_combo = QComboBox()
        tanks = [t for t in MockData.get_storage_tanks() if t.nitrogen_pressure > 0]
        for t in tanks:
            self.tank_combo.addItem(f"{t.id} - {t.name}", t.id)
        self.tank_combo.setFixedHeight(32)
        self.add_field("储罐", self.tank_combo)
        
        self.inlet_spin = QDoubleSpinBox()
        self.inlet_spin.setRange(0, 1.0)
        self.inlet_spin.setSuffix(" MPa")
        self.inlet_spin.setDecimals(2)
        self.inlet_spin.setSingleStep(0.01)
        self.inlet_spin.setValue(0.45)
        self.inlet_spin.setFixedHeight(32)
        self.add_field("进口压力", self.inlet_spin)
        
        self.tank_spin = QDoubleSpinBox()
        self.tank_spin.setRange(0, 0.1)
        self.tank_spin.setSuffix(" MPa")
        self.tank_spin.setDecimals(4)
        self.tank_spin.setSingleStep(0.0005)
        self.tank_spin.setValue(0.005)
        self.tank_spin.setFixedHeight(32)
        self.add_field("罐内压力", self.tank_spin)
        
        self.set_spin = QDoubleSpinBox()
        self.set_spin.setRange(0, 0.1)
        self.set_spin.setSuffix(" MPa")
        self.set_spin.setDecimals(4)
        self.set_spin.setSingleStep(0.0005)
        self.set_spin.setValue(0.005)
        self.set_spin.setFixedHeight(32)
        self.add_field("设定压力", self.set_spin)
        
        self.valve_combo = QComboBox()
        self.valve_combo.addItems(["正常", "调节中", "关闭"])
        self.valve_combo.setFixedHeight(32)
        self.add_field("阀门状态", self.valve_combo)
        
        self.operator_edit = QLineEdit()
        self.operator_edit.setFixedHeight(32)
        self.add_field("操作人", self.operator_edit)
    
    def get_data(self):
        if not self.operator_edit.text().strip():
            QMessageBox.warning(self, "提示", "操作人不能为空")
            return None
        return {
            "tank_id": self.tank_combo.currentData(),
            "inlet_pressure": self.inlet_spin.value(),
            "tank_pressure": self.tank_spin.value(),
            "set_pressure": self.set_spin.value(),
            "valve_status": self.valve_combo.currentText(),
            "operator": self.operator_edit.text().strip(),
        }
