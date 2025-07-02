# debugmodel.py

# ------------------- 导入必要的模块 -------------------
import sys
import serial
import serial.tools.list_ports
import time
import html

from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog

from PyQt5.QtCore import QTimer, QDateTime, Qt, pyqtSignal
# 从你生成的UI文件FDdebug.py中导入Ui_Form类
from FDdebug import Ui_Form 

# ------------------- 页面逻辑类定义 -------------------
class DebugPage(QWidget):
    raw_data_received = pyqtSignal(bytes)
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # 初始化核心对象和变量
        self.serial = serial.Serial()
        self.receive_timer = QTimer(self)
        self.port_check_timer = QTimer(self)
        self.known_port_list = []
        self.auto_save_file = None
        self.color_rx = "#0000FF"
        self.color_tx = "#008000"
        self.color_info = "#808080"
        
        # 设置UI初始状态
        self.init_com_port()
        self.init_serial_params()
        
        # 连接所有信号与槽
        self.connect_signals()
        
        # 启动后台服务
        self.port_check_timer.start(1000)

    def init_com_port(self):
        port_list_info = list(serial.tools.list_ports.comports())
        self.known_port_list = [f"{p.device}：{p.description}" for p in port_list_info]
        current_selection = self.ui.comboBox_com.currentText()
        self.ui.comboBox_com.clear()
        if not self.known_port_list:
            self.ui.comboBox_com.addItem("无可用串口")
        else:
            self.ui.comboBox_com.addItems(self.known_port_list)
            if current_selection in self.known_port_list:
                self.ui.comboBox_com.setCurrentText(current_selection)
            
    def init_serial_params(self):
        if self.ui.comboBox_baud.count() == 0:
            self.ui.comboBox_baud.addItems(['9600', '19200', '38400', '57600', '115200'])
            self.ui.comboBox_baud.setCurrentText('9600') # 常用波特率
        if self.ui.comboBox_data.count() == 0:
            self.ui.comboBox_data.addItems(['8', '7', '6', '5'])
        if self.ui.comboBox_stop.count() == 0:
            self.ui.comboBox_stop.addItems(['1', '1.5', '2'])
        if self.ui.comboBox_check.count() == 0:
            self.ui.comboBox_check.addItems(['None', 'Even', 'Odd', 'Mark', 'Space'])
            self.ui.comboBox_check.setCurrentText('Even')

    def connect_signals(self):
        self.ui.pushButton_openclose.clicked.connect(self.toggle_port)
        self.ui.pushButton_send.clicked.connect(self.send_data)
        self.ui.pushButton_clean.clicked.connect(self.ui.textEdit_display.clear)
        self.ui.pushButton_cleansend.clicked.connect(self.ui.textEdit_input.clear)
        self.ui.pushButton_save.clicked.connect(self.save_log_to_file)
        self.ui.toolButton_help.clicked.connect(self.show_help_dialog)
        self.receive_timer.timeout.connect(self.receive_data)
        self.port_check_timer.timeout.connect(self.check_serial_ports)
        self.ui.checkBox_save.stateChanged.connect(self.toggle_auto_save)

    # =================================================================
    # ==================== 新增的CRC计算方法 ============================
    # =================================================================
    def calculate_crc16(self, data: bytes) -> bytes:
        """
        根据MODBUS CRC-16算法计算给定数据的CRC校验码。
        :param data: 需要计算的字节串。
        :return: 一个包含2个字节的CRC校验码的字节串 (低字节在前，高字节在后)。
        """
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:  # 检查最低位是否为1
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
        low_byte = crc & 0xFF
        high_byte = (crc >> 8) & 0xFF
        return bytes([low_byte, high_byte])
    # =================================================================

    def check_serial_ports(self):
        if not self.serial.is_open:
            current_ports_info = list(serial.tools.list_ports.comports())
            current_port_list = [f"{p.device}：{p.description}" for p in current_ports_info]
            if set(current_port_list) != set(self.known_port_list):
                self.init_com_port()

    def toggle_port(self):
        if self.serial.is_open:
            if self.ui.checkBox_save.isChecked(): self.ui.checkBox_save.setChecked(False)
            self.receive_timer.stop()
            self.serial.close()
            self.ui.pushButton_openclose.setText("打开串口")
            self.enable_settings(True)
            self.log_data("INFO", "Serial port closed.".encode())
            return
        try:
            port_text = self.ui.comboBox_com.currentText()
            if port_text == "无可用串口": raise ValueError("未选择有效的串口")
            self.serial.port = port_text.split('：')[0]
            self.serial.baudrate = int(self.ui.comboBox_baud.currentText())
            self.serial.bytesize = int(self.ui.comboBox_data.currentText())
            stop_bits_map = {'1': serial.STOPBITS_ONE, '1.5': serial.STOPBITS_ONE_POINT_FIVE, '2': serial.STOPBITS_TWO}
            self.serial.stopbits = stop_bits_map[self.ui.comboBox_stop.currentText()]
            parity_map = {'None': serial.PARITY_NONE, 'Even': serial.PARITY_EVEN, 'Odd': serial.PARITY_ODD, 'Mark': serial.PARITY_MARK, 'Space': serial.PARITY_SPACE}
            self.serial.parity = parity_map[self.ui.comboBox_check.currentText()]
            self.serial.open()
            self.serial.reset_input_buffer() 
            self.receive_timer.start(20)
            self.ui.pushButton_openclose.setText("关闭串口")
            self.enable_settings(False)
            self.log_data("INFO", f"Serial port {self.serial.port} opened successfully.".encode())
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开串口。\n{e}")

    def toggle_auto_save(self, state):
        if state == Qt.Checked:
            file_path, _ = QFileDialog.getSaveFileName(self, "选择自动保存的日志文件", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                try:
                    self.auto_save_file = open(file_path, 'a', encoding='utf-8')
                    self.auto_save_file.write(self.ui.textEdit_display.toPlainText())
                    self.log_data("INFO", f"Start automatically saving to a file: {file_path}".encode())
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"无法打开文件进行自动保存：\n{e}")
                    self.ui.checkBox_save.setChecked(False)
            else:
                self.ui.checkBox_save.setChecked(False)
        else:
            if self.auto_save_file:
                self.log_data("INFO", "Stop automatically saving file.".encode())
                self.auto_save_file.close()
                self.auto_save_file = None

    def receive_data(self):
        try:
            if self.serial.in_waiting > 0:
                time.sleep(0.015) 
                data = self.serial.read(self.serial.in_waiting)
                if data:
                    self.raw_data_received.emit(data)
                    self.log_data("RX", data)
        except Exception as e:
            self.toggle_port()

    # =================================================================
    # ==================== 修改后的send_data方法 =======================
    # =================================================================
    def send_data(self):
        if not self.serial.is_open:
            QMessageBox.warning(self, "提示", "请先打开串口。")
            return
        text_to_send = self.ui.textEdit_input.toPlainText()
        if not text_to_send:
            return
        try:
            data_to_send = b''
            if self.ui.checkBox_16send.isChecked():
                hex_str = text_to_send.replace(" ", "").replace("\n", "").replace("\r", "")
                if len(hex_str) % 2 != 0:
                    hex_str = "0" + hex_str
                data_to_send = bytes.fromhex(hex_str)
            else:
                data_to_send = text_to_send.encode('utf-8')

            # --- 这里是核心修改 ---
            if self.ui.checkBox_send_CRC_2.isChecked():
                crc_bytes = self.calculate_crc16(data_to_send)
                data_to_send += crc_bytes
                self.log_data("INFO", f"Appended CRC: {crc_bytes.hex(' ').upper()}".encode())

            self.serial.write(data_to_send)
            self.log_data("TX", data_to_send)

        except ValueError:
            QMessageBox.critical(self, "错误", "16进制格式错误。请输入有效的十六进制字符（0-9, A-F）。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"发送数据时发生错误: {e}")
    # =================================================================

    def save_log_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存日志文件", "", "Text Files (*.txt);;All Files (*)")
        if not file_path: return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.ui.textEdit_display.toPlainText())
            QMessageBox.information(self, "成功", f"日志已成功保存到：\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件时发生错误：\n{e}")
    
    def log_data(self, direction: str, data: bytes):
        plain_text = ""
        if self.ui.checkBox_time.isChecked():
            plain_text += f"[{QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss.zzz')}] "
        plain_text += f"{direction} -> "
        if direction == "INFO":
            plain_text += data.decode('utf-8', errors='ignore')
        elif self.ui.checkBox_16dispaly.isChecked():
            plain_text += ' '.join([f'{b:02X}' for b in data])
        else:
            try:
                plain_text += data.decode('utf-8')
            except UnicodeDecodeError:
                plain_text += '(Hex): ' + ' '.join([f'{b:02X}' for b in data])
        if self.auto_save_file and not self.auto_save_file.closed:
            self.auto_save_file.write(plain_text + '\n')
            self.auto_save_file.flush()
        color = {'RX': self.color_rx, 'TX': self.color_tx, 'INFO': self.color_info}.get(direction)
        self.ui.textEdit_display.append(f'<font color="{color}">{html.escape(plain_text)}</font>')

    def enable_settings(self, enable: bool):
        for widget in [self.ui.comboBox_com, self.ui.comboBox_baud, self.ui.comboBox_data, self.ui.comboBox_stop, self.ui.comboBox_check]:
            widget.setEnabled(enable)

   # 在 debugmodel.py 的 DebugPage 类中，找到并替换这个方法

