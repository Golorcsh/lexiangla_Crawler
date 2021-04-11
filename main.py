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


if __name__ == '__main__':
    lecture_keyword = input('请输入讲座主题关键字：')
    # 测试
    # job(keyword=lecture_keyword)

    print('请选择抢讲座时间：')
    print('1 12:00讲座')
    print('2 17:00讲座')
    time_mode = int(input("请输入选择："))
    start_times = {
        1: '11:59:20',
        2: '16:59:20',
    }
    end_times = {
        1: '12:00:30',
        2: '17:00:30',
    }
    print('定时任务已开始')
    # schedule 添加任务
    schedule.every().day.at(start_times[time_mode]).do(lambda: job(keyword=lecture_keyword))
    # schedule 添加退出任务
    schedule.every().day.at(end_times[time_mode]).do(lambda: exit(0))

    while True:
        schedule.run_pending()
        time.sleep(1)
