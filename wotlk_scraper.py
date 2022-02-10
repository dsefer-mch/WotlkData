from tabnanny import verbose
from wotlk_scraper_bot import ScraperBot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import re


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

    def nav_to_main_page(self):
        action = ActionChains(self.driver)
        database = self.driver.find_element(By.LINK_TEXT, 'Database')
        action.move_to_element(database)
        action.perform()
        items = self.driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div/a[4]/span")
        action.move_to_element(items)
        action.perform()
        if self.item in Scraper.weapons:
            weapons = self.driver.find_element(By.LINK_TEXT, 'Weapons')
            action.move_to_element(weapons)
            action.perform()
            weapon = self.driver.find_element(By.LINK_TEXT, self.item).click()
            action.perform()
            try:
                filter_button = self.driver.find_element(By.XPATH, '//*[@id="fi_toggle"]').text
                print('FILTER ON/OFF?', filter_button)
                if filter_button == 'Create a filter':
                    button = self.driver.find_element(By.XPATH, '//*[@id="fi_toggle"]').click()
                action.perform()
            except:
                EC.NoSuchElementException
        else:
            armor = self.driver.find_element(By.LINK_TEXT, 'Armor')
            action.move_to_element(armor)
            action.perform()
            if self.item in Scraper.armor_08:
                armor_type_menu = self.driver.find_element(
                    By.LINK_TEXT, self.arm_type)
                action.move_to_element(armor_type_menu)
                action.perform()
                armor_item = self.driver.find_element(
                    By.LINK_TEXT, self.item).click()
                action.perform()
                try:
                    filter_button = self.driver.find_element(By.XPATH, '//*[@id="fi_toggle"]').text
                    print('FILTER ON/OFF?', filter_button)
                    if filter_button == 'Create a filter':
                        button = self.driver.find_element(By.XPATH, '//*[@id="fi_toggle"]').click()
                    action.perform()
                except:
                    EC.NoSuchElementException

    def use_web_filter(self):
        min_item_lvl = 1
        max_item_lvl = 20    # Change it for less or more scraping 10 -290
        step = 10
        bott_ilvl = 0
        top_ilvl = 9
        for ilvl_set in [(bott_ilvl + i, top_ilvl + i) for i in range(min_item_lvl, max_item_lvl, step)]:
            min_lvl = self.driver.find_element(By.NAME, 'minle')
            min_lvl.clear()
            min_lvl.send_keys(ilvl_set[0])
            max_lvl = self.driver.find_element(By.NAME, 'maxle')
            max_lvl.clear()
            max_lvl.send_keys(ilvl_set[1])
            max_lvl.send_keys(Keys.RETURN)
            self.driver.implicitly_wait(10)
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
        for i in self.list_of_items:
            if verbose == True:
                print('this is just the element i :', i)
            self.driver.get("https://wotlkdb.com/?item=" + i[1])
            scraped_data = self.driver.find_element(
                By.XPATH, "(//TD)[4]/../../../..").text
            libr = {
                'Item': scraped_data
            }
            df = df.append(libr, ignore_index=True)
        df.to_csv('data_test.csv')


if __name__ == '__main__':

    s = Scraper('Waist', 'Mail')
    s.verbose = True
    s.accept_cookies()
    s.nav_to_main_page()
    s.use_web_filter()
    s.scrape_item_nums()
    s.scrape_the_items()
    s.delete_cookies()
    s.driver.quit()
