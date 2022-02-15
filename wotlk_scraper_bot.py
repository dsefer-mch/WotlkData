from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
from time import sleep



class ScraperBot():

    def __init__(self, url, options=None):
        print(self)
        
        self.url = url
        if options:
            self.driver = Chrome(ChromeDriverManager().install(), options=options)
        else:
            self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)


    def accept_cookies(self, xpath=None, iframe=None):
        sleep(5)
        try:
            if iframe:
                self.driver.switch_to.frame(iframe)
            accept_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Accept')
            if accept_button == None:
                accept_button = self.driver.find_element(By.XPATH, xpath)
            accept_button.click()
        except:
            print('Cookies not detected.')

    def hoover_over(self, text= str, xpath=None):
        action = ActionChains(self.driver)
        if text:
            action.move_to_element(text)
            action.perform()
        if xpath:
            action.move_to_element(xpath)
            action.perform()

    def click_text(self, text):
        self.driver.find_element(By.LINK_TEXT, text).click()

    def click_xpath(self, xpath):
        self.driver.find_element(By.LINK_TEXT, xpath).click()

    def click_href(self, href):
        self.driver.find_element(By.LINK_TEXT, href).click()

    def input_id(self, id, text):
        input = self.driver.find_element(By.ID, id)
        input.clear()
        input.send_keys(text)

    def input_name(self, name, text):
        input = self.driver.find_element(By.NAME, name)
        input.clear()
        input.send_keys(text)
        
    def reading_elem(self, xpath):
        reading = self.driver.find_element(By.XPATH, xpath).text
        return reading

    def click_type_button(self, type_name):
            button = self.driver.find_element(By.XPATH, f'//button[contains(@type,"{type_name}")]')
            button.click()

    def click_class_button(self, class_name):
            button = self.driver.find_element(By.XPATH, f'//button[contains(@class,"{class_name}")]')
            button.click()
            
    def hit_enter(self):
        self.driver(Keys.RETURN)

    def set_url(self, url):
        self.driver.get(url)

    def delete_cookies(self):
        self.driver.delete_all_cookies()
        print('does it cleans it?')

    def download_file(self, sorce_url, loc_repo):
        response = requests.get(sorce_url)
        with open(loc_repo, 'wb+') as f:
            f.write(response.content)


if __name__ == '__main__':
    bot = ScraperBot(url='https://wotlkdb.com')
    bot.accept_cookies()
    bot.delete_cookies()
    sleep(10)
    bot.driver.quit()
