# controlmodel.py

from PyQt5.QtWidgets import QWidget, QMessageBox
from FDcontrol import Ui_Form
from debugmodel import DebugPage
from database_manager import DatabaseManager
from PyQt5.QtCore import QTimer, pyqtSignal
class ControlPage(QWidget):
    database_record_saved = pyqtSignal(dict)
    def __init__(self, debug_page: DebugPage, parent=None):
        super().__init__(parent)
        
        self.debug_page = debug_page
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.is_forward = True 

        # 初始化UI控件列表
        self.pump_addr_edits = []
        self.pump_speed_edits = []
        self.pump_enable_checkboxes = []
        # ==================== 新增代码 ====================
        self.sensor_addr_edits = []
        self.sensor_enable_checkboxes = []
        self.sensor_lcd_displays = []
        self.current_sensor_to_poll = 0 # 用于轮询的索引
        # ===============================================
        
        self._initialize_widget_lists()
        self.db_manager = DatabaseManager()
        self.db_manager.create_table()
        self.connect_signals()

        # ==================== 新增代码 ====================
        # 创建并启动用于读取传感器的定时器
        self.sensor_read_timer = QTimer(self)
        self.sensor_read_timer.timeout.connect(self.request_sensor_data)
        self.sensor_read_timer.timeout.connect(self.on_timer_tick)
        self.sensor_read_timer.start(2000) # 每5秒触发一次
        # ===============================================
        
    def _initialize_widget_lists(self):
        """初始化所有泵和传感器的UI控件列表"""
        for i in range(1, 17): # 泵相关的控件
            if i <= 16:
                self.pump_addr_edits.append(getattr(self.ui, f'lineEdit_pump_addr{i}'))
                self.pump_speed_edits.append(getattr(self.ui, f'lineEdit_sensor_speed{i}'))
                self.pump_enable_checkboxes.append(getattr(self.ui, f'checkBox_pump{i}_enable'))
            if i <= 10: # 传感器相关的控件
                self.sensor_addr_edits.append(getattr(self.ui, f'lineEdit_sensor_addr{i}'))
                self.sensor_enable_checkboxes.append(getattr(self.ui, f'checkBox_sensor{i}_enable'))
                # 注意：QLCDNumber的名字可能不同，请根据您的.ui文件确认
                self.sensor_lcd_displays.append(getattr(self.ui, f'lcdNumber_sensor{i}'))
        print("所有UI控件已初始化到列表中。")
            
    def connect_signals(self):
        # ... (泵控制按钮的连接保持不变) ...
        self.ui.pushButton_start.clicked.connect(self.on_start_clicked)
        self.ui.pushButton_stop.clicked.connect(self.on_stop_clicked)
        self.ui.pushButton_direction.clicked.connect(self.on_direction_toggled)
    
    def on_timer_tick(self):
        """定时器触发的顶层方法，负责调度数据保存和传感器轮询"""
        # 1. 检查是否需要保存数据，并执行
        self._save_data_to_db_if_enabled()
        
        # 2. 照常执行传感器数据请求
        self.request_sensor_data()

    def _save_data_to_db_if_enabled(self):
        """如果“保存到数据库”复选框被选中，则收集所有状态并保存"""
        # 检查您的新复选框，请确保其 objectName 是 'checkBox_save_data_sql'
        if not self.ui.checkBox_save_data_sql.isChecked():
            return

        # 准备一个字典来收集所有数据
        record = {}

        # 收集10个传感器的pH值
        for i in range(10):
            # QLCDNumber.value() 可以直接获取显示的数值
            ph_value = self.sensor_lcd_displays[i].value()
            record[f'sensor{i+1}_ph'] = ph_value
        
        # 收集16个泵的状态
        direction_text = "正转" if self.is_forward else "反转"
        for i in range(16):
            try:
                # 从UI读取速度，如果为空或无效则记为0
                speed = int(self.pump_speed_edits[i].text())
            except ValueError:
                speed = 0 # 无效输入时，记为0
            
            record[f'pump{i+1}_speed'] = speed
            # 方向是全局统一的
            record[f'pump{i+1}_direction'] = direction_text
            
        # 调用数据库管理器插入记录
        self.db_manager.insert_record(record)
        self.database_record_saved.emit(record)

    # ==================== 以下为新增的传感器相关方法 ====================

    def request_sensor_data(self):
        """定时器触发此方法，轮流发送读取指令给一个启用的传感器。"""
        # 搜索下一个需要读取的、已启用的传感器
        # range(10) * 2 确保能从当前位置循环一圈找到下一个
        for i in range(10):
            # 使用 % (取余) 操作实现循环索引
            idx = (self.current_sensor_to_poll + i) % 10
            
            if self.sensor_enable_checkboxes[idx].isChecked():
                addr_text = self.sensor_addr_edits[idx].text()
                if not addr_text:
                    continue
                
                try:
                    slave_addr = int(addr_text, 16)
                    # 构建读取pH值的指令 (地址0x0000, 读1个寄存器)
                    command = bytearray([slave_addr, 0x03, 0x00, 0x00, 0x00, 0x01])
                    command.extend(self.debug_page.calculate_crc16(command))
                    
                    if self._send_command(command):
                        # 发送成功后，更新下一个要轮询的索引，并退出循环
                        self.current_sensor_to_poll = (idx + 1) % 10
                        return # 本次只发送一条指令
                except ValueError:
                    continue # 地址格式错误，跳过
        # 如果循环一圈都没有找到启用的传感器，则什么都不做

    def parse_sensor_response(self, raw_data: bytes):
        """
        解析从串口收到的数据，判断是否为pH传感器的有效响应。
        这个方法被 debug_page 的 raw_data_received 信号触发。
        """
        # Modbus RTU 读响应的最小长度: 地址(1) + 功能码(1) + 字节数(1) + 数据(>=2) + CRC(2)
        if len(raw_data) < 7:
            return

        # 1. 校验CRC
        payload = raw_data[:-2]
        received_crc = raw_data[-2:]
        if self.debug_page.calculate_crc16(payload) != received_crc:
            return # CRC校验失败，不是一个有效的包

        # 2. 校验功能码和返回数据长度 (针对读pH值的响应)
        func_code = raw_data[1]
        byte_count = raw_data[2]
        if func_code != 0x03 or byte_count != 0x02:
            return # 不是我们期待的读pH响应

        # 3. 提取数据并换算
        slave_addr = raw_data[0]
        ph_integer_value = int.from_bytes(raw_data[3:5], 'big')
        ph_value = ph_integer_value / 100.0

        # 4. 找到对应的UI控件并更新
        for i in range(10):
            addr_text = self.sensor_addr_edits[i].text()
            if not addr_text: continue
            
            try:
                # 找到与返回的从机地址匹配的输入框
                if int(addr_text, 16) == slave_addr:
                    # 更新对应的LCD仪表盘
                    lcd_display = self.sensor_lcd_displays[i]
                    lcd_display.display(f"{ph_value:.2f}") # 格式化为两位小数
                    break # 找到并更新后，退出循环
            except ValueError:
                continue

    # ==================== 以下为泵控制的相关方法 (保持不变) ====================
    
    def _create_modbus_command(self, slave_addr: int, reg_addr: int, data: int) -> bytes:
        # ... (此方法保持不变) ...
        func_code = 0x06
        command = bytearray([slave_addr, func_code])
        command.extend(reg_addr.to_bytes(2, 'big'))
        command.extend(data.to_bytes(2, 'big'))
        command.extend(self.debug_page.calculate_crc16(command))
        return bytes(command)

    def _send_command(self, command: bytes):
        # ... (此方法保持不变) ...
        if not self.debug_page.serial.is_open:
            QMessageBox.warning(self, "提示", "请先在“调试模式”页面打开串口。")
            return False
        try:
            self.debug_page.serial.write(command)
            self.debug_page.log_data("TX", command)
            return True
        except Exception as e:
            QMessageBox.critical(self, "错误", f"发送指令时发生错误: {e}")
            return False

    def on_start_clicked(self):
        # ... (此方法保持不变) ...
        print("开始执行精准启动...")
        direction_data = 1 if self.is_forward else 0
        for i, addr_widget in enumerate(self.pump_addr_edits):
            if not self.pump_enable_checkboxes[i].isChecked(): continue
            speed_widget = self.pump_speed_edits[i]
            addr_text, speed_text = addr_widget.text(), speed_widget.text()
            if not addr_text or not speed_text: continue
            try:
                slave_addr = int(addr_text, 16) 
                target_speed_rpm = int(speed_text)
                speed_data = int(target_speed_rpm * 10)
                set_direction_command = self._create_modbus_command(slave_addr, 0x0001, direction_data)
                if not self._send_command(set_direction_command): continue
                set_speed_command = self._create_modbus_command(slave_addr, 0x0002, speed_data)
                if not self._send_command(set_speed_command): continue
                start_motor_command = self._create_modbus_command(slave_addr, 0x0000, 1)
                self._send_command(start_motor_command)
                print(f"已发送启动序列到地址: 0x{slave_addr:02X}")
            except ValueError:
                print(f"地址 '{addr_text}' 或速度 '{speed_text}' 无效，已跳过。")
                continue

    def on_stop_clicked(self):
        # ... (此方法保持不变) ...
        print("开始执行精准停止...")
        for i, addr_widget in enumerate(self.pump_addr_edits):
            if not self.pump_enable_checkboxes[i].isChecked(): continue
            addr_text = addr_widget.text()
            if not addr_text: continue
            try:
                slave_addr = int(addr_text, 16)
                stop_motor_command = self._create_modbus_command(slave_addr, 0x0000, 0)
                self._send_command(stop_motor_command)
                print(f"已发送停止指令到地址: 0x{slave_addr:02X}")
            except ValueError:
                print(f"地址 '{addr_text}' 无效，已跳过。")
                continue
    
    def on_direction_toggled(self):
        # ... (此方法保持不变) ...
        self.is_forward = not self.is_forward
        direction_data = 1 if self.is_forward else 0
        self.ui.pushButton_direction.setText("正转" if self.is_forward else "反转")
        for i, addr_widget in enumerate(self.pump_addr_edits):
            if not self.pump_enable_checkboxes[i].isChecked(): continue
            addr_text = addr_widget.text()
            if not addr_text: continue
            try:
                slave_addr = int(addr_text, 16)
                direction_command = self._create_modbus_command(slave_addr, 0x0001, direction_data)
                self._send_command(direction_command)
            except ValueError:
                print(f"地址 '{addr_text}' 无效，已跳过。")
                continue