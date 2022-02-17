from time import sleep
from wotlk_scraper_bot import ScraperBot
from tabnanny import verbose
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
        database = self.hoover_over(text='Database')
        items = self.hoover_over(xpath="//span[text()='Items']")

        if self.item in Scraper.weapons:
            weapons = self.hoover_over(text='Weapons')
            weapon = self.click_text(text=self.item)
            try:
                filter_switch = self.reading_elem(xpath='//*[@id="fi_toggle"]')
                print('FILTER ON/OFF?', filter_switch)
                if filter_switch == 'Create a filter':
                    print('da sravnqva gi pravilno ')
                    button = self.click_xpath(xpath='//*[@id="fi_toggle"]')
            except:
                print('Filter switch not found.')
        else:
            armor = self.hoover_over(text='Armor')
            if self.item in Scraper.armor_08:
                armor_type_menu = self.hoover_over(text=self.arm_type)
                armor_item = self.click_text(text=self.item)
                try:
                    filter_switch = self.reading_elem(xpath='//*[@id="fi_toggle"]')
                    print('FILTER ON/OFF?', filter_switch)
                    if filter_switch == 'Create a filter':
                        print('da sravnqva gi pravilno ')
                        button = self.click_xpath(xpath='//*[@id="fi_toggle"]')
                except:
                    print('Filter switch not found.')

    def use_web_filter(self):
        min_item_lvl = 1
        max_item_lvl = 20    # Change it for less or more scraping 10 -290
        step = 10
        bott_ilvl = 0
        top_ilvl = 9
        for ilvl_set in [(bott_ilvl + i, top_ilvl + i) for i in range(min_item_lvl, max_item_lvl, step)]:
            min_lvl = self.input_name('minle', ilvl_set[0])
            max_lvl = self.input_name('maxle', ilvl_set[1])
            print('1')
            self.hit_enter(max_lvl)
            print('2')
            sleep(5)
            self.driver.implicitly_wait(10)
            print('3')
            self.scrape_item_nums()
            print('4')

    def scrape_item_nums(self):
        print('does it even reach inside here?')
        all_items_list = re.findall(r'(\w+)=(\d+)', self.driver.page_source)
        all_items_list_as_a_list = [
            list(element_in_the_item_list) for element_in_the_item_list in all_items_list]
        list_of_real_items = []
        [list_of_real_items.append(element) for element in all_items_list_as_a_list if element[0]
         == 'item' if element not in list_of_real_items]
        self.list_of_items += list_of_real_items
        print(list_of_real_items)
        print(self.list_of_items)

    def scrape_the_items(self):
        print('here we start scraping items')
        df = pd.DataFrame({})
        print('here we start scraping items2')
        for i in self.list_of_items:
            print('here we start scraping items3')
            # if verbose == True:
            #     print('this is just the element i :', i)
            item_url = "https://wotlkdb.com/?item=" + i[1]
            self.driver.get(item_url)
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            scraped_data = self.driver.find_element(
                By.XPATH, "(//TD)[4]/../../../..").text
            libr = {
                'Item': scraped_data
            }
            df = df.append(libr, ignore_index=True)
            print(df)
        df.to_csv('data_test.csv')
        print(df)

    def scrape_image(self):
        try:
            address_str = re.findall(r'(\w+)=(\w+)', self.driver.page_source)
            address_str_list = [list(element_in_address_str) for element_in_address_str in address_str]
            address_filter_list = []
            [address_filter_list.append(element) for element in address_str_list if element[0]=='style' if 'background-image' in element[1]]
            link_list = []
            if address_filter_list:
                for element in address_filter_list:
                    link = element[1].split('"')[-1]
        except:
            print('No image link found')
        




if __name__ == '__main__':


    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')

    # bot = ScraperBot(url='https://wotlkdb.com')
    # bot.accept_cookies(xpath='//*[@id="ncmp__tool"]')
    scrape_test1 = Scraper('Guns')
    scrape_test1.accept_cookies(xpath='//*[@class="ncmp__btn"]')
    scrape_test1.nav_to_main_page()
    scrape_test1.use_web_filter()
    # scrape_test1.scrape_item_nums()
    scrape_test1.scrape_the_items()
    scrape_test1.delete_cookies()
    scrape_test1.driver.quit()
