from scraper_bot import ScraperBot
from aws_rds_client import Client
from aws_rds_client import Query
from aws_rds_client import Meta
from aws_rds_client import Load
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import base64
import uuid
import os
import requests
import io
from PIL import Image
import datetime
import boto3


class Scraper(ScraperBot):

    """
    Scrapes item discription and icon images from 
    World of warcraft (the Lich King expansion v3.3.5)
    data base website.
    """

    weapons = ['Daggers', 'Fist Weapons', 'One-Handed Axes', 'One-Handed Maces', 'One-Handed Swords', 'Polearms', 'Staves',
               'Two-Handed Axes', 'Two-Handed Maces', 'Two-Handed Swords', 'Bows', 'Crossbows', 'Guns', 'Thrown', 'Wands']  # These are item names
    armor = ['Cloaks', 'Shields', 'Amulets', 'Rings',
             'Trinkets', 'Idols', 'Librams', 'Totems', 'Sigils']  # These are item names
    armor_08 = ['Chest', 'Feet', 'Hands', 'Head',
                'Legs', 'Shoulder', 'Wrist', 'Waist']  # These are item names
    armor_type = ['Cloth', 'Leather', 'Mail',
                  'Plate']  # These are NOT item names

    def __init__(self, item, arm_type='Plate', **kwds):
        super().__init__(**kwds)

        self.item = item
        self.arm_type = arm_type
        self.list_couples = []
        self.dpoint_name = None
        self.img_dir = None
        self.dp_dir_name = None
        self.df = pd.DataFrame({})
        self.df_img = pd.DataFrame({})

        # Declare directory & cradential paths
        self.curr_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.par_dir_path = os.path.abspath(
            os.path.join(self.curr_dir_path, os.pardir))
        self.cred_path = self.par_dir_path + '/config/cred.json'

    def local_config(self):
        """
        Creates local /raw_data directory and sets paths
        """

        if os.path.isdir(self.curr_dir_path + '/raw_data') == False:
            self.create_dir(name='raw_data', dir_path=self.curr_dir_path)
        if self.item in Scraper.armor_08:
            self.dp_dir_name = self.item + '.' + self.arm_type + '@' + self.date_id()
        else:
            self.dp_dir_name = self.item + '@' + self.date_id()
        self.dpoint_name = self.create_dir(
            name=self.dp_dir_name, dir_path=self.curr_dir_path + '/raw_data')
        self.img_dir = self.create_dir(
            name='images', dir_path=self.dpoint_name)

    def nav_to_main_page(self):
        """
        Navigate to desired item category page and set the filter.
        """
        self.set_url('https://wotlkdb.com/')
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@class="ncmp__btn"]')))
            self.accept_cookies(xpath='//*[@class="ncmp__btn"]')
        except TimeoutException:
            print("Cookies timeout exeption.")
        self.hoover_over(text='Database')
        self.hoover_over(xpath="//span[text()='Items']")
        if self.item in Scraper.weapons:
            self.hoover_over(text='Weapons')
        elif self.item in Scraper.armor or self.item in Scraper.armor_08:
            self.hoover_over(text='Armor')
            if self.item in Scraper.armor_08:
                self.hoover_over(text=self.arm_type)
        else:
            print("Please correct item argument.")
            self.shut()
        self.click_text(text=self.item)
        filter_switch = self.reading_elem(xpath='//*[@id="fi_toggle"]')
        if filter_switch == 'Create a filter':
            self.click_xpath(xpath='//*[@id="fi_toggle"]')

    def use_web_filter(self):
        """
        Define ranges of items (on the base of >item level< stat).
        The largest rang is 1 - 290.
        """
        min_item_lvl = 1
        max_item_lvl = 290  # Change it for less or more scraping 10 -290
        if self.verbose:
            print('Range of >item level< stat are set to - min:',
                  min_item_lvl, ', max:', max_item_lvl)
            print(
                'If you need different range, please change values inside >> def use_web_filter.')
        step = 10
        bott_ilvl = 0
        top_ilvl = 9
        for ilvl_set in [(bott_ilvl + i, top_ilvl + i) for i in range(min_item_lvl, max_item_lvl, step)]:
            self.input_name('minle', ilvl_set[0])
            max_lvl = self.input_name('maxle', ilvl_set[1])
            self.hit_enter(max_lvl)
            self.parsing_data()

    def parsing_data(self):
        """
        Scraping unique web-number for each item on the page.
        """
        elementSource = self.driver.find_elements(By.CLASS_NAME, 'iconmedium')
        for elements in elementSource:
            text_to_clear = str(elements.get_attribute("innerHTML"))
            img_url1 = text_to_clear.split(';')
            final_url = img_url1[1].split('&')
            FINAL_URL = re.sub("medium", "large", final_url[0])
            item_num1 = re.findall(r"(\d+)", img_url1[3])
            item_num = item_num1[0]
            couple = [item_num, FINAL_URL]
            self.list_couples.append(couple)

    def scrape_items(self):
        """
        Scraping item data.
        """

        list_data_lib = []
        list_url_lib = []
        if len(self.list_couples) != 0:
            for couple in self.list_couples:
                id0 = self.list_couples.index(couple)
                id = id0 + 1
                uuid = self.get_uuid()

                item_url = "https://wotlkdb.com/?item=" + couple[0]
                self.set_url(item_url)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "(//TD)[4]/../../../..")))
                scraped_data = self.driver.find_element(
                    By.XPATH, "(//TD)[4]/../../../..").text

                data_lib = {
                    'ID': id,
                    'UUID': uuid,
                    'Web Item Number': couple[0],
                    'Item Info': scraped_data
                }
                list_data_lib.append(data_lib)
                self.df = pd.DataFrame.from_records(list_data_lib)

                url_lib = {
                    'Web Item Number': couple[0],
                    'Image source link': item_url
                }
                list_url_lib.append(url_lib)
                self.df_img = pd.DataFrame.from_records(list_url_lib)
                self.download_img(src_url=couple[1], id=id)

            self.driver.quit()

        else:
            print("There are no items to scrape with this web-filter.")
            self.shut()

    def data_procesing(self):
        """
        Saves data localy and AWS - EC2 & RDS.
        """

        image_data_table = "image_data"

        # saving data localy
        self.df.to_json(self.dpoint_name + '/data.json')
        self.df.to_csv(self.dpoint_name + '/data.csv')
        self.df_img.to_csv(self.dpoint_name + '/images_link_data.csv')

        # uploading data to AWS RDS local call out
        # Client.from_json(self.cred_path)
        # with open("rds_cred.json", "w") as jf:
        #     json.dump(cred_dict, jf)

        # uploading data to AWS RDS docker-EC2
        # Client.env_var()

        # Load.create_and_load_pd(self.df, f'data_of_{self.dp_dir_name}')
        # res = Meta.checkTableExists(self.cred_path, tablename=image_data_table)
        # if res:
        #     Load.create_and_load_pd(self.df_img, 'image_data_demo')
        #     # scalability check
        #     df_query = Query.query(
        #         'SELECT * FROM image_data id JOIN image_data_demo d ON id."Web Item Number" = d."Web Item Number"')
        #     if df_query.empty:
        #         appending_image_data_table_query = Query.query(
        #             'INSERT INTO "image_data" ("Web Item Number", "Image source link") SELECT * FROM "image_data_demo"')
        #     else:
        #         unique_img_table_query = Query.query(
        #             'SELECT * FROM image_data UNION SELECT * FROM image_data_demo')
        #         Load.create_and_load_pd(unique_img_table_query, 'image_data1')
        #         Load.drop('image_data')
        #         new_data_df = Query.fetchall('image_data1')
        #         Load.create_and_load_pd(new_data_df, 'image_data')
        #         Load.drop('image_data1')
        #     Load.drop('image_data_demo')
        # else:
        #     Load.create_and_load_pd(self.df_img, image_data_table)

        # s3_client = boto3.client('s3')
        # try:
        #     response = s3_client.upload_file(file_name=self.dpoint_name + '/data.json',
        #                                      bucket='wotk.proj',
        #                                      object_name='/raw_data/' + self.dp_dir_name + '/data.json'
        #                                      )
        #     print('Image uploaded to s3')
        # except:
        #     print('File (image) NOT uploaded!')

        # # # uploading image to AWS s3
        # list_of_img_files = os.listdir(self.img_dir)
        # for file in list_of_img_files:
        #     img_name = self.img_dir + '/' + file
        #     s3_path = '/raw_data/' + self.dp_dir_name + '/image/' + file
        #     try:
        #         response = s3_client.upload_file(file_name=img_name,
        #                                          bucket='wotk.proj',
        #                                          object_name=s3_path
        #                                          )
        #         print('Image uploaded to s3')
        #     except:
        #         print('File (image) NOT uploaded!')

    def download_img(self, src_url, id):
        """
        Downloading and saving images localy.
        """
        try:
            r = requests.get(src_url).content
        except requests.exceptions.HTTPError:
            print("HttpError found while request to: ", src_url)
        except requests.exceptions.ConnectionError:
            print("ConnectionError found while request to: ", src_url)
        except requests.exceptions.Timeout:
            print("Timeout exception for: ", src_url)
        except requests.exceptions.RequestException:
            print("Refused request to ", src_url)
        bit_image = io.BytesIO(r)
        image = Image.open(bit_image)  # .convert('RGB')
        image_file_name = os.path.join(self.img_dir, str(id) + '.jpg')
        with open(image_file_name, 'wb') as f:
            image.save(f, "JPEG", quality=85)

    def get_uuid(self):
        """
        Generates universally unique id.
        """
        rand_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        return str(rand_uuid).replace('=', '')

    def date_id(self):
        """
        Generates date id.
        """
        current_date = datetime.datetime.now()
        return current_date.strftime("%Y%m%d%H%M%S")


