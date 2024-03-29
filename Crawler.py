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
import datetime


class Crawler:
    driver_path = './chromedriver.exe'
    login_url = 'https://lexiangla.com/login?use_workwechat=1'
    events_url = 'https://lexiangla.com/events'
    user_agent = 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.66Safari/537.36'
    current_window = None

    def __init__(self, ):
        self.option = webdriver.ChromeOptions()
        # 添加User_Agent
        self.option.add_argument(self.user_agent)
        # 谷歌文档提到需要加上这个属性来规避bug
        self.option.add_argument('--disable-gpu')
        # 禁用浏览器正在被自动化程序控制的提示
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        if not self.cookie_exist():
            # 判断cookie文件是否存在，不存在先登录获取cookie
            # 新建chrome浏览器变量
            self.driver = webdriver.Chrome(options=self.option, executable_path=self.driver_path)
            self.login_and_save_cookies()
            print('请重新运行程序！程序将会在5秒后退出。')
            sleep(5)
            self.driver.close()
            exit(0)
        else:
            # 若cookie文件存在，则设置浏览器为无界面、无图片模式
            # 无界面模式
            self.option.add_argument('headless')
            # 无图模式
            self.option.add_argument('blink-settings=imagesEnabled=false')
            # 新建chrome浏览器变量
            self.driver = webdriver.Chrome(options=self.option, executable_path=self.driver_path)

    def login_and_save_cookies(self):
        """打开登陆页面，登陆后抓取cookies信息保存下来以便之后自动登陆使用"""
        self.driver.get(self.login_url)

        # 判断是否已经扫码登录
        current_url = self.driver.current_url
        print('请扫码登录')
        while current_url == self.driver.current_url:
            print('*', end='')
            sleep(1)
        print('')

        # 登录后获得cookies
        cookies = self.driver.get_cookies()
        # 保存cookies信息到文件中
        file = open('cookies', 'w')
        file.write(json.dumps(cookies))
        file.close()
        print("cookies获取成功，保存cookies文件")

    @staticmethod
    def cookie_exist():
        """判断cookies文件是否存在"""
        if os.path.exists('cookies'):
            return True
        else:
            print('cookies文件不存在，请先扫描登录')
            return False

    @staticmethod
    def delete_cookie():
        """判断cookies文件是否存在，如果存在则删除cookie"""
        if os.path.exists('cookies'):
            os.remove('cookies')

    @staticmethod
    def cookie_is_expired(cookie_time) -> bool:
        """判断cookie时间是否有效"""
        cookie_time = datetime.datetime.fromtimestamp(cookie_time)
        now_time = datetime.datetime.now()
        if cookie_time > now_time:
            print("读取cookie，cookie有效，有效期至：", cookie_time.strftime("%Y-%m-%d %H:%M:%S"), "，返回cookie")
            return False
        else:
            return True

    def get_cookie(self):
        """打开读取cookie文件，返回cookie"""
        if self.cookie_exist():
            print("cookie文件存在")
            # 获得cookies
            file = open('cookies', 'r')
            cookie = json.loads(file.read())[-1]
            file.close()
            cookie_time = int(cookie['expiry'])
            # 判断cookie是已过期，如果过期删除过期cookie，并退出程序
            if not self.cookie_is_expired(cookie_time):
                return cookie
            else:
                print('cookie已经过期，删除cookie')
                self.delete_cookie()
                exit(0)

    def get_html(self):
        """进入腾讯乐享活动界面"""
        self.driver.get(self.events_url)
        self.driver.add_cookie(cookie_dict=self.get_cookie())
        print("浏览器添加cookie信息，进入活动界面")
        self.driver.get(self.events_url)

    def click_lecture_button(self):
        """点击'讲座'关键字，进入讲座列表界面"""
        # 隐式加载界面,在进行查询元素前，如果还有未加载完，再等5秒
        print("进入讲座列表页面")
        self.driver.implicitly_wait(2)
        lecture_xpath = '//*[@id="app-vue"]/div[2]/div/ul[1]/li[2]/a'
        self.driver.find_element_by_xpath(lecture_xpath).click()

    def find_latest_lecture(self, lecture_keyword) -> bool:
        """输入讲座标题，搜索标题，查询符合元素，获取该讲座的链接，进入讲座具体页面"""
        lecture = None
        refresh_times = 0
        # 通话标题关键字获得讲座链接
        while lecture is None:
            refresh_times += 1
            try:
                lecture = self.driver.find_element('partial link text', lecture_keyword)
                lecture_name = lecture.get_attribute('text').strip()
                print("根据关键字 '{}' 查询到讲座标题为：{}，进入讲座详情页面。".format(lecture_keyword, lecture_name))
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
        # 报名后，人数已满的xpath
        enroll_inform_xpath = "//*[@id='app-vue']/div[2]/div/div[1]/div[1]/div/div[2]/span/span"
        # 讲座已过期
        lecture_overtime = "//*[@id='app-vue']/div[2]/div/div[1]/div[1]/div/div[1]/span"
        # 报名后成功后的xpath
        enroll_inform_xpath1 = "//*[@id='app-vue']/div[2]/div/div[1]/div[1]/div/div[2]/span"

        # 若找不到报名按钮，或报名信息，则查询讲座是否结束
        try:
            # 查找报名按钮，并点击报名按钮
            self.driver.find_element_by_xpath(button_xpath).click()
            print('已点击报名')
            self.driver.refresh()
            # 点击报名后，查询提示信息,是人员已满还是报名成功
            enroll_inform = self.driver.find_element_by_xpath(enroll_inform_xpath1).text
            print("报名情况:" + enroll_inform)
        except NoSuchElementException as error:
            try:
                enroll_inform = self.driver.find_element_by_xpath(enroll_inform_xpath).text
                print("报名情况:" + enroll_inform)
            except NoSuchElementException as error:
                # 查询讲座是否结束
                try:
                    inform = self.driver.find_element_by_xpath(overtime_button_xpath).text
                    print('讲座情况:' + inform)
                except NoSuchElementException as error:
                    try:
                        inform = self.driver.find_element_by_xpath(lecture_overtime).text
                        print('讲座情况:' + inform)
                    except NoSuchElementException as error:
                        print('当前讲座页面未查询到任何相关信息')
                        return False
