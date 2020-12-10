"""
_*_ coding:UTF-8 _*_
Project:lexiangla
File:Pyqt
Author:Golor
Date:2020/11/27
"""
from selenium import webdriver
from time import *
import json
import os
from selenium.common.exceptions import NoSuchElementException


class Crawler:
    cookies = {}
    login_url = 'https://lexiangla.com/login/'
    url = 'https://lexiangla.com/events'
    user_agent = 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.66Safari/537.36'

    def __init__(self, ):
        self.option = webdriver.ChromeOptions()
        # 添加User_Agent
        self.option.add_argument(self.user_agent)
        # 无界面模式
        self.option.add_argument('headless')
        # 无图模式
        self.option.add_argument('blink-settings=imagesEnabled=false')
        # 谷歌文档提到需要加上这个属性来规避bug
        self.option.add_argument('--disable-gpu')
        # 禁用浏览器正在被自动化程序控制的提示
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 新建chrome浏览器变量
        self.driver = webdriver.Chrome(options=self.option)
        # 最大化浏览器
        # self.driver.maximize_window()
        # 判断cookie文件是否存在，不存在先登录获取cookie
        if not self.cookie_exist():
            self.login_and_save_cookies()
            sleep(5)

    def login_and_save_cookies(self):
        """打开登陆页面，登陆后抓取cookies信息保存下来以便之后自动登陆使用"""
        print('cookie文件不存在，请先扫描登录')
        self.driver.get(self.login_url)
        # 暂停10秒扫码登录
        sleep(10)
        # 登录后获得cookies
        self.cookies = self.driver.get_cookies()
        # 保存cookies信息到文件中
        file = open('cookies', 'w')
        file.write(json.dumps(self.cookies))
        file.close()
        print("cookies获取成功，保存cookies文件")

    @staticmethod
    def cookie_exist():
        """判断cookies文件是否存在"""
        if os.path.exists('cookies'):
            return True
        else:
            return False

    def get_cookie(self):
        """打开读取cookie文件，返回cookie"""
        if self.cookie_exist():
            print("cookies文件存在")
            # 获得cookies
            file = open('cookies', 'r')
            cookie = json.loads(file.read())[-1]
            file.close()
            print("读取cookie，返回cookie")
            return cookie

    def get_html(self):
        """进入腾讯乐享活动界面"""
        self.driver.get(self.url)
        self.driver.add_cookie(cookie_dict=self.get_cookie())
        print("浏览器添加cookie信息，进入活动界面")
        self.driver.get(self.url)
        print("进入讲座列表页面")

    def click_lecture_button(self):
        """点击'讲座'关键字，进入讲座列表界面"""
        # 隐式加载界面,在进行查询元素前，如果还有未加载完，再等5秒
        self.driver.implicitly_wait(1)
        self.driver.find_element('link text', '讲座').click()

    def find_latest_lecture(self, lecture_keyword) -> bool:
        """输入讲座标题，搜索标题，查询符合元素，获取该讲座的链接，进入讲座具体页面"""
        lecture = None
        refresh_times = 0
        # 通话标题关键字获得讲座链接
        while lecture is None:
            refresh_times += 1
            try:
                lecture = self.driver.find_element('partial link text', lecture_keyword)
                self.driver.get(lecture.get_attribute('href'))
                return True
            except NoSuchElementException as error:
                self.driver.refresh()
                print('第' + str(refresh_times) + '次查询，未找到讲座，刷新页面')
        return False

    def enroll(self) -> bool:
        """在讲座详细页面中查找报名按钮，并点击"""
        # 报名按钮的xpath
        button_xpath = "//div[@class='mt-l']/button[@class='btn btn-primary btn-lg']"
        # 超时后，报名按钮的xpath
        overtime_button_xpath = "//div[@class='mt-l']/span[@class='secondary']"
        try:
            self.driver.find_element_by_xpath(button_xpath).click()
            print('已报名')
        except NoSuchElementException as error:
            try:
                inform = self.driver.find_element_by_xpath(overtime_button_xpath)
                print(inform.text)
            except NoSuchElementException as error:
                print('讲座已结束')
                return False
        return True
