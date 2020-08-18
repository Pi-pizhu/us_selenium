import os
import sys

from selenium import webdriver
from web_selenium import config as br_config
from web_selenium.base.configuration import load_file
from web_selenium.base.sys_operation import get_current_path, get_all_subdirectories, join_path

PLATFORM = sys.platform

# 浏览器类型
class Browser:
    Chrome = 'chrome'
    Firefox = 'firefox'
    Internet = 'ie'
    Safari = 'safari'


def load_browser_settings():
    """
        browser_name
        use_grid
        address
        user_data_dir
        user_agent
        proxy_string
        proxy_user
        proxy_pass
        headless
        swiftshader
    :return:
    """
    file_path = get_current_path()
    filename = get_all_subdirectories(filter_name="browser_settings")
    settings_file = join_path(file_path, filename[0])
    settings_data = load_file(settings_file, load_type='json')

    br_config.browser = settings_data.get('browser')
    br_config.use_grid = settings_data.get('use_grid')
    br_config.address = settings_data.get('address')
    br_config.user_data_dir = settings_data.get('user_data_dir')
    br_config.user_agent = settings_data.get('user_agent')
    br_config.proxy_string = settings_data.get('proxy_string')
    br_config.proxy_user = settings_data.get('proxy_user')
    br_config.proxy_pass = settings_data.get('proxy_pass')
    br_config.headless = settings_data.get('headless')
    br_config.swiftshader = settings_data.get('swiftshader')


def get_driver(browser_name, use_grid, address, user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth):
    if use_grid:
        return _get_remote_driver(address, user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth)
    else:
        return _get_local_driver(browser_name, user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth)


def _get_remote_driver(address, user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth):
    chrome_options: webdriver.ChromeOptions = _set_chrome_options(user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth)
    capabilities = chrome_options.to_capabilities()
    driver = webdriver.Remote(command_executor=address,
                              desired_capabilities=capabilities,
                              keep_alive=True)
    return driver


def _get_local_driver(broswer_name, user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth):

    if broswer_name == Browser.Chrome:
        chrome_options = _set_chrome_options(user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth)
        chrome_driver = webdriver.Chrome(options=chrome_options)
        return chrome_driver
    elif broswer_name == Browser.Firefox:
        firefox_profile = _set_firefox_profile()
        firefox_driver = webdriver.Firefox(firefox_profile=firefox_profile)
        return firefox_driver
    elif broswer_name == Browser.Internet:
        ie_driver = webdriver.Ie()
        return ie_driver
    elif broswer_name == Browser.Safari:
        safari_driver = webdriver.Safari()
        return safari_driver


def _add_chrome_proxy_extension(chrome_options, proxy_string, proxy_user, proxy_pass):
    pass


def _set_chrome_options(user_data_dir, user_agent, proxy_string, proxy_user, proxy_pass, headless,
                        swiftshader, proxy_auth):
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation", "enable-logging"])

    if user_data_dir:
        abs_path = os.path.abspath(user_data_dir)
        chrome_options.add_argument("user-data-dir=%s" % abs_path)

    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--ignore-certificate-errors")
    # if devtools and not headless:
    #     chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--allow-running-insecure-content")
    if user_agent:
        chrome_options.add_argument("--user-agent=%s" % user_agent)
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-single-click-autofill")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--homepage=about:blank")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--dom-automation")
    # if not use_auto_aext:  # (It's ON by default. Disable it when not wanted.)
    chrome_options.add_experimental_option("useAutomationExtension", False)
    # if (settings.DISABLE_CSP_ON_CHROME or disable_csp) and not headless:
        # Headless Chrome doesn't support extensions, which are required
        # for disabling the Content Security Policy on Chrome
        # chrome_options = _add_chrome_disable_csp_extension(chrome_options)
    if proxy_string:
        if proxy_auth:
            chrome_options = _add_chrome_proxy_extension(
                chrome_options, proxy_string, proxy_user, proxy_pass)
        chrome_options.add_argument('--proxy-server=%s' % proxy_string)
    else:
        chrome_options.add_argument("--no-proxy-server")
    if headless:
        if not proxy_auth:
            # Headless Chrome doesn't support extensions, which are
            # required when using a proxy server that has authentication.
            # Instead, base_case.py will use PyVirtualDisplay when not
            # using Chrome's built-in headless mode. See link for details:
            # https://bugs.chromium.org/p/chromium/issues/detail?id=706008
            chrome_options.add_argument("--headless")
    # if (headless and "linux" in PLATFORM) or no_sandbox:
    chrome_options.add_argument("--no-sandbox")  # (Now always on)
    if swiftshader:
        chrome_options.add_argument("--use-gl=swiftshader")
    else:
        chrome_options.add_argument("--disable-gpu")
    if "linux" in PLATFORM:
        chrome_options.add_argument("--disable-dev-shm-usage")

    return chrome_options


def _set_firefox_profile():
    firefox_profile = webdriver.FirefoxProfile()
    return firefox_profile
