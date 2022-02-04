from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from time import sleep, time
import requests


class Bot():
    def __init__(self):
        print('Bot initialising...')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)
        url = "https://wotlkdb.com/"

    def find_element(self, element, type='textlink'):
        try:
            if type == 'textlink':
                obect = self.driver.find_element(By.LINK_TEXT, element)
                return obect
            elif type == 'xpath':
                obect = self.driver.find_element(By.XPATH, element)
                return obect
            elif type == 'name':
                obect = self.driver.find_element(By.NAME, element)
                return obect
            elif type == 'tag':
                obect = self.driver.find_element(By.TAG_NAME, element)
                return obect
        except:
            EC.NoSuchElementException('No such element found...')

    def move_cursor(self, obect):
        try:
           self.action.move_to_element(obect).perform()

        except:
            EC.NoSuchElementException(f'Object not found...')

    def clear_field(self):
        try:
            self.clear()
        except:
            EC.NoSuchElementException('Field to clear not found or not a propper type...')

    def set_filter(self, value):
        try:
            self.send_keys(value)
        except:
            EC.NoSuchElementException('Field to clear not found or not a propper type...')

    def hit_enter(self):
        try:
            self.send_keys(Keys.RETURN)
        except:
            EC.NoSuchElementException('Field to clear not found or not a propper type...')

        
    def move_cursor(self):
        try:
           self.action.move_to_element(self).perform()

        except:
            EC.NoSuchElementException(f'Object not found...')




    def download_file(self, src_url, local_destination):
        response = requests.get(src_url)
        with open(local_destination, 'wb+') as f:
            f.write(response.content)

if __name__ == '__main__':
    # EXAMPLE USAGE