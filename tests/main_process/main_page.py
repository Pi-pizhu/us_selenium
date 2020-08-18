from selenium.webdriver.common.by import By

from web_selenium.base.basepage import BasePage


class MainPage(BasePage):

    _base_url = 'https://testerhome.com/'
    # _base_url = 'https://www.baidu.com/'

    shequ = {
        'locat': (
            By.LINK_TEXT, '社区'
        ),
        'action': 'click'
    }

    bug = {
        'locat': (
            By.LINK_TEXT, 'Bug 曝光台'
        ),
        'action': 'click'
    }

    wenda = {
        'locat': (
            By.LINK_TEXT, '问答'
        ),
        'action': 'click'
    }

    shetuan = {
        'locat': (
            By.LINK_TEXT, '社团'
        ),
        'action': 'click'
    }

    zhaopin = {
        'locat': (
            By.LINK_TEXT, '招聘'
        ),
        'action': 'click'
    }

    wiki = {
        'locat': (
            By.LINK_TEXT, 'Wiki'
        ),
        'action': 'click'
    }

    kaiyuan = {
        'locat': (
            By.LINK_TEXT, '开源项目'
        ),
        'action': 'click'
    }

    kuzhan = {
        'locat': (
            By.LINK_TEXT, '酷站'
        ),
        'action': 'click'
    }

    bangdan = {
        'locat': (
            By.LINK_TEXT, 'TTF榜单'
        ),
        'action': 'click'
    }

    def go_shequ(self):
        self.steps(**self.shequ)
        return self

    def go_bug(self):
        self.steps(**self.bug)
        return self

    def go_wenda(self):
        self.steps(**self.wenda)
        return self

    def go_shetuan(self):
        self.steps(**self.shetuan)
        return self

    def go_zhaopin(self):
        self.steps(**self.zhaopin)
        return self

    def go_wiki(self):
        self.steps(**self.wiki)
        return self

    def go_kaiyuan(self):
        self.steps(**self.kaiyuan)
        return self

    def go_kuzhan(self):
        self.steps(**self.kuzhan)
        return self

    def go_bangdan(self):
        self.steps(**self.bangdan)
        return self

    def go_home(self):
        self.driver.get(self._base_url)