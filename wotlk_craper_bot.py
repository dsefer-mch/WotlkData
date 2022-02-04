from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import requests


class ScriperBot():
    def __init__(self, verbose=False):
        print('Bot initialising...')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)
        self.url = "https://wotlkdb.com/"
        self.verbose = verbose

    def open_chrome_url(self, headless=False):
        timeout = 5
        try:
            requests.get(self.url, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection.")
            return self.driver.quit()
        if headless:
            chrome_options = Options()
            chrome_options.add_argument("headless")
            self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

    def find_element(self, element, type='textlink'):
        try:
            if type == 'id':
                obect = self.driver.find_element(By.ID, element)
                return obect
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
            EC.NoSuchElementException(
                'Field to clear not found or not a propper type...')

    def set_field(self, value):
        try:
            self.send_keys(value)
        except:
            EC.NoSuchElementException(
                'Field to clear not found or not a propper type...')

    def hit_enter(self):
        try:
            self.send_keys(Keys.RETURN)
        except:
            EC.NoSuchElementException(
                'Field to clear not found or not a propper type...')

    def move_cursor(self):
        try:
            self.action.move_to_element(self).perform()

        except:
            EC.NoSuchElementException(f'Object not found...')

    def driver_quit(self):
        self.driver.quit()


    # def download_file(self, src_url, local_destination):
    #     response = requests.get(src_url)
    #     with open(local_destination, 'wb+') as f:
    #         f.write(response.content)


if __name__ == '__main__':
    bot = ScriperBot(verbose=True)
    bot.open_chrome_url()
    bot.driver_quit()