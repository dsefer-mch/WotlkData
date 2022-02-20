from time import sleep
from unittest.util import _count_diff_all_purpose
from wotlk_scraper_bot import ScraperBot
from tabnanny import verbose
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import base64
import uuid
import json
import os
import requests
import io
from PIL import Image
import datetime


class Scraper(ScraperBot):

    weapons = ['Daggers', 'Fist Weapons', 'One-Handed Axes', 'One-Handed Maces', 'One-Handed Swords', 'Polearms', 'Staves',
               'Two-Handed Axes', 'Two-Handed Maces', 'Two-Handed Swords', 'Bows', 'Crossbows', 'Guns', 'Thrown', 'Wands']
    armor = ['Chest', 'Feet', 'Hands', 'Head', 'Legs', 'Shoulder', 'Wrist', 'Waist', 'Cloaks',
             'Shields', 'Amulets', 'Rings', 'Trinkets', 'Idols', 'Librams', 'Totems', 'Sigils']
    armor_type = ['Cloth', 'Leather', 'Mail', 'Plate']
    armor_08 = ['Chest', 'Feet', 'Hands', 'Head',
                'Legs', 'Shoulder', 'Wrist', 'Waist']

    def __init__(self, item, arm_type='Plate'):

        super().__init__()
        self.item = item
        self.arm_type = arm_type
        self.list_of_items = []
        self.list_img_couples = []
        self.dpoint_name = None

    def nav_to_main_page(self):
        self.hoover_over(text='Database')
        self.hoover_over(xpath="//span[text()='Items']")

        if self.item in Scraper.weapons:
            self.hoover_over(text='Weapons')
            self.click_text(text=self.item)
            try:
                filter_switch = self.reading_elem(xpath='//*[@id="fi_toggle"]')
                print('FILTER ON/OFF?', filter_switch)
                if filter_switch == 'Create a filter':
                    print('da sravnqva gi pravilno ')
                    self.click_xpath(xpath='//*[@id="fi_toggle"]')
            except:
                print('Filter switch not found.')
        else:
            self.hoover_over(text='Armor')
            if self.item in Scraper.armor_08:
                self.hoover_over(text=self.arm_type)
                self.click_text(text=self.item)
                try:
                    filter_switch = self.reading_elem(
                        xpath='//*[@id="fi_toggle"]')
                    if filter_switch == 'Create a filter':
                        self.click_xpath(xpath='//*[@id="fi_toggle"]')
                except:
                    print('Filter switch not found.')

    def use_web_filter(self):
        min_item_lvl = 1
        max_item_lvl = 30  # Change it for less or more scraping 10 -290
        step = 10
        bott_ilvl = 0
        top_ilvl = 9
        for ilvl_set in [(bott_ilvl + i, top_ilvl + i) for i in range(min_item_lvl, max_item_lvl, step)]:
            self.input_name('minle', ilvl_set[0])
            max_lvl = self.input_name('maxle', ilvl_set[1])
            self.hit_enter(max_lvl)
            self.scrape_item_nums()

    def scrape_item_nums(self):
        all_items_list = re.findall(r'(\w+)=(\d+)', self.driver.page_source)
        all_items_list_as_a_list = [
            list(element_in_the_item_list) for element_in_the_item_list in all_items_list]
        list_of_real_items = []
        [list_of_real_items.append(element) for element in all_items_list_as_a_list if element[0]
         == 'item' if element not in list_of_real_items]
        self.list_of_items += list_of_real_items

    def scrape_the_items(self):
        df = pd.DataFrame({})
        if self.item in Scraper.armor_08:
            dp_dir_name = self.item + '.' + self.arm_type + '@' + self.date_id()
        else:
            dp_dir_name = self.item + '@' + self.date_id()
        dpoint_name = self.create_dir(
            name=dp_dir_name, parent_dir=os.path.dirname(os.path.realpath(__file__)) + '/raw_data')
        self.dpoint_name = dpoint_name
        for i in self.list_of_items:
            # if verbose == True:
            #     print('this is just the element i :', i)
            item_url = "https://wotlkdb.com/?item=" + i[1]
            self.set_url(item_url)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "(//TD)[4]/../../../..")))
            scraped_data = self.driver.find_element(
                By.XPATH, "(//TD)[4]/../../../..").text
            id = self.list_of_items.index(i)
            uuid = self.get_uuid()
            self.scrape_image_elements(data=scraped_data, id=id)
            libr = {
                'ID': id,
                'UUID': uuid,
                'Web Item Number': i[1],
                'Item': scraped_data
            }
            df = df.append(libr, ignore_index=True)
        df.to_json(self.dpoint_name + '/data.json')
        df.to_csv(self.dpoint_name + '/data.csv')

    def scrape_image_elements(self, data, id):
        img_src_url_elements = re.findall(
            r"(\w+)/(\w+[.]+\bjpg)", self.driver.page_source)
        img_src_url_element = [
            element[1] for element in img_src_url_elements if element[0] == 'large']
        img_elem_str = img_src_url_element[0]
        item_name_list = data.split('\n')
        item_name = item_name_list[0]
        image_couple = [item_name, img_elem_str, id]
        self.list_img_couples.append(image_couple)

    def images(self):
        df_img = pd.DataFrame({})
        img_dir = self.create_dir(name='images', parent_dir=self.dpoint_name)
        for couple in self.list_img_couples:
            link = 'https://wotlkdb.com/static/images/wow/icons/large/' + \
                couple[1]
            try:
                self.set_url(link)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
            except ConnectionResetError:
                print('Connection Error')
                continue
            try:
                img_src = self.driver.find_element(
                    By.XPATH, '/html/body/img').get_attribute('src')
            except:
                print('Source not found')
                continue
            self.download_img(img_src, id=couple[2], img_parent_dir=img_dir)
            lib = {
                'id': couple[2],
                'Item Name': couple[0],
                'Image source link': link
            }
            df_img = df_img.append(lib, ignore_index=True)
        df_img.to_csv(self.dpoint_name + '/images_link_data.csv')
        self.dpoint_name = None            # That resets datapoint id name

    def download_img(self, src_url, id, img_parent_dir):
        try:
            image_content = requests.get(src_url).content
        except ConnectionResetError:
            print('Connection Error')
        finally:  # need to think about it
            pass
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(img_parent_dir, str(id) + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)

    def get_uuid(self):
        rand_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        return str(rand_uuid).replace('=', '')

    def date_id(self):
        current_date = datetime.datetime.now()
        return current_date.strftime("%Y%m%d%H%M%S")


if __name__ == '__main__':

    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    for item in Scraper.armor_08:
        for armor_type in Scraper.armor_type:
            scrape_test1 = Scraper(item, armor_type)
            scrape_test1.accept_cookies(xpath='//*[@class="ncmp__btn"]')
            scrape_test1.nav_to_main_page()
            scrape_test1.use_web_filter()
            scrape_test1.scrape_the_items()
            scrape_test1.images()
            scrape_test1.delete_cookies()
            scrape_test1.driver.quit()
