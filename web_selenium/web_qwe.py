from time import sleep

from selenium import webdriver

from web_selenium import config

argument_list = [
    # 'auto-open-devtools-for-tabs',
    '--disable-infobars',
    'lang=en'
]

experimental_list = [
    ("w3c", False),
    ("useAutomationExtension", False),
    ("excludeSwitches", ["enable-automation", "enable-logging", "disable-sync"]),
]
chrome_options = webdriver.ChromeOptions()

for option in experimental_list:
    chrome_options.add_experimental_option(*option)
# chrome_options.add_extension()
# chrome_options.add_encoded_extension()

for option in argument_list:
    chrome_options.add_argument(option)
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://testerhome.com/')
sleep(5)
config.driver = driver
print(config.driver)
print(config.browser)
driver.quit()