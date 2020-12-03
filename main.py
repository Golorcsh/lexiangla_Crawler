# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver

from Crawler import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user_agent = "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.66Safari/537.36"
    lecture_keyword = input('请输入讲座主题关键字：')
    crawler = Crawler(user_agent=user_agent)
    crawler.get_html()
    crawler.click_lecture_button()
    crawler.find_latest_lecture(lecture_keyword)
    crawler.enroll()
