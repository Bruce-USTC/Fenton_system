# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

# 导入你上面创建的三个页面逻辑类
from debugmodel import DebugPage
from controlmodel import ControlPage
from watchwindow import WatchPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("芬顿控制系统")
        # 设置一个足够大的默认尺寸
        self.resize(1450, 1050) 

        # --- 核心设置 ---
        # 1. 创建一个QStackedWidget实例
        self.stacked_widget = QStackedWidget()
        # 2. 将QStackedWidget设置为主窗口的中心部件
        self.setCentralWidget(self.stacked_widget)
        
        # --- 创建并添加页面 ---
        # 3. 实例化你的三个页面
        self.debug_page = DebugPage()
        self.control_page = ControlPage(debug_page=self.debug_page) 
        self.watch_page = WatchPage()
        
        # 4. 将这三个页面添加到stacked_widget中
        self.stacked_widget.addWidget(self.debug_page)     # 索引 0
        self.stacked_widget.addWidget(self.control_page)   # 索引 1
        self.stacked_widget.addWidget(self.watch_page)     # 索引 2
        self.debug_page.raw_data_received.connect(self.control_page.parse_sensor_response)
        self.control_page.database_record_saved.connect(self.watch_page.on_new_data_record)
        # --- 连接导航信号 ---
        # 5. 这是实现切换的关键
        self.connect_navigation_signals()
        
        # 6. 设置初始显示的页面
        self.go_to_debug_page()

    def connect_navigation_signals(self):
        """专门处理页面之间的跳转信号"""
        # 调试页面的跳转按钮
        self.debug_page.ui.pushButton_control_model.clicked.connect(self.go_to_control_page)
        self.debug_page.ui.pushButton_watchwindow.clicked.connect(self.go_to_watch_page)
        
        # 控制页面的跳转按钮
        # 注意: control.ui里的第一个按钮文字是"调试模式", 所以它应该跳回debug_page
        self.control_page.ui.pushButton_control_model.clicked.connect(self.go_to_debug_page)
        self.control_page.ui.pushButton_watchwindow.clicked.connect(self.go_to_watch_page)
        
        # 观测窗口的跳转按钮
        self.watch_page.ui.pushButton_debug_model.clicked.connect(self.go_to_debug_page)
        self.watch_page.ui.pushButton_control_model.clicked.connect(self.go_to_control_page)

    # --- 导航槽函数 ---
    def go_to_debug_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_control_page(self):
        self.stacked_widget.setCurrentIndex(1)
        
    def go_to_watch_page(self):
        self.stacked_widget.setCurrentIndex(2)


    def closeEvent(self, event):
        """重写关闭事件，确保所有页面的资源都被正确清理"""
        print("主窗口正在关闭，执行清理程序...")
        self.debug_page.cleanup()  # 调用DebugPage的清理方法
        # 如果其他页面也需要清理，在这里一并调用
        # self.control_page.cleanup() 
        # self.watch_page.cleanup()
        self.control_page.db_manager.close()
        event.accept() # 接受关闭事件
# --- 程序主入口 ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 创建并显示主窗口
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())