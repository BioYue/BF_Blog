"""
项目配置
"""
from pathlib import Path
from utils.timed_task import spider_bing

# 基础路径
BASE_DIR = Path(__file__).resolve().parent.parent
# 开启调试模式
DEBUG = True
# 定义密钥  https://password.buyaocha.com/ 密钥生成
SECRET_KEY = 't7xbeV>RX^naH56AAYy!e-wdk}/(?dZ4r[C%hc.33TQw&n<{$q'
# 数据库连接信息
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/blog?charset=utf8mb4'

# 设置时区，时区不一致会导致定时任务的时间错误
SCHEDULER_TIMEZONE = 'Asia/Shanghai'

JOBS = [
    {
        'id': 'task1',  # 任务id
        'func': spider_bing,  # 任务执行程序
        'args': None,  # 执行程序参数
        'trigger': 'cron',
        'second': '0',
        'minute': '52',
        'hour': '18'
    }
]