# 在 DebugPage 类中添加这个方法
    def show_help_dialog(self):
        """显示一个包含使用方法的帮助对话框"""
        
        help_title = "使用帮助"
        
        help_text = """
欢迎使用串口调试工具！

【基本步骤】
1. 从“串口选择”下拉框中选择正确的COM端口。
2. 设置波特率等参数（通常默认为9600或115200）。
3. 点击“打开串口”按钮。成功后按钮会变为“关闭串口”。
4. 在下方的输入框中输入文本或16进制数据。
5. 点击“发送”按钮将数据发送出去。
6. 接收到的数据会显示在上方的数据显示区。

【特色功能】
- 16进制显示/发送: 勾选复选框后，收发的数据将按16进制格式处理。
- 时间戳: 勾选后，每条收发信息前都会附带当前时间。
- CRC校验尾补充: 勾选后，发送数据时会自动在末尾添加两位CRC-16/MODBUS校验码。
- 自动保存: 勾选后，所有通信日志将自动保存到您指定的文件中。

使用完毕后，请记得点击“关闭串口”并安全退出。
        """
        
        QMessageBox.information(self, help_title, help_text.strip())
        
    def cleanup(self):
        if self.serial.is_open:
            self.serial.close()
        if self.auto_save_file:
            self.auto_save_file.close()
        print("DebugPage资源已清理。")