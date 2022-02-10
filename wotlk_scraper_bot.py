from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import requests
from time import sleep
import subprocess, os


def open_chrome(port=9200, on_mac=False):
    my_env = os.environ.copy()
    if on_mac:
        print('opening chrome')
        subprocess.Popen(['open', '-a', "Google Chrome", '--args', f'--remote-debugging-port={port}', 'http://www.example.com'], env=my_env)
    else:
        subprocess.Popen(f'google-chrome --remote-debugging-port={port} --user-data-dir=data_dir'.split(), env=my_env)
    print('opened chrome')

class ScraperBot():

    def __init__(self, verbose=False, headless=False):
        print('Bot initialising...')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url = "https://wotlkdb.com/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.verbose = verbose
        if headless:
            chrome_options = Options()
            chrome_options.add_argument("headless")
            chrome_options.add_experimental_option(f"debuggerAddress", f"127.0.0.1:9200")
            self.driver = webdriver.Chrome(options=chrome_options)
        options = Options()
        options.add_argument('--no-sandbox')


    def accept_cookies(self):
        action = ActionChains(self.driver)
        try:
            accept_button = self.driver.find_element(By.XPATH, '//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]')
            action.move_to_element(accept_button)
            action.perform()
            action.click()
            action.perform()
        except:
            EC.NoSuchElementException(f'Something went wrong or NO cookies...')

    def delete_cookies(self):
        self.driver.delete_all_cookies()
        print('does it cleans it?')


if __name__ == '__main__':
    bot = ScraperBot()
    # bot.open_chrome_url(headless=True)
    bot.accept_cookies()
    bot.delete_cookies()
    sleep(10)
    bot.driver.quit()
