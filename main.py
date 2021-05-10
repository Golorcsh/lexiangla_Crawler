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
import schedule
from Crawler import Crawler
import time


# Press the green button in the gutter to run the script.

def job(keyword):
    crawler = Crawler()
    crawler.get_html()
    crawler.click_lecture_button()
    crawler.find_latest_lecture(keyword)
    crawler.enroll()


def get_time() -> dict:
    times = {}
    input_time = input('请输入抢讲座时间：')
    begin_minute = ':59'
    begin_second = ':15'
    start_time = str(int(input_time) - 1) + begin_minute + begin_second

    end_minute = ':00'
    end_second = ':20'
    end_time = input_time + end_minute + end_second

    times['start'] = start_time
    times['end'] = end_time

    return times


if __name__ == '__main__':
    lecture_keyword = input('请输入讲座主题关键字：')
    # 测试例子
    # job(keyword=lecture_keyword)

    # 获得开始和结束时间
    times = get_time()
    print('定时任务已开始')
    # schedule 添加任务
    schedule.every().day.at(times['start']).do(lambda: job(keyword=lecture_keyword))
    # schedule 添加退出任务
    schedule.every().day.at(times['end']).do(lambda: exit(0))

    while True:
        schedule.run_pending()
        time.sleep(1)
