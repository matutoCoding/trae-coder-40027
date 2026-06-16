from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QComboBox, QFrame, QGroupBox, QGridLayout,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QDoubleSpinBox, QDateEdit, QTextEdit, QTabWidget, QWidget,
    QTableWidgetItem
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QBrush

from ui.modules.base_page import BasePage, BaseDialog
from data.mock_data import MockData
from data.models import StorageTank
from ui.styles import AppStyles
from datetime import datetime


class TankLedgerPage(BasePage):
    def __init__(self):
        super().__init__("储罐台账")
        self.tanks = MockData.get_storage_tanks()
        self.tank_row_map = []
        self._build_ui()
        self.refresh_all()
    
    def _build_ui(self):
        main_layout = self.layout()
        
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(16)
        main_layout.addLayout(self.stats_row)
        
        card, card_layout = self.create_card("储罐基础台账")
        
        toolbar, toolbar_layout = self.create_toolbar()
        
        self.search_input = self.create_search_input("搜索储罐编号、名称、介质...")
        self.search_input.setFixedWidth(280)
        self.search_input.textChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.search_input)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部状态", "正常", "待检修", "停用"])
        self.filter_combo.setFixedHeight(32)
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 4px;
                padding: 4px 12px;
                background-color: white;
                min-height: 24px;
            }}
        """)
        self.filter_combo.currentIndexChanged.connect(self._apply_filters)
        toolbar_layout.addWidget(self.filter_combo)
        
        toolbar_layout.addStretch()
        
        add_btn = self.create_primary_button("+ 新增储罐")
        add_btn.clicked.connect(self._on_add_tank)
        toolbar_layout.addWidget(add_btn)
        
        edit_btn = self.create_secondary_button("编辑")
        edit_btn.clicked.connect(self._on_edit_tank)
        toolbar_layout.addWidget(edit_btn)
        
        detail_btn = self.create_secondary_button("详情")
        detail_btn.clicked.connect(self._on_detail)
        toolbar_layout.addWidget(detail_btn)
        
        card_layout.addWidget(toolbar)
        
        headers = ["储罐编号", "储罐名称", "类型", "介质", "容量(m³)", "当前液位(m)", 
                   "当前体积(m³)", "温度(℃)", "状态", "位置"]
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
        
        total_capacity = sum(t.capacity for t in self.tanks)
        total_current = sum(t.current_volume for t in self.tanks)
        normal_count = sum(1 for t in self.tanks if t.status == "正常")
        warn_count = sum(1 for t in self.tanks if t.status != "正常")
        
        card1 = self.create_stat_card("储罐总数", f"{len(self.tanks)} 个", "含固定顶、浮顶等", AppStyles.PRIMARY_COLOR)
        card2 = self.create_stat_card("总容量", f"{total_capacity:.0f} m³", "设计总容量", AppStyles.INFO_COLOR)
        card3 = self.create_stat_card("当前库存", f"{total_current:.1f} m³", f"占比 {total_current/total_capacity*100:.1f}%", AppStyles.SUCCESS_COLOR)
        card4 = self.create_stat_card("异常储罐", f"{warn_count} 个", "需关注", AppStyles.WARNING_COLOR)
        
        self.stats_row.addWidget(card1, 1)
        self.stats_row.addWidget(card2, 1)
        self.stats_row.addWidget(card3, 1)
        self.stats_row.addWidget(card4, 1)
    
    def _rebuild_table(self):
        self.table.setRowCount(0)
        self.tank_row_map = []
        status_map = {
            "正常": "normal",
            "待检修": "warning",
            "停用": "error"
        }
        
        for i, tank in enumerate(self.tanks):
            row_data = [
                tank.id,
                tank.name,
                tank.tank_type,
                tank.medium,
                f"{tank.capacity:.0f}",
                f"{tank.current_level:.2f}",
                f"{tank.current_volume:.1f}",
                f"{tank.current_temperature:.1f}",
                tank.status,
                tank.location
            ]
            self.add_table_row(self.table, row_data, status_col=8, status_type_map=status_map)
            self.tank_row_map.append(i)
    
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
                status_widget = self.table.cellWidget(row, 8)
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
                    if col == 8:
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
    
    def _get_selected_tank(self):
        current_row = self.table.currentRow()
        if current_row < 0 or current_row >= len(self.tank_row_map):
            return None
        orig_idx = self.tank_row_map[current_row]
        if 0 <= orig_idx < len(self.tanks):
            return self.tanks[orig_idx]
        return None
    
    def _on_add_tank(self):
        dialog = TankDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                tank = StorageTank(**data)
                self.tanks.append(tank)
                self.refresh_all()
                QMessageBox.information(self, "提示", "储罐添加成功！")
    
    def _on_edit_tank(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一个储罐")
            return
        
        tank = self._get_selected_tank()
        if tank is None:
            QMessageBox.warning(self, "提示", "未找到选中的储罐")
            return
        
        dialog = TankDialog(self, tank)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                for k, v in data.items():
                    if hasattr(tank, k):
                        setattr(tank, k, v)
                self.refresh_all()
                QMessageBox.information(self, "提示", "储罐信息更新成功！")
    
    def _on_detail(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一个储罐")
            return
        tank = self._get_selected_tank()
        if tank is None:
            QMessageBox.warning(self, "提示", "未找到选中的储罐")
            return
        dialog = TankDetailDialog(tank, self)
        dialog.exec()


class TankDialog(BaseDialog):
    def __init__(self, parent=None, tank=None):
        title = "编辑储罐" if tank else "新增储罐"
        super().__init__(title, parent)
        self.tank = tank
        self._build_form()
        if tank:
            self._load_data()
    
    def _build_form(self):
        self.id_edit = QLineEdit()
        self.id_edit.setFixedHeight(32)
        self.add_field("储罐编号", self.id_edit)
        
        self.name_edit = QLineEdit()
        self.name_edit.setFixedHeight(32)
        self.add_field("储罐名称", self.name_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["固定顶罐", "内浮顶罐", "外浮顶罐", "球罐", "卧式罐"])
        self.type_combo.setFixedHeight(32)
        self.add_field("储罐类型", self.type_combo)
        
        self.medium_edit = QLineEdit()
        self.medium_edit.setFixedHeight(32)
        self.add_field("储存介质", self.medium_edit)
        
        self.capacity_spin = QDoubleSpinBox()
        self.capacity_spin.setRange(0, 100000)
        self.capacity_spin.setSuffix(" m³")
        self.capacity_spin.setFixedHeight(32)
        self.add_field("设计容量", self.capacity_spin)
        
        self.material_edit = QLineEdit()
        self.material_edit.setFixedHeight(32)
        self.add_field("材质", self.material_edit)
        
        self.location_edit = QLineEdit()
        self.location_edit.setFixedHeight(32)
        self.add_field("所在位置", self.location_edit)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["正常", "待检修", "停用"])
        self.status_combo.setFixedHeight(32)
        self.add_field("状态", self.status_combo)
        
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)
        self.add_field("备注说明", self.desc_edit)
    
    def _load_data(self):
        self.id_edit.setText(self.tank.id)
        self.name_edit.setText(self.tank.name)
        self.type_combo.setCurrentText(self.tank.tank_type)
        self.medium_edit.setText(self.tank.medium)
        self.capacity_spin.setValue(self.tank.capacity)
        self.material_edit.setText(self.tank.material)
        self.location_edit.setText(self.tank.location)
        self.status_combo.setCurrentText(self.tank.status)
        self.desc_edit.setPlainText(self.tank.description)
    
    def get_data(self):
        if not self.id_edit.text().strip() or not self.name_edit.text().strip():
            QMessageBox.warning(self, "提示", "储罐编号和名称不能为空")
            return None
        
        if self.tank is not None:
            return {
                "id": self.id_edit.text().strip(),
                "name": self.name_edit.text().strip(),
                "tank_type": self.type_combo.currentText(),
                "medium": self.medium_edit.text().strip(),
                "capacity": self.capacity_spin.value(),
                "material": self.material_edit.text().strip(),
                "location": self.location_edit.text().strip(),
                "status": self.status_combo.currentText(),
                "description": self.desc_edit.toPlainText().strip(),
            }
        
        return {
            "id": self.id_edit.text().strip(),
            "name": self.name_edit.text().strip(),
            "tank_type": self.type_combo.currentText(),
            "capacity": self.capacity_spin.value(),
            "material": self.material_edit.text().strip() or "304不锈钢",
            "medium": self.medium_edit.text().strip(),
            "location": self.location_edit.text().strip(),
            "diameter": 10.0,
            "height": 10.0,
            "design_pressure": 0.1,
            "design_temperature": 50.0,
            "install_date": datetime.now().strftime("%Y-%m-%d"),
            "last_inspection_date": datetime.now().strftime("%Y-%m-%d"),
            "status": self.status_combo.currentText(),
            "current_volume": 0.0,
            "current_level": 0.0,
            "current_temperature": 20.0,
            "current_pressure": 0.05,
            "nitrogen_pressure": 0.005,
            "description": self.desc_edit.toPlainText().strip(),
        }


class TankDetailDialog(QDialog):
    def __init__(self, tank, parent=None):
        super().__init__(parent)
        self.tank = tank
        self.setWindowTitle(f"储罐详情 - {tank.name}")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        self._build_ui()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        tabs = QTabWidget()
        
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        basic_layout.setContentsMargins(0, 0, 0, 0)
        
        info_group = QGroupBox("基础信息")
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
        grid = QGridLayout(info_group)
        grid.setSpacing(12)
        grid.setContentsMargins(16, 12, 16, 12)
        
        info_items = [
            ("储罐编号", self.tank.id),
            ("储罐名称", self.tank.name),
            ("储罐类型", self.tank.tank_type),
            ("储存介质", self.tank.medium),
            ("设计容量", f"{self.tank.capacity:.0f} m³"),
            ("材质", self.tank.material),
            ("直径", f"{self.tank.diameter:.1f} m"),
            ("高度", f"{self.tank.height:.1f} m"),
            ("设计压力", f"{self.tank.design_pressure:.2f} MPa"),
            ("设计温度", f"{self.tank.design_temperature:.0f} ℃"),
            ("安装日期", self.tank.install_date),
            ("所在位置", self.tank.location),
        ]
        
        for i, (label, value) in enumerate(info_items):
            row = i // 2
            col = (i % 2) * 2
            label_w = QLabel(f"{label}：")
            label_w.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY};")
            value_w = QLabel(str(value))
            value_w.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY};")
            grid.addWidget(label_w, row, col)
            grid.addWidget(value_w, row, col + 1)
        
        basic_layout.addWidget(info_group)
        
        status_group = QGroupBox("当前状态")
        status_group.setStyleSheet(f"""
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
        status_grid = QGridLayout(status_group)
        status_grid.setSpacing(12)
        status_grid.setContentsMargins(16, 12, 16, 12)
        
        level_percent = self.tank.current_level / self.tank.height * 100 if self.tank.height > 0 else 0
        
        status_items = [
            ("当前液位", f"{self.tank.current_level:.2f} m"),
            ("当前体积", f"{self.tank.current_volume:.1f} m³"),
            ("液位占比", f"{level_percent:.1f} %"),
            ("当前温度", f"{self.tank.current_temperature:.1f} ℃"),
            ("罐内压力", f"{self.tank.current_pressure:.3f} MPa"),
            ("氮封压力", f"{self.tank.nitrogen_pressure:.4f} MPa"),
            ("运行状态", self.tank.status),
            ("上次检验", self.tank.last_inspection_date),
        ]
        
        for i, (label, value) in enumerate(status_items):
            row = i // 2
            col = (i % 2) * 2
            label_w = QLabel(f"{label}：")
            label_w.setStyleSheet(f"color: {AppStyles.TEXT_SECONDARY};")
            value_w = QLabel(str(value))
            value_w.setStyleSheet(f"color: {AppStyles.TEXT_PRIMARY};")
            status_grid.addWidget(label_w, row, col)
            status_grid.addWidget(value_w, row, col + 1)
        
        basic_layout.addWidget(status_group)
        basic_layout.addStretch()
        
        tabs.addTab(basic_tab, "基本信息")
        
        history_tab = QWidget()
        hist_layout = QVBoxLayout(history_tab)
        hist_layout.setContentsMargins(0, 0, 0, 0)
        
        hist_label = QLabel("收发明细")
        hist_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        hist_layout.addWidget(hist_label)
        
        from ui.modules.base_page import BasePage
        bp = BasePage()
        history_table = bp.create_table(["日期", "类型", "数量(m³)", "操作人"])
        history_table.setFixedHeight(250)
        
        sample_data = [
            ("2026-06-15", "收料", "+150.5", "李四"),
            ("2026-06-14", "发料", "-150.0", "张工"),
            ("2026-06-10", "收料", "+200.0", "李四"),
            ("2026-06-05", "发料", "-120.0", "张工"),
        ]
        for data in sample_data:
            row = history_table.rowCount()
            history_table.insertRow(row)
            for col, val in enumerate(data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                history_table.setItem(row, col, item)
        
        hist_layout.addWidget(history_table)
        hist_layout.addStretch()
        
        tabs.addTab(history_tab, "收发记录")
        
        layout.addWidget(tabs)
        
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
