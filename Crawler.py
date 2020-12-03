from selenium import webdriver
from time import *
import json
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from requests import request


class Crawler:
    cookies = {}
    user_agent = ''
    login_url = 'https://lexiangla.com/login/'
    url = 'https://lexiangla.com/events'

    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.option = webdriver.ChromeOptions()
        # 添加User_Agent
        self.option.add_argument(self.user_agent)
        # 谷歌文档提到需要加上这个属性来规避bug
        self.option.add_argument('--disable-gpu')
        # 禁用浏览器正在被自动化程序控制的提示
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 新建chrome浏览器变量
        self.driver = webdriver.Chrome(options=self.option)
        # 最大化浏览器
        self.driver.maximize_window()
        # 判断cookie文件是否存在，不存在先登录获取cookie
        if not self.cookie_exist():
            self.login_and_save_cookies()

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
        self.driver.implicitly_wait(2)
        self.driver.find_element('link text', '讲座').click()

    def find_latest_lecture(self, lecture_keyword):
        """输入讲座标题，搜索标题，查询符合元素，获取该讲座的链接，进入讲座具体页面"""
        lecture = None
        # 通话标题关键字获得讲座链接
        while lecture is None:
            if lecture:
                break
            try:
                lecture = self.driver.find_element('partial link text', lecture_keyword)
                self.driver.get(lecture.get_attribute('href'))
            except NoSuchElementException as error:
                print('未找到讲座,刷新页面')
            self.driver.refresh()

    def enroll(self):
        xpath = "//div[@class='mt-l']/button[@class='btn btn-primary btn-lg']"
        xpath1 = "//div[@class='mt-l']/span[@class='secondary']"
        self.driver.implicitly_wait(2)
        button = None
        while button is None:
            try:
                web_element_button = self.driver.find_element_by_xpath(xpath).click()
            except NoSuchElementException as error:
                print('未找到报名按钮')

            inform = self.driver.find_element_by_xpath(xpath1)
            if button or inform:
                print(inform.text)
                break
