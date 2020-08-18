from time import sleep

import pytest

from tests.main_process.main_page import MainPage


class TestCase:

    def setup_method(self):
        self.main = MainPage()

    def test_demo1(self):
        sleep(5)

    # def test_goPage1(self):
    #     self.main.go_shequ().go_bug().go_wenda().go_shetuan().go_zhaopin(). \
    #         go_wiki().go_kaiyuan().go_kuzhan().go_bangdan().go_home()

    # def test_goPage2(self):
    #     self.main.go_shequ().go_bug().go_wenda().go_shetuan().go_zhaopin(). \
    #         go_wiki().go_kaiyuan().go_kuzhan().go_bangdan().go_home()
    #
    # def test_goPage3(self):
    #     self.main.go_shequ().go_bug().go_wenda().go_shetuan().go_zhaopin(). \
    #         go_wiki().go_kaiyuan().go_kuzhan().go_bangdan().go_home()

    def teardown_method(self):
        self.main.quit()


if __name__ == '__main__':
    pytest.main()