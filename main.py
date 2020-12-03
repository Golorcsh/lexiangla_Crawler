# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver

from Crawler import *
import json

# Press the green button in the gutter to run the script.
# chrome 开启远程调试模式
if __name__ == '__main__':
    login_url = 'https://lexiangla.com/login/'
    url = 'https://lexiangla.com/events'
    user_agent = "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.66Safari/537.36"
    # lecture_keyword = input('请输入讲座主题关键字：')
    lecture_keyword = "仰望星空，脚踏实地--对当代大学生国际视野培养的思考"
    CRAWLER = Crawler(user_agent=user_agent, login_url=login_url, url=url)
    CRAWLER.get_html()
    CRAWLER.click_lecture_button()
    CRAWLER.find_latest_lecture(lecture_keyword)
    CRAWLER.enroll()
