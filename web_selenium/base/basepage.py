import time
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from web_selenium.base.configuration import load_file
from web_selenium.base.sys_operation import *
from web_selenium import config as br_config
from web_selenium.base.browser_launcher import get_driver, load_browser_settings


def exception_handle(func):
    def magic(*args, **kwargs):
        instance: BasePage = args[0]
        try:
            result = func(*args, **kwargs)
            # time.sleep(2)
            instance._retry = 0
            return result
        except Exception as error:
            instance._retry += 1
            if instance._retry > instance._retry_max:
                raise error
            instance.driver.implicitly_wait(0)
            for black in instance._black_list.values():
                elements = instance.finds(black)
                if len(elements) > 0:
                    elements[0].click()
                    instance.driver.implicitly_wait(3)
                    return func(*args, **kwargs)
            return func(*args, **kwargs)
    return magic


class BasePage:
    _driver: RemoteWebDriver = None
    _base_url = ""
    _width = 1792
    _height = 1120
    _retry = 0
    _retry_max = 5
    _black_list = {}
    capabilities = {
        "browserName": "chrome",
        "version": "",
        "platform": "ANY",
        "javascriptEnabled": True,
    }
    _local_options = {
        "browser_type": "Chrome",
        "port": 0,
        "options": None,
        "service_args": None,
        "desired_capabilities": capabilities,
        "service_log_path": None,
        "chrome_options": None,
        "keep_alive": True
    }
    _remote_options = {
        "command_executor": 'http://127.0.0.1:4444/wd/hub',
        "desired_capabilities": None,
        "browser_profile": None,
        "proxy": None,
        "keep_alive": False,
        "file_detector": None,
        "options": None
    }
    """
    chrome.options={
    "add_argument": [],
    "add_experimental_option": [],
    "add_encoded_extension": [],
    "add_extension": [],
    }
    firefox.options={
    "add_argument": []
    }
    """
    # def __init__(self, **driver_options):
    #     driver_options = ''
    #     if not driver_options:
    #         raise('请添加driver配置信息')
    #     else:
    #
    #         driver = br_config.driver
    #         if driver:
    #             self.driver = driver
    #         else:



    def __init__(self, reuse_driver=False):
        if reuse_driver and br_config.driver:
            # 如果传入了一个已存在的driver实例，那么则继续使用这个driver实例
            self._driver = br_config.driver
        else:
            # todo: 从命令行中获取路径和文件名
            # # current_path = "/Users/yewenkai/PycharmProjects/us_selenium/tests/data/config.ini"
            # options_path = get_current_path()
            # options_filename = get_all_subdirectories(filter_name="json")
            # options_file = join_path(options_path, options_filename[0])
            load_browser_settings()

            browser_name = br_config.browser
            use_grid = br_config.use_grid
            address = br_config.address
            user_data_dir = br_config.user_data_dir
            user_agent = br_config.user_agent
            proxy_string = br_config.proxy_string
            proxy_user = br_config.proxy_user
            proxy_pass = br_config.proxy_pass
            headless = br_config.headless
            swiftshader = br_config.swiftshader
            proxy_auth = False
            if proxy_string:
                proxy_auth = True

            self._driver = self.get_new_driver(browser_name, use_grid, address, user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth)


            # if remote:
            #     # 从配置文件中获取内容
            #     self._remote_options = load_file(options_file, load_type="json")['remote_options']
            #     browser_type = self._local_options.get("desired_capabilities").get('browserName')
            #     # 根据标识创建options实例
            #     browser_options_ins = self._create_options_ins(browser_type)
            #     # 使用实例添加配置
            #     browser_options_ins = self._browser_options(option_instance=browser_options_ins,
            #                                                 options_config=self._remote_options)
            #     # option = webdriver.ChromeOptions()
            #     # option.add_argument("--user-data-dir=/home/seluser/.config/google-chrome/Default")
            #     # option.add_argument('--disable-infobars')
            #     # option.add_experimental_option("lang", "zh-CN")
            #     # option.add_argument('--lang=zh-CN') # zh_CN.UTF-8
            #     self._remote_options.update({
            #             "options": browser_options_ins
            #         })
            #     self._driver = webdriver.Remote(**self._remote_options)
            # else:
            #     # 从配置文件中获取内容
            #     self._local_options = load_file(options_file, load_type="json")['local_options']
            #     browser_type = self._local_options.pop("browser_type")
            #     # 根据标识创建options实例
            #     browser_options_ins = self._create_options_ins(browser_type)
            #     # 使用实例添加配置
            #     browser_options_ins = self._browser_options(option_instance=browser_options_ins,
            #                                                 options_config=self._local_options)
            #     self._local_options.update(
            #         {
            #             "options": browser_options_ins
            #         }
            #     )
            #     self._driver = self.start_browser(browser_type=browser_type)
        self._driver.implicitly_wait(3)

        if self._base_url:
            # 如果创建或获取实例时，添加了base_url 则转到对应的页面
            self._driver.get(url=self._base_url)

        self._driver.set_window_size(self._width,self._height)

    def get_new_driver(self, browser_name='chrome', use_grid=False, address=None, user_data_dir=None,
                       user_agent=None, proxy_string=None, proxy_user=None, proxy_pass=None, headless=False,
                        swiftshader=False, proxy_auth=False):
        return get_driver(browser_name, use_grid, address, user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth)

    def start_browser(self, browser_type='Chrome'):
        # 初始化浏览器实例
        browser_type = browser_type.lower()
        try:
            if browser_type == 'chrome':
                driver = webdriver.Chrome(**self._local_options)
            elif browser_type == 'firefox':
                driver = webdriver.Firefox(**self._local_options)
            else:
                err_msg = f"请传入正确的浏览器类型(chrome、firefox、Ie):\n{browser_type}"
                raise(err_msg)
            return driver
        except Exception as error:
            err_msg = f"初始化浏览器实例失败：\n{error}"
            raise(err_msg)
            # todo: 后续需要添加一个启动失败重试的次数循环

    def _create_options_ins(self, browser_type: str):
        browser_type = browser_type.lower()
        if "chrome" in browser_type:
            browser_options_ins = webdriver.ChromeOptions()
        elif "firefox" in browser_type or "gecko" in browser_type:
            browser_options_ins = webdriver.FirefoxOptions()
        elif "ie" in browser_type:
            browser_options_ins = webdriver.IeOptions()
        else:
            raise(f"请输入正确的浏览器类型：{browser_type}")
        return browser_options_ins

    def _browser_options(self, option_instance: webdriver.ChromeOptions, options_config: dict):
        # 添加浏览器配置、扩展、实验性质参数等
        """
        如果options_config内有值就添加配置：
            add_argument
            add_experimental_option
            add_encoded_extension
            add_extension
        :param option_instance:
        :param options_config:
        :return:
        """
        # todo: add_argument 设置浏览器启动语言、隐藏自动化测试提示不生效
        # todo: 可能是zh_CN 下次尝试一下下划线
        options_initial: dict = options_config.pop('options')
        if options_initial:
            argument = options_initial.get("add_argument")
            experimental = options_initial.get("add_experimental_option")
            encoded = options_initial.get("add_encoded_extension")
            extension = options_initial.get("add_extension")

            if argument and len(argument) > 0:
                for arg in argument:
                    option_instance.add_argument(arg)

            if experimental and len(experimental) > 0:
                for exper in experimental:
                    option_instance.add_experimental_option(*exper)

            if encoded and len(encoded) > 0:
                for encod in encoded:
                    option_instance.add_encoded_extension(encod)

            if extension and len(extension) > 0:
                for exten in extension:
                    option_instance.add_extension(exten)
        return option_instance

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    # @error_if_driver(_driver)
    def find(self, locat):
        element = WebDriverWait(self._driver, 20, 0.5).until(
            EC.presence_of_element_located(locat)
        )
        return element

    def finds(self, locat):
        elements = WebDriverWait(self._driver, 20, 0.5).until(
            EC.presence_of_all_elements_located(locat)
        )
        return elements

    @exception_handle
    def steps(self, **locat):
        """
        **locat:{
            locat: (
                By.id, 'kw'
                )
            action: click
            gmessage: None
        }
        :param locat:
        :return:
        """
        # print(args)
        print(locat)
        # locat = args[0]
        action = locat['action']
        locating: tuple = tuple(locat['locat'])
        element: WebElement = self.find(locating)

        if action == 'click':
            element.click()
        elif action == 'send':
            value = locat.get('gmessage')
            element.send_keys(value)
        elif action == 'text':
            print('------------>text_element:{}'.format(element))
            return element.text
        elif action == 'submit':
            element.submit()
        elif action == 'clear':
            element.clear()
        elif action == 'attribute':
            value = locat.get('gmessage')
            return element.get_attribute(value)
        elif action == 'is_selected':
            return element.is_selected()
        elif action == 'element':
            return element

    def close(self):
        self._driver.close()

    def quit(self):
        self._driver.quit()

    def switch_window(self, page_index: int):
        windows = self._driver.window_handles
        while len(windows) < 2:
            windows = self._driver.window_handles
        self._driver.switch_to.window(windows[page_index])

    def scroll(self, js: str, join_value = None):
        # 如果需要动态控制
        js = ''.join((js, join_value)) if join_value else js
        self._driver.execute_script(js)

    def ActionChains(self, element: WebElement, driver = None) -> None:
        ActionChains(
            driver if driver else self._driver
        ).move_to_element(element).perform()
        time.sleep(3)