from selenium import webdriver
from time import *
import json
import os
from selenium.common.exceptions import NoSuchElementException


class Crawler:
    cookies = {}
    user_agent = ''
    login_url = ''
    url = ''

    def __init__(self, user_agent, login_url, url):
        self.user_agent = user_agent
        self.login_url = login_url
        self.url = url
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
        # self.driver.maximize_window()

    def login_and_save_cookies(self, login_url):
        """打开登陆页面，登陆后抓取cookies信息保存下来以便之后自动登陆使用"""
        self.driver.get(login_url)
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
        """判断是否有cookie文件，cookies是否过期，如果过期再次打开登录页面进行获取，若有未过期cookies直接返回"""
        if self.cookie_exist():
            print("cookies文件存在")
            # 获得cookies
            file = open('cookies', 'r')
            cookie = json.loads(file.read())[-1]
            file.close()
            print("读取cookie，返回cookie")
            return cookie
        else:
            print("cookies文件不存在，跳转到登录界面进行获取")
            self.login_and_save_cookies(self.login_url)
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
        search_times = 0
        # 通话标题关键字获得讲座链接
        while lecture is None:
            search_times += 1
            try:
                lecture = self.driver.find_element('partial link text', lecture_keyword)
            except NoSuchElementException as error:
                print('未找到讲座')
            self.driver.refresh()

            if search_times == 100:
                lecture_keyword = input('请输入讲座标题的其他关键字:')
                search_times = 0

            if lecture_keyword == 'quit':
                print('退出')
                self.driver.close()
                return

        lecture_title = str(lecture.text)
        print("查询成功，讲座：" + lecture_title)
        # 获得讲座链接
        lecture_href = lecture.get_attribute('href')
        print("成功获得讲座详细界面链接")
        # 进入具体讲座页面
        self.driver.get(lecture_href)
        print("进入讲座：" + lecture_title + '详细界面')
