from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import requests
from time import sleep


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

    def accept_cookies(self):
        print('1')
        try:
            print('2')
            butt = self.find_element_by_element('Accept')
            print('1.1', butt)
            if butt == None:
                print('here we are in the xpath br')
                butt = self.find_element_by_element(
                    '//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]', 'xpath')
            print(butt)
            self.move_cursor(butt)
            print('4')
            print(butt)
            self.click_on(butt)
        except:
            EC.NoSuchElementException(f'Something went wrong or NO cookies...')

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def find_element_by_element(self, element, type='textlink'):
        try:
            print('6')
            if type == 'id':
                print('its in the id')
                obj = self.driver.find_element(By.ID, element)
                print('thats after the oject')
                print('what the fack?', obj)
                return obj
            elif type == 'xpath':
                obj = self.driver.find_element(By.XPATH, element)
                return obj
            elif type == 'textlink':
                print('7')
                print(element)
                sleep(10)
                obj = self.driver.find_element(By.LINK_TEXT, element)
                print('8')
                print(obj)
                return obj
            elif type == 'name':
                obj = self.driver.find_element(By.NAME, element)
                return obj
            elif type == 'tag':
                obj = self.driver.find_element(By.TAG_NAME, element)
                return obj
            elif type == 'class':
                obj = self.driver.find_element(By.CLASS_NAME, element)
                return obj
        except:
            EC.NoSuchElementException('No such element found...')

    def move_cursor(self, obj):
        try:
            print('9')
            print(obj)
            self.action.move_to_element(obj)
            self.action.perform()
            return
        except:
            EC.NoSuchElementException(f'Object not found...')

    def click_on(self, obj):
        try:
            print('10')
            print(obj)
            self.action.click(obj)
            self.action.perform()
        except:
            EC.NoSuchElementException(f'Nothing to click on...')

    def clear_field(self):
        try:
            self.clear()
            return
        except:
            EC.NoSuchElementException(
                'Field to clear not found or not a propper type...')

    def set_field(self, value):
        try:
            self.send_keys(value)
            return
        except:
            EC.NoSuchElementException(
                'Field to clear not found or not a propper type...')

    def hit_enter(self):
        try:
            return self.send_keys(Keys.RETURN)
        except:
            EC.NoSuchElementException(
                'Field to clear not found or not a propper type...')

    def driver_quit(self):
        self.driver.quit()

    # def download_file(self, src_url, local_destination):
    #     response = requests.get(src_url)
    #     with open(local_destination, 'wb+') as f:
    #         f.write(response.content)


if __name__ == '__main__':
    bot = ScriperBot(verbose=True)
    bot.open_chrome_url()
    bot.accept_cookies()
    found = bot.find_element_by_element('Database')
    bot.move_cursor(found)
    sleep(20)
    bot.delete_cookies()
    bot.driver_quit()
