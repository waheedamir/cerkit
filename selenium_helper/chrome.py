import time

from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options as ff_options
from selenium.webdriver.chrome.options import Options


class SeleniumDriver(object):
    """
    This middleware is written to use headless selenium
    """
    driver = None

    def __init__(self, headless=True, cloud_flare=False):
        self.cloud_flare = cloud_flare
        self.headless = headless
        self.create_driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def create_driver(self):
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("start-maximized")
        options.add_argument('--disable-javascript')
        options.add_argument('--disable-dev-shm-usage')
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument('--profile-directory=Default')
        if self.cloud_flare:
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        capabilities = webdriver.DesiredCapabilities.CHROME
        capabilities['marionette'] = True
        self.driver = webdriver.Chrome(executable_path='drivers/chromedriver.exe',
                                       options=options, desired_capabilities=capabilities)

    def close_driver(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            pass

    def make_request(self, url, timeout=0, wait_until_page_load=False):
        # self.driver.request('GET', url, verify=False, page_load_timeout=20,
        #                     find_window_handle_timeout=20)
        self.driver.get(url)
        if timeout:
            time.sleep(timeout)
        if wait_until_page_load:
            self.page_loading_wait()

    def process_request(self, url, timeout=0, wait_until_page_load=False):
        try:
            self.make_request(url, timeout, wait_until_page_load)
        except AttributeError as e:
            pass
        except (TimeoutException, WebDriverException) as e:
            self.close_driver()
            self.create_driver()
            self.make_request(url, timeout)
            time.sleep(1)

        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body,
                            encoding='utf-8')

    def next(self, selector=None, xpath=None):
        try:
            if selector:
                self.driver.find_element_by_css_selector(selector).click()
            elif xpath:
                self.driver.find_element_by_xpath(xpath=xpath).click()
            else:
                return False
            time.sleep(2)
            return True
        except:
            return False

    def scroll(self, scrolls=20, wait=1):
        for i in range(1, scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait)

    def page_loading_wait(self):
        while True:
            x = self.driver.execute_script("return document.readyState")
            if x != "complete":
                time.sleep(1)
            else:
                break
        return True

    @property
    def page_source(self):
        return self.driver.page_source
