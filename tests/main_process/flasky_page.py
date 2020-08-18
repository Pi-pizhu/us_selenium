from selenium.webdriver.common.by import By

from web_selenium.base.basepage import BasePage


class FlaskyPage(BasePage):

    _base_url = 'http://127.0.0.1:5000/admin'
    # _base_url = 'https://www.baidu.com/'

    username = {
        'locat': (
            By.CSS_SELECTOR, '#email'
        ),
        'action': 'send',
        'gmessage': 'huster1446@admin.com'
    }

    password = {
        'locat': (
            By.CSS_SELECTOR, '#password'
        ),
        'action': 'send',
        'gmessage': 'huster1446'
    }

    login = {
        'locat': (
            By.CSS_SELECTOR, '#login'
        ),
        'action': 'click'
    }

    frozen = {
        'locat': (
            By.CSS_SELECTOR, 'tr:nth-child(1) > td:nth-child(9) > button.frozen'
        ),
        'action': 'click'
    }

    delete = {
        'locat': (
            By.CSS_SELECTOR, 'tr:nth-child(3) > td:nth-child(9) > button.delete'
        ),
        'action': 'click'
    }

    def send_username(self):
        self.steps(**self.username)
        return self

    def send_password(self):
        self.steps(**self.password)
        return self

    def go_login(self):
        self.steps(**self.login)
        return self

    def go_frozen(self):
        self.steps(**self.frozen)
        return self

    def go_delete(self):
        self.steps(**self.delete)
        return self

    def go_home(self):
        self.driver.get(self._base_url)