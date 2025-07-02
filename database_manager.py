# database_manager.py
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='fendun_data.db'):
        """
        初始化数据库连接。
        check_same_thread=False 是为了让数据库连接在多线程环境中更易于管理，
        虽然我们现在还没用多线程，但这是一个好习惯。
        """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        print(f"数据库 '{db_name}' 连接成功。")

    def create_table(self):
        """
        创建数据表（如果它不存在）。
        为了示例简洁，我们只创建了部分字段，您可以按需扩展。
        """
        try:
            # 使用 '''...''' 多行字符串来定义SQL语句，更清晰
            # REAL 用于存储浮点数, INTEGER 用于整数, TEXT 用于文本
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    sensor1_ph REAL,
                    sensor2_ph REAL,
                    sensor3_ph REAL,
                    sensor4_ph REAL,
                    sensor5_ph REAL,
                    sensor6_ph REAL,
                    sensor7_ph REAL,
                    sensor8_ph REAL,
                    sensor9_ph REAL,
                    sensor10_ph REAL,
                    pump1_speed INTEGER,
                    pump1_direction TEXT,
                    pump2_speed INTEGER,
                    pump2_direction TEXT,
                    pump3_speed INTEGER,
                    pump3_direction TEXT,
                    pump4_speed INTEGER,
                    pump4_direction TEXT,
                    pump5_speed INTEGER,
                    pump5_direction TEXT,
                    pump6_speed INTEGER,
                    pump6_direction TEXT,
                    pump7_speed INTEGER,
                    pump7_direction TEXT,
                    pump8_speed INTEGER,
                    pump8_direction TEXT,
                    pump9_speed INTEGER,
                    pump9_direction TEXT,
                    pump10_speed INTEGER,
                    pump10_direction TEXT,
                    pump11_speed INTEGER,
                    pump11_direction TEXT,
                    pump12_speed INTEGER,
                    pump12_direction TEXT,
                    pump13_speed INTEGER,
                    pump13_direction TEXT,
                    pump14_speed INTEGER,
                    pump14_direction TEXT,
                    pump15_speed INTEGER,
                    pump15_direction TEXT,
                    pump16_speed INTEGER,
                    pump16_direction TEXT
                )
            ''')
            self.conn.commit()
            print("数据表 'sensor_data' 创建或检查成功。")
        except Exception as e:
            print(f"创建数据表时出错: {e}")

    def insert_record(self, data_dict: dict):
        """
        将一条记录插入到数据库中。
        :param data_dict: 一个包含列名和对应值的字典。
        """
        try:
            # 自动添加当前时间戳
            data_dict['timestamp'] = datetime.now()
            
            # 使用 '?' 占位符来安全地插入数据，防止SQL注入
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['?'] * len(data_dict))
            
            sql = f"INSERT INTO sensor_data ({columns}) VALUES ({placeholders})"
            
            # 保证值的顺序与列的顺序一致
            values = [data_dict[key] for key in data_dict.keys()]
            
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"一条新记录已插入数据库: {data_dict['timestamp']}")
        except Exception as e:
            print(f"插入数据时出错: {e}")

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭。")