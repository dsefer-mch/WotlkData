from urllib import response
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
import os
import boto3
from sqlalchemy import create_engine
import yaml

class ScraperBot():
    def __init__(self,credens , headless=False, verbose=False ):

        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")	
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.driver.maximize_window()
        self.verbose = verbose

        # with open(credens, 'r') as f:
        #     credens = yaml.safe_load(f)
        # DATABASE_TYPE = credens['DATABASE_TYPE']
        # DBAPI = credens['DBAPI']
        # HOST = credens['HOST']
        # USER = credens['USER']
        # PASSWORD = credens['PASSWORD']
        # DATABASE = credens['DATABASE']
        # PORT = credens['PORT']

        # self.engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
        self.engine = create_engine('postgresql://postgres_wtlk_db@scrap-wtlk-db.cc7x6bcgkame.eu-west-1.rds.amazonaws.com:5432/scrap-wtlk-db')
        # self.engine.connect()
    def accept_cookies(self, xpath=None, iframe=None):
        accept_button = None
        if iframe:
            try:
                self.driver.switch_to.frame(iframe)
            except:
                if self.verbose:
                    print('Unable to switch to selected iframe')
        if xpath:
            try:
                accept_button = self.driver.find_element(By.XPATH, xpath)
            except:
                if self.verbose:
                    print('Xpath object not found')
        if not accept_button:
            print('accept but', accept_button)
            try:
                print('im trying accept button')
                accept_button = self.driver.find_element(
                    By.LINK_TEXT, 'Accept')
            except:
                if self.verbose:
                    print('"Accept" button not found')
        print(accept_button)
        if accept_button:
            try:
                accept_button.click()
            except:
                if self.verbose:
                    print('Cookies not detected.')

    def hoover_over(self, text=None, xpath=None):
        action = ActionChains(self.driver)
        if text:
            text_obj = self.driver.find_element(By.LINK_TEXT, text)
            action.move_to_element(text_obj)
            action.perform()
        if xpath:
            xpath_obj = self.driver.find_element(By.XPATH, xpath)
            action.move_to_element(xpath_obj)
            action.perform()

    def click_text(self, text):
        self.driver.find_element(By.LINK_TEXT, text).click()

    def click_xpath(self, xpath):
        self.driver.find_element(By.XPATH, xpath).click()

    def click_href(self, href):
        self.driver.find_element(By.LINK_TEXT, href).click()

    def input_id(self, id, text):
        input = self.driver.find_element(By.ID, id)
        input.clear()
        input.send_keys(text)
        return input

    def input_name(self, name, text):
        input = self.driver.find_element(By.NAME, name)
        input.clear()
        input.send_keys(text)
        return input

    def reading_elem(self, xpath):
        reading = self.driver.find_element(By.XPATH, xpath).text
        return reading

    def click_type_button(self, type_name):
        button = self.driver.find_element(
            By.XPATH, f'//button[contains(@type,"{type_name}")]')
        button.click()

    def click_class_button(self, class_name):
        button = self.driver.find_element(
            By.XPATH, f'//button[contains(@class,"{class_name}")]')
        button.click()

    def hit_enter(self, obj):
        obj.send_keys(Keys.ENTER)
        return

    def set_url(self, url):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            if self.verbose:
                print('Selenium opens ', url)
        except:
            print('No internet connection or bad url.')
        return

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def create_dir(self, name, parent_dir=None):
        dir_name = name
        if parent_dir == None:
            curr_dir = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(curr_dir, dir_name)
        else:
            path = os.path.join(parent_dir, dir_name)
        try:
            os.mkdir(path)
            if self.verbose:
                if self.verbose:
                    print("Directory '% s' created" % dir_name)
        except OSError as error:
            print(error)
            if self.verbose:
                print(
                    '</raw_data> directory is created at the start of scraping. Ignore this directory error massage.')
        return path

    def create_dir_drop_file(self, full_path, data):
        f_name = full_path
        os.makedirs(os.path.dirname(f_name), exist_ok=True)
        with open(f_name, "w") as f:
            f.write(data)

    def download_file(self, sorce_url, loc_repo):
        response = requests.get(sorce_url)
        with open(loc_repo, 'wb+') as f:
            f.write(response.content)

    def s3_up(self, file_name_or_img, bucket_name, obj_name):
        s3_client = boto3.client('s3') #, aws_access_key_id=#aws_config_file, region_name=...,aws_secret_access_key=...)
        try:
            response = s3_client.upload_file(file_name_or_img, bucket_name, obj_name)
        except:
            print('File NOT uploaded!')


if __name__ == '__main__':
    bot = ScraperBot(credens='config/rds_credens.yaml')
    bot.accept_cookies(xpath='//*[@class="ncmp__btn"]')
    bot.delete_cookies()
    bot.driver.quit()
