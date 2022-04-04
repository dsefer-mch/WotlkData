from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common import exceptions as ex
from urllib3.exceptions import MaxRetryError, NewConnectionError
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import sys
import os
import boto3


class ScraperBot():
    def __init__(self, headless=False, verbose=False):

        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.driver.maximize_window()
        self.verbose = verbose

    def accept_cookies(self, xpath=None, iframe=None):
        accept_button = None
        if iframe:
            try:
                self.driver.switch_to.frame(iframe)
            except ex.NoSuchFrameException(msg="Frame target doesn't exist."):
                print(
                    "Web-page may be changed.Try another way to get the cookie's button")
        elif xpath:
            try:
                accept_button = self.driver.find_element(By.XPATH, xpath)
            except ex.NoSuchElementException(msg="Cookie's xpath button not found."):
                print(
                    "Web-page may be changed.Try another way to get the cookie's button")
        if not accept_button:
            try:
                accept_button = self.driver.find_element(
                    By.LINK_TEXT, 'Accept')
            except ex.NoSuchElementException(msg="Accept button to accept cookies not found."):
                print(
                    "Web-page may be changed.Try another way to get the cookie's button")
                print('Cookies not detected.')
        elif accept_button:
            try:
                accept_button.click()
            except Exception as e:
                print("For some reason cookie's button is unclickable", e)

    def hoover_over(self, text=None, xpath=None):
        action = ActionChains(self.driver)
        if text:
            try:
                obj = self.driver.find_element(By.LINK_TEXT, text)
            except ex.NoSuchElementException:
                print('Element not found @ <hoover_over> by text.')
                self.shut()

        if xpath:
            try:
                obj = self.driver.find_element(By.XPATH, xpath)
            except ex.NoSuchElementException:
                print('Element not found @ <hoover_over> by xpath.')
                # self.shut()
        action.move_to_element(obj)
        action.perform()

    def click_text(self, text):
        try:
            self.driver.find_element(By.LINK_TEXT, text).click()
        except ex.NoSuchElementException(msg="Element <LINK_TEXT> to click not found.") as e:
            print(e)
        except ex.ElementClickInterceptedException(msg="Element Click command could not be completed because the element receiving the events is obscuring the element that was requested to be clicked"):
            self.shut()

    def click_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath).click()
        except ex.NoSuchElementException(msg="Element <XPATH> to click not found.") as e:
            print(e)
        except ex.ElementClickInterceptedException(msg="Element Click command could not be completed because the element receiving the events is obscuring the element that was requested to be clicked"):
            self.shut()

    def input_id(self, id, text):  # wotlk scraper doesn't use this one
        try:
            input = self.driver.find_element(By.ID, id)
        except ex.NoSuchElementException(msg="Element not found @ imput_id func."):
            print("Look for changes in the HTML.")
        try:
            input.clear()
        except ex.InvalidElementStateException(msg="command could not be completed <clear()> , because the element is in an invalid state."):
            print(
                "The field selenium is trying to clear isn't both editable and resettable")
        input.send_keys(text)
        return input

    def input_name(self, name, text):
        try:
            input = self.driver.find_element(By.NAME, name)
        except ex.NoSuchElementException(msg="Element not found @ imput_name func."):
            print("Look for changes in the HTML.")
        try:
            input.clear()
        except ex.InvalidElementStateException(msg="command could not be completed <clear()> , because the element is in an invalid state."):
            print(
                "The field selenium is trying to clear isn't both editable and resettable")
        input.send_keys(text)
        return input

    def reading_elem(self, xpath):
        try:
            reading = self.driver.find_element(By.XPATH, xpath).text
        except ex.NoSuchElementException(msg="Element not found @ reading_elem by xpath"):
            if self.verbose:
                print('Possible reason - web-page content change.Check xpath.')
        return reading

    def hit_enter(self, obj):
        try:
            obj.send_keys(Keys.ENTER)
        except AttributeError as e:
            print('Check obj @ hit_enter func', e)
        return

    def set_url(self, url):
        try:
            self.driver.get(url)
        except TimeoutException:
            print("TimeoutException")
        except (ConnectionRefusedError, MaxRetryError, NewConnectionError):
            # MaxRetryError and NewConnectionError come from urllib3.exceptions
            # ConnectionRefusedError is a Python builtin.
            print("Connection error")
        except Exception:
            print("Unexpected exception in driver.get().")
        if self.verbose:
            print('Selenium opens ', url)

    def create_dir(self, name, dir_path=None):
        dir_name = name
        if dir_path == None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(dir_path, dir_name)
        else:
            path = os.path.join(dir_path, dir_name)
        try:
            os.mkdir(path)
            if self.verbose:
                if self.verbose:
                    print("Directory '% s' created" % dir_name)
        except OSError:
            if self.verbose:
                print(
                    'Existing directory:', dir_name)
        return path

    def s3_up(self, file_or_img_name, bucket_name, obj_name):
        # , aws_access_key_id=#aws_config_file, region_name=...,aws_secret_access_key=...)
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(
                file_or_img_name, bucket_name, obj_name)
            print('Image uploaded to s3')
        except:
            print('File (image) NOT uploaded!')

    def shut(self):
        self.driver.quit()
        sys.exit("Session over!")


if __name__ == '__main__':
    bot = ScraperBot()
    bot.accept_cookies(xpath='//*[@class="ncmp__btn"]')
    bot.delete_cookies()
    bot.driver.quit()
