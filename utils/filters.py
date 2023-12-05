from datetime import datetime


def strftime(date):
    # 格式化日期和时间
    return date.strftime('%y年 %m月%d日 %H:%M')


FILTERS = {
    'strftime': strftime
}
