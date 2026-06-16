from data.models import (
    StorageTank, ReceiveRecord, DispatchRecord, InspectionRecord,
    NitrogenSealRecord, GasDetector, FireFightingEquipment,
    HotWorkPermit, EmergencyDrill, LightningProtectionCheck, CofferdamRecord
)


class MockData:
    @staticmethod
    def get_storage_tanks():
        return [
            StorageTank(
                id="TK-001", name="TK-101甲醇储罐", tank_type="内浮顶罐",
                capacity=2000.0, material="304不锈钢", medium="甲醇",
                location="A罐区1号罐位", diameter=16.0, height=12.5,
                design_pressure=0.1, design_temperature=50.0,
                install_date="2020-03-15", last_inspection_date="2026-01-20",
                status="正常", current_volume=1250.5, current_level=6.8,
                current_temperature=23.5, current_pressure=0.08,
                nitrogen_pressure=0.005, description="A罐区主要储甲醇储罐"
            ),
            StorageTank(
                id="TK-002", name="TK-102乙醇储罐", tank_type="内浮顶罐",
                capacity=2000.0, material="304不锈钢", medium="乙醇",
                location="A罐区2号罐位", diameter=16.0, height=12.5,
                design_pressure=0.1, design_temperature=50.0,
                install_date="2020-03-15", last_inspection_date="2026-01-22",
                status="正常", current_volume=850.0, current_level=4.8,
                current_temperature=22.8, current_pressure=0.08,
                nitrogen_pressure=0.006, description="A罐区乙醇储罐"
            ),
            StorageTank(
                id="TK-003", name="TK-201丙酮储罐", tank_type="固定顶罐",
                capacity=1000.0, material="304不锈钢", medium="丙酮",
                location="B罐区1号罐位", diameter=12.0, height=10.0,
                design_pressure=0.15, design_temperature=45.0,
                install_date="2019-08-10", last_inspection_date="2025-12-15",
                status="正常", current_volume=680.0, current_level=7.2,
                current_temperature=24.1, current_pressure=0.05,
                nitrogen_pressure=0.004, description="B罐区丙酮储罐"
            ),
            StorageTank(
                id="TK-004", name="TK-202甲苯储罐", tank_type="内浮顶罐",
                capacity=1500.0, material="Q345R", medium="甲苯",
                location="B罐区2号罐位", diameter=14.0, height=11.0,
                design_pressure=0.1, design_temperature=50.0,
                install_date="2021-05-20", last_inspection_date="2026-02-10",
                status="正常", current_volume=1120.0, current_level=7.5,
                current_temperature=25.2, current_pressure=0.08,
                nitrogen_pressure=0.005, description="B罐区甲苯储罐"
            ),
            StorageTank(
                id="TK-005", name="TK-301硫酸储罐", tank_type="固定顶罐",
                capacity=500.0, material="碳钢衬塑", medium="硫酸(98%)",
                location="C罐区1号罐位", diameter=8.0, height=10.0,
                design_pressure=0.05, design_temperature=40.0,
                install_date="2018-11-30", last_inspection_date="2026-01-05",
                status="待检修", current_volume=320.0, current_level=6.4,
                current_temperature=26.8, current_pressure=0.02,
                nitrogen_pressure=0.0, description="C罐区硫酸储罐，近期安排检修"
            ),
            StorageTank(
                id="TK-006", name="TK-302液碱储罐", tank_type="固定顶罐",
                capacity=500.0, material="304不锈钢", medium="氢氧化钠溶液",
                location="C罐区2号罐位", diameter=8.0, height=10.0,
                design_pressure=0.05, design_temperature=60.0,
                install_date="2019-02-18", last_inspection_date="2026-01-10",
                status="正常", current_volume=280.0, current_level=5.6,
                current_temperature=28.5, current_pressure=0.02,
                nitrogen_pressure=0.0, description="C罐区液碱储罐"
            ),
        ]
    
    @staticmethod
    def get_receive_records():
        return [
            ReceiveRecord(
                id="RC-202606001", tank_id="TK-001", tank_name="TK-101甲醇储罐",
                medium="甲醇", supplier="陕西榆林化工", vehicle_no="陕K·A8865挂",
                driver="张三", receive_date="2026-06-15", receive_time="09:30",
                before_volume=1100.0, after_volume=1250.5, receive_volume=150.5,
                before_level=6.0, after_level=6.8, temperature=23.5, density=0.791,
                operator="李四", inspector="王五", status="已完成"
            ),
            ReceiveRecord(
                id="RC-202606002", tank_id="TK-004", tank_name="TK-202甲苯储罐",
                medium="甲苯", supplier="山东齐鲁石化", vehicle_no="鲁C·D3562挂",
                driver="赵六", receive_date="2026-06-14", receive_time="14:20",
                before_volume=980.0, after_volume=1120.0, receive_volume=140.0,
                before_level=6.6, after_level=7.5, temperature=25.0, density=0.866,
                operator="钱七", inspector="孙八", status="已完成"
            ),
            ReceiveRecord(
                id="RC-202606003", tank_id="TK-002", tank_name="TK-102乙醇储罐",
                medium="乙醇", supplier="江苏洋河酒精", vehicle_no="苏N·E2580挂",
                driver="周九", receive_date="2026-06-13", receive_time="11:15",
                before_volume=720.0, after_volume=850.0, receive_volume=130.0,
                before_level=4.1, after_level=4.8, temperature=22.5, density=0.789,
                operator="吴十", inspector="郑十一", status="已完成"
            ),
            ReceiveRecord(
                id="RC-202606004", tank_id="TK-003", tank_name="TK-201丙酮储罐",
                medium="丙酮", supplier="上海化工集团", vehicle_no="沪B·F7892挂",
                driver="钱十二", receive_date="2026-06-12", receive_time="16:45",
                before_volume=560.0, after_volume=680.0, receive_volume=120.0,
                before_level=6.0, after_level=7.2, temperature=24.0, density=0.784,
                operator="冯十三", inspector="陈十四", status="已完成"
            ),
            ReceiveRecord(
                id="RC-202606005", tank_id="TK-001", tank_name="TK-101甲醇储罐",
                medium="甲醇", supplier="陕西榆林化工", vehicle_no="陕K·B9987挂",
                driver="褚十五", receive_date="2026-06-16", receive_time="08:00",
                before_volume=1250.5, after_volume=0.0, receive_volume=0.0,
                before_level=6.8, after_level=0.0, temperature=0.0, density=0.0,
                operator="", inspector="", status="待检斤"
            ),
        ]
    
    @staticmethod
    def get_dispatch_records():
        return [
            DispatchRecord(
                id="DS-202606001", tank_id="TK-001", tank_name="TK-101甲醇储罐",
                medium="甲醇", customer="浙江医药股份", vehicle_no="浙A·M2023挂",
                driver="王师傅", dispatch_date="2026-06-15", dispatch_time="14:30",
                before_volume=1450.0, after_volume=1300.0, dispatch_volume=150.0,
                before_level=7.8, after_level=7.0, temperature=23.8, density=0.790,
                operator="张工", inspector="李工", status="已完成"
            ),
            DispatchRecord(
                id="DS-202606002", tank_id="TK-002", tank_name="TK-102乙醇储罐",
                medium="乙醇", customer="江苏制药厂", vehicle_no="苏B·N5678挂",
                driver="刘师傅", dispatch_date="2026-06-14", dispatch_time="10:20",
                before_volume=1050.0, after_volume=900.0, dispatch_volume=150.0,
                before_level=5.8, after_level=5.0, temperature=22.6, density=0.788,
                operator="王工", inspector="赵工", status="已完成"
            ),
            DispatchRecord(
                id="DS-202606003", tank_id="TK-004", tank_name="TK-202甲苯储罐",
                medium="甲苯", customer="上海涂料公司", vehicle_no="沪C·P9876挂",
                driver="陈师傅", dispatch_date="2026-06-13", dispatch_time="15:45",
                before_volume=1280.0, after_volume=1130.0, dispatch_volume=150.0,
                before_level=8.5, after_level=7.5, temperature=25.5, density=0.865,
                operator="周工", inspector="吴工", status="已完成"
            ),
            DispatchRecord(
                id="DS-202606004", tank_id="TK-003", tank_name="TK-201丙酮储罐",
                medium="丙酮", customer="安徽塑料厂", vehicle_no="皖A·Q3456挂",
                driver="杨师傅", dispatch_date="2026-06-12", dispatch_time="09:10",
                before_volume=820.0, after_volume=680.0, dispatch_volume=140.0,
                before_level=8.5, after_level=7.2, temperature=24.2, density=0.783,
                operator="郑工", inspector="孙工", status="已完成"
            ),
            DispatchRecord(
                id="DS-202606005", tank_id="TK-001", tank_name="TK-101甲醇储罐",
                medium="甲醇", customer="山东化工厂", vehicle_no="鲁D·R7654挂",
                driver="黄师傅", dispatch_date="2026-06-16", dispatch_time="10:00",
                before_volume=1250.5, after_volume=0.0, dispatch_volume=0.0,
                before_level=6.8, after_level=0.0, temperature=0.0, density=0.0,
                operator="", inspector="", status="待装车"
            ),
        ]
    
    @staticmethod
    def get_inspection_records():
        return [
            InspectionRecord(
                id="IN-2026061501", inspection_date="2026-06-15",
                inspection_time="08:30", inspector="李安全", location="A罐区",
                check_items=["罐区围堰", "消防通道", "防雷接地", "可燃气体报警", "应急物资"],
                abnormal_items=[], status="正常"
            ),
            InspectionRecord(
                id="IN-2026061502", inspection_date="2026-06-15",
                inspection_time="14:30", inspector="王安全", location="B罐区",
                check_items=["罐区围堰", "消防通道", "防雷接地", "可燃气体报警", "应急物资"],
                abnormal_items=["2号消防沙箱沙量不足"], status="异常"
            ),
            InspectionRecord(
                id="IN-2026061401", inspection_date="2026-06-14",
                inspection_time="08:00", inspector="张安全", location="C罐区",
                check_items=["罐区围堰", "消防通道", "防腐检查", "应急物资", "洗眼器"],
                abnormal_items=[], status="正常"
            ),
            InspectionRecord(
                id="IN-2026061402", inspection_date="2026-06-14",
                inspection_time="20:00", inspector="刘安全", location="A罐区",
                check_items=["夜间照明", "可燃气体报警", "视频监控", "氮封系统"],
                abnormal_items=["3号照明灯具故障"], status="异常"
            ),
            InspectionRecord(
                id="IN-2026061601", inspection_date="2026-06-16",
                inspection_time="08:00", inspector="李安全", location="全厂",
                check_items=["罐区围堰", "消防通道", "防雷接地", "可燃气体报警", "应急物资", "装卸站台"],
                abnormal_items=[], status="进行中"
            ),
        ]
    
    @staticmethod
    def get_nitrogen_seal_records():
        return [
            NitrogenSealRecord(
                id="NS-202606001", tank_id="TK-001", tank_name="TK-101甲醇储罐",
                record_date="2026-06-15", record_time="09:00",
                inlet_pressure=0.45, tank_pressure=0.005, set_pressure=0.005,
                valve_status="正常", operator="张工", status="正常"
            ),
            NitrogenSealRecord(
                id="NS-202606002", tank_id="TK-002", tank_name="TK-102乙醇储罐",
                record_date="2026-06-15", record_time="09:05",
                inlet_pressure=0.42, tank_pressure=0.006, set_pressure=0.005,
                valve_status="正常", operator="张工", status="正常"
            ),
            NitrogenSealRecord(
                id="NS-202606003", tank_id="TK-003", tank_name="TK-201丙酮储罐",
                record_date="2026-06-15", record_time="09:10",
                inlet_pressure=0.48, tank_pressure=0.004, set_pressure=0.005,
                valve_status="调节中", operator="李工", status="调整中"
            ),
            NitrogenSealRecord(
                id="NS-202606004", tank_id="TK-004", tank_name="TK-202甲苯储罐",
                record_date="2026-06-15", record_time="09:15",
                inlet_pressure=0.46, tank_pressure=0.005, set_pressure=0.005,
                valve_status="正常", operator="李工", status="正常"
            ),
        ]
    
    @staticmethod
    def get_gas_detectors():
        return [
            GasDetector(
                id="GD-001", location="A罐区1号罐旁", detector_type="可燃气体探测器",
                gas_type="可燃气体", current_value=12.5, alarm_threshold=25.0,
                unit="%LEL", status="正常",
                last_calibration="2026-04-10", next_calibration="2026-10-10"
            ),
            GasDetector(
                id="GD-002", location="A罐区2号罐旁", detector_type="可燃气体探测器",
                gas_type="可燃气体", current_value=8.2, alarm_threshold=25.0,
                unit="%LEL", status="正常",
                last_calibration="2026-04-12", next_calibration="2026-10-12"
            ),
            GasDetector(
                id="GD-003", location="B罐区1号罐旁", detector_type="可燃气体探测器",
                gas_type="可燃气体", current_value=28.5, alarm_threshold=25.0,
                unit="%LEL", status="报警",
                last_calibration="2026-03-20", next_calibration="2026-09-20"
            ),
            GasDetector(
                id="GD-004", location="B罐区2号罐旁", detector_type="可燃气体探测器",
                gas_type="可燃气体", current_value=15.3, alarm_threshold=25.0,
                unit="%LEL", status="正常",
                last_calibration="2026-03-22", next_calibration="2026-09-22"
            ),
            GasDetector(
                id="GD-005", location="C罐区1号罐旁", detector_type="有毒气体探测器",
                gas_type="硫酸雾", current_value=0.8, alarm_threshold=2.0,
                unit="mg/m³", status="正常",
                last_calibration="2026-02-15", next_calibration="2026-08-15"
            ),
            GasDetector(
                id="GD-006", location="装卸站台1号位", detector_type="可燃气体探测器",
                gas_type="可燃气体", current_value=22.1, alarm_threshold=25.0,
                unit="%LEL", status="预警",
                last_calibration="2026-04-05", next_calibration="2026-10-05"
            ),
            GasDetector(
                id="GD-007", location="装卸站台2号位", detector_type="可燃气体探测器",
                gas_type="可燃气体", current_value=5.6, alarm_threshold=25.0,
                unit="%LEL", status="正常",
                last_calibration="2026-04-08", next_calibration="2026-10-08"
            ),
            GasDetector(
                id="GD-008", location="罐区泵房", detector_type="可燃气体探测器",
                gas_type="可燃气体", current_value=3.2, alarm_threshold=25.0,
                unit="%LEL", status="正常",
                last_calibration="2026-04-10", next_calibration="2026-10-10"
            ),
        ]
    
    @staticmethod
    def get_fire_equipment():
        return [
            FireFightingEquipment(
                id="FE-001", name="消防泡沫罐1号", type="泡沫灭火系统",
                location="A罐区北侧", quantity=1, install_date="2020-03-10",
                last_check_date="2026-06-01", status="正常", remark="容量10立方米"
            ),
            FireFightingEquipment(
                id="FE-002", name="消防泡沫罐2号", type="泡沫灭火系统",
                location="B罐区北侧", quantity=1, install_date="2020-03-10",
                last_check_date="2026-06-01", status="正常", remark="容量10立方米"
            ),
            FireFightingEquipment(
                id="FE-003", name="消防水泵", type="消防水泵",
                location="消防泵房", quantity=2, install_date="2019-12-20",
                last_check_date="2026-06-10", status="正常"
            ),
            FireFightingEquipment(
                id="FE-004", name="干粉灭火器", type="手提式灭火器",
                location="A罐区", quantity=20, install_date="2025-10-01",
                last_check_date="2026-05-01", status="正常"
            ),
            FireFightingEquipment(
                id="FE-005", name="干粉灭火器", type="手提式灭火器",
                location="B罐区", quantity=15, install_date="2025-10-05",
                last_check_date="2026-05-05", status="正常"
            ),
            FireFightingEquipment(
                id="FE-006", name="防化服", type="个人防护装备",
                location="应急物资柜", quantity=5, install_date="2025-08-15",
                last_check_date="2026-06-01", status="正常"
            ),
            FireFightingEquipment(
                id="FE-007", name="消防沙箱", type="消防沙箱",
                location="B罐区2号", quantity=1, install_date="2020-05-10",
                last_check_date="2026-06-15", status="不足", remark="需要补充消防沙"
            ),
        ]
    
    @staticmethod
    def get_hot_work_permits():
        return [
            HotWorkPermit(
                id="HW-202606001", permit_no="HW-2026-06-001",
                work_location="B罐区2号罐旁管线", work_type="动火作业-焊接",
                work_content="焊接修复管线法兰漏点", applicant="设备部-王工",
                apply_date="2026-06-14", start_time="2026-06-15 09:00",
                end_time="2026-06-15 17:00", guardian="安全员-李师傅",
                approver="安全总监-张总", approve_date="2026-06-14",
                status="已完成"
            ),
            HotWorkPermit(
                id="HW-202606002", permit_no="HW-2026-06-002",
                work_location="装卸站台", work_type="动火作业-切割",
                work_content="切割更换旧管道", applicant="设备部-刘工",
                apply_date="2026-06-15", start_time="2026-06-17 08:00",
                end_time="2026-06-17 18:00", guardian="安全员-王师傅",
                approver="", approve_date="",
                status="待审批"
            ),
            HotWorkPermit(
                id="HW-202606003", permit_no="HW-2026-06-003",
                work_location="A罐区泵房", work_type="动火作业-打磨",
                work_content="泵体法兰面打磨修复", applicant="设备部-赵工",
                apply_date="2026-06-13", start_time="2026-06-16 14:00",
                end_time="2026-06-16 17:00", guardian="安全员-张师傅",
                approver="安全总监-张总", approve_date="2026-06-15",
                status="进行中"
            ),
        ]
    
    @staticmethod
    def get_emergency_drills():
        return [
            EmergencyDrill(
                id="ED-202601", drill_name="第一季度危化品泄漏应急演练",
                drill_type="泄漏演练", drill_date="2026-03-15",
                location="B罐区", organizer="安全部",
                participants=35, duration=2.5, status="已完成",
                summary="演练效果良好，发现应急物资配备不足问题，已整改。"
            ),
            EmergencyDrill(
                id="ED-202602", drill_name="第二季度消防灭火演练",
                drill_type="消防演练", drill_date="2026-06-10",
                location="消防训练场", organizer="安全部",
                participants=42, duration=3.0, status="已完成",
                summary="全员参与，熟练掌握灭火器使用方法和逃生技能。"
            ),
            EmergencyDrill(
                id="ED-202603", drill_name="第三季度综合应急演练",
                drill_type="综合演练", drill_date="2026-09-20",
                location="全厂", organizer="安全部",
                participants=0, duration=0.0, status="计划中"
            ),
        ]
    
    @staticmethod
    def get_lightning_checks():
        return [
            LightningProtectionCheck(
                id="LP-202601", check_date="2026-04-15",
                check_location="A罐区", inspector="市防雷检测中心",
                grounding_resistance=1.2, standard_resistance=10.0,
                equipment_status="完好", status="合格"
            ),
            LightningProtectionCheck(
                id="LP-202602", check_date="2026-04-16",
                check_location="B罐区", inspector="市防雷检测中心",
                grounding_resistance=0.8, standard_resistance=10.0,
                equipment_status="完好", status="合格"
            ),
            LightningProtectionCheck(
                id="LP-202603", check_date="2026-04-17",
                check_location="C罐区", inspector="市防雷检测中心",
                grounding_resistance=2.5, standard_resistance=10.0,
                equipment_status="完好", status="合格"
            ),
            LightningProtectionCheck(
                id="LP-202604", check_date="2026-05-20",
                check_location="装卸站台", inspector="安全部",
                grounding_resistance=3.2, standard_resistance=10.0,
                equipment_status="完好", status="合格"
            ),
        ]
    
    @staticmethod
    def get_cofferdam_records():
        return [
            CofferdamRecord(
                id="CD-202606001", record_date="2026-06-15",
                location="A罐区围堰", liquid_level=0.0,
                liquid_type="无", discharge_status="正常",
                operator="王班长", status="正常"
            ),
            CofferdamRecord(
                id="CD-202606002", record_date="2026-06-15",
                location="B罐区围堰", liquid_level=0.05,
                liquid_type="雨水", discharge_status="已排放",
                operator="李班长", status="正常"
            ),
            CofferdamRecord(
                id="CD-202606003", record_date="2026-06-14",
                location="C罐区围堰", liquid_level=0.02,
                liquid_type="雨水", discharge_status="已排放",
                operator="张班长", status="正常"
            ),
            CofferdamRecord(
                id="CD-202606004", record_date="2026-06-13",
                location="应急事故池", liquid_level=0.3,
                liquid_type="应急收集液", discharge_status="待处理",
                operator="刘班长", status="待处理",
                remark="含少量危化品，需专业处理"
            ),
        ]
