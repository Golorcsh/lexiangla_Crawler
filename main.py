"""
_*_ coding:UTF-8 _*_
Project:lexiangla
File:Pyqt
Author:Golor
Date:2020/11/27
"""
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import schedule
from Crawler import Crawler
import time


# Press the green button in the gutter to run the script.

def job(keyword: str):
    """
    执行爬虫
    :param keyword:
    :return:
    """
    crawler = Crawler()
    crawler.get_html()
    crawler.click_lecture_button()
    crawler.find_latest_lecture(keyword)
    crawler.enroll()


def get_time() -> dict:
    """
    解析输入时间，并设置返回合适时间
    :return:
    """
    t = {}
    print("输入抢讲座时间(格式为 HH:MM，例如:10:30)")
    print("输入 now 直接执行脚本(第一次运行脚本请输入now)")
    input_time = str(input("输入时间或 now :")).strip()
    if input_time == "now":
        return None
    pattern = R"(0\d|1\d|2[0-4]):([0-5]\d)"
    if re.match(pattern, input_time) is None:
        print("输入时间格式错误，格式为: HH:MM，例如:10:30")
        exit(0)
    h: int = int(input_time[0:2])
    m: int = int(input_time[3:])
    # 设置合适时间，如 09:30 -> 09:29 09:32   11:00 -> 10:59 11:02
    begin_hour: int
    begin_minus: int
    end_hour: int
    end_minus: int
    if m == 0:
        begin_hour = h - 1
        begin_minus = 59
    else:
        begin_hour = h
        begin_minus = m - 1
    end_hour = h
    end_minus = m + 2
    begin_time = str(begin_hour) + ":" + str(begin_minus)
    end_time = str(end_hour) + ":" + str(end_minus)
    if begin_hour < 10:
        begin_time = "0" + begin_time
    if end_hour < 10:
        end_time = "0" + end_time
    if begin_minus < 10:
        begin_time = begin_time[0:3] + "0" + begin_time[3:]
    if end_minus < 10:
        end_time = end_time[0:3] + "0" + end_time[3:]
    t['start'] = begin_time
    t['end'] = end_time
    return t


if __name__ == '__main__':
    # 获得开始和结束时间
    times = get_time()
    lecture_keyword = input('请输入讲座主题关键字(使用模糊匹配，建议输入完整的讲座名)：').strip()
    if times is None:  # 直接运行脚本
        job(keyword=lecture_keyword)
    else:  # 定时任务
        print('定时任务已开始,脚本将会在:{}启动,在{}自动关闭，请勿关闭程序!'.format(times['start'], times['end']))
        # schedule 添加任务
        schedule.every().day.at(times['start']).do(lambda: job(keyword=lecture_keyword))
        # schedule 添加退出任务
        schedule.every().day.at(times['end']).do(lambda: exit(0))
        while True:
            schedule.run_pending()
            time.sleep(1)
