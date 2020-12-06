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
from selenium import webdriver

from Crawler import Crawler

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lecture_keyword = input('请输入讲座主题关键字：')
    crawler = Crawler()
    crawler.get_html()
    crawler.click_lecture_button()
    crawler.find_latest_lecture(lecture_keyword)
    crawler.enroll()
