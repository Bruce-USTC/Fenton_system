# watchwindow.py

import sys
import csv
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QHeaderView, QSplitter, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import pyqtgraph as pg

from FDwatchwindow import Ui_Form

class WatchPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.model = None
        self._init_database()

        self.current_data = {'x': [], 'y': []}
        
        self.plot_widget = None
        self.plot_curve = None
        self._setup_layout_and_chart()

        self._populate_combobox()
        self.connect_signals()

    def _init_database(self):
        db = QSqlDatabase.addDatabase("QSQLITE", "watch_connection")
        db.setDatabaseName("fendun_data.db")
        if not db.open():
            print("错误: 无法建立到数据库的连接")
            return

        self.model = QSqlTableModel(self, db)
        self.model.setTable("sensor_data")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select() 

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        print("数据库模型已设置到TableView。")
        
    def _setup_layout_and_chart(self):
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('left', '数值')
        
        axis = pg.DateAxisItem(orientation='bottom')
        self.plot_widget.setAxisItems({'bottom': axis})
        self.plot_widget.setLabel('bottom', '时间')

        pen = pg.mkPen(color=(0, 0, 255), width=2)
        self.plot_curve = self.plot_widget.plot(x=[], y=[], pen=pen)

        self.plot_widget.hide()

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.ui.tableView)
        splitter.addWidget(self.plot_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.ui.layoutWidget)
        main_layout.addWidget(self.ui.layoutWidget1)
        main_layout.addWidget(splitter)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
    def _populate_combobox(self):
        if self.ui.comboBox_data.count() == 0:
            items = ["- 显示所有数据 -"]
            items.extend([f"传动泵 {i}" for i in range(1, 17)])
            items.extend([f"传感器 {i}" for i in range(1, 11)])
            self.ui.comboBox_data.addItems(items)

    def connect_signals(self):
        self.ui.comboBox_data.currentIndexChanged.connect(self.on_target_selected)
        self.ui.checkBox_chart.stateChanged.connect(self.toggle_chart_visibility)
        self.ui.pushButton_data_output.clicked.connect(self.export_data)

    def on_target_selected(self, index):
        self.update_chart_from_db()
        
        selected_text = self.ui.comboBox_data.currentText()
        
        for i in range(self.model.columnCount()):
            self.ui.tableView.setColumnHidden(i, False)

        if selected_text.startswith("传动泵"):
            pump_index = int(selected_text.split(' ')[1])
            visible_columns = {'id', 'timestamp', f'pump{pump_index}_speed', f'pump{pump_index}_direction'}
            for i in range(self.model.columnCount()):
                if self.model.headerData(i, Qt.Horizontal) not in visible_columns:
                    self.ui.tableView.setColumnHidden(i, True)
        elif selected_text.startswith("传感器"):
            sensor_index = int(selected_text.split(' ')[1])
            visible_columns = {'id', 'timestamp', f'sensor{sensor_index}_ph'}
            for i in range(self.model.columnCount()):
                if self.model.headerData(i, Qt.Horizontal) not in visible_columns:
                    self.ui.tableView.setColumnHidden(i, True)

    def toggle_chart_visibility(self, state):
        is_checked = (state == Qt.Checked)
        self.plot_widget.setVisible(is_checked)
        self.ui.tableView.setVisible(not is_checked)

    def on_new_data_record(self, record: dict):
        self.model.select()
        
        selected_text = self.ui.comboBox_data.currentText()
        if not selected_text.startswith(('传动泵', '传感器')): return

        dt_object = record.get('timestamp', datetime.now())
        x_value = dt_object.timestamp()

        if selected_text.startswith("传动泵"):
            pump_index = int(selected_text.split(' ')[1])
            key_speed, key_direction = f'pump{pump_index}_speed', f'pump{pump_index}_direction'
            if key_speed in record:
                y_value = record[key_speed] if record[key_direction] == '正转' else -record[key_speed]
                self.current_data['x'].append(x_value)
                self.current_data['y'].append(y_value)
                self.plot_curve.setData(self.current_data['x'], self.current_data['y'])
        elif selected_text.startswith("传感器"):
            sensor_index = int(selected_text.split(' ')[1])
            key_ph = f'sensor{sensor_index}_ph'
            if key_ph in record:
                y_value = record[key_ph]
                self.current_data['x'].append(x_value)
                self.current_data['y'].append(y_value)
                self.plot_curve.setData(self.current_data['x'], self.current_data['y'])

    def update_chart_from_db(self):
        selected_text = self.ui.comboBox_data.currentText()
        self.current_data = {'x': [], 'y': []} 
        
        if not selected_text.startswith(('传动泵', '传感器')):
            self.plot_curve.setData(self.current_data['x'], self.current_data['y'])
            return

        for row in range(self.model.rowCount()):
            record = self.model.record(row)
            y_value = 0
            
            timestamp_str = record.value("timestamp")
            try:
                dt_object = datetime.strptime(timestamp_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
                x_value = dt_object.timestamp()
            except (ValueError, TypeError):
                x_value = record.value("id")

            if selected_text.startswith("传动泵"):
                pump_index = int(selected_text.split(' ')[1])
                speed = record.value(f"pump{pump_index}_speed")
                direction = record.value(f"pump{pump_index}_direction")
                y_value = speed if direction == '正转' else -speed
            elif selected_text.startswith("传感器"):
                sensor_index = int(selected_text.split(' ')[1])
                y_value = record.value(f"sensor{sensor_index}_ph")
            
            self.current_data['x'].append(x_value)
            self.current_data['y'].append(y_value)
        
        print(f"为 '{selected_text}' 加载了 {len(self.current_data['x'])} 个历史数据点。")
        self.plot_curve.setData(self.current_data['x'], self.current_data['y'])

    # ==================== 核心修改：重写 export_data 方法 ====================
    def export_data(self):
        """导出数据到CSV文件。支持导出全部数据或当前选定目标的数据。"""
        selected_index = self.ui.comboBox_data.currentIndex()
        
        # 默认文件名和表头
        default_filename = "exported_data.csv"
        headers = []
        
        # 准备要写入的数据行
        rows_to_write = []

        if selected_index == 0: # 选择了 "- 显示所有数据 -"
            default_filename = "all_sensor_data.csv"
            
            # 从模型获取表头
            for i in range(self.model.columnCount()):
                headers.append(self.model.headerData(i, Qt.Horizontal))
            
            # 从模型获取所有行数据
            for row in range(self.model.rowCount()):
                row_data = [self.model.record(row).value(i) for i in range(self.model.columnCount())]
                rows_to_write.append(row_data)

        elif self.current_data['x']: # 选择了特定目标，且有数据
            selected_target = self.ui.comboBox_data.currentText().replace(" ", "_")
            default_filename = f"{selected_target}_data.csv"
            headers = ['Timestamp', 'Value']
            
            for i in range(len(self.current_data['x'])):
                readable_time = datetime.fromtimestamp(self.current_data['x'][i]).strftime('%Y-%m-%d %H:%M:%S')
                rows_to_write.append([readable_time, self.current_data['y'][i]])
        else:
            QMessageBox.warning(self, "提示", "当前没有可导出的数据。")
            return

        # 打开文件保存对话框
        file_path, _ = QFileDialog.getSaveFileName(self, "导出数据到CSV", default_filename, "CSV Files (*.csv)")
        if not file_path: return

        # 写入文件
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows_to_write)
            QMessageBox.information(self, "成功", f"数据已成功导出到:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出文件时发生错误:\n{e}")
    # =====================================================================