if __name__ == '__main__':

    for item in Scraper.armor_08:  # <<-- Scraping armor from armor_08 list
        for armor_type in Scraper.armor_type:
            # <<-- HERE add headless=True for Ec2 , opt verbose. Pattern doesn't matter
            scrape_test1 = Scraper(
                item, armor_type, verbose=True, headless=True)
            scrape_test1.local_config()
            scrape_test1.nav_to_main_page()
            scrape_test1.use_web_filter()
            scrape_test1.scrape_items()
            scrape_test1.data_procesing()

    for item in Scraper.armor:  # <<-- Screaping armor from armor list
        # <<-- HERE add headless=True for Ec2 , opt verbose. Pattern doesn't matter
        scrape_test1 = Scraper(item, verbose=True, headless=True)
        scrape_test1.local_config()
        scrape_test1.nav_to_main_page()
        scrape_test1.use_web_filter()
        scrape_test1.scrape_items()
        scrape_test1.data_procesing()

    for item in Scraper.weapons:  # <<-- Scraping weapons
        # <<-- HERE add headless=True for Ec2 , opt verbose. Pattern doesn't matter
        scrape_test1 = Scraper(item, verbose=True, headless=True)
        scrape_test1.local_config()
        scrape_test1.nav_to_main_page()
        scrape_test1.use_web_filter()
        scrape_test1.scrape_items()
        scrape_test1.data_procesing()

    scrape_test1.shut()

    # # -- HERE add headless=True for Ec2 , opt verbose.
    # scrape_test1 = Scraper(item='Bows',
    #                        verbose=True, headless=True)
    # scrape_test1.local_config()
    # scrape_test1.nav_to_main_page()
    # scrape_test1.use_web_filter()
    # scrape_test1.scrape_items()
    # scrape_test1.data_procesing()
