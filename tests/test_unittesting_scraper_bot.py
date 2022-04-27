import unittest
import sys
import os
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from src.scraper_bot import ScraperBot


class ScraperBotTestCase(unittest.TestCase):

    def setUp(self):
        self.scraper = ScraperBot(verbose=True)
        self.scraper.set_url('https://wotlkdb.com/')

    def test_accept_cookies(self):
        sleep(2)
        obj = self.scraper.driver.find_element(By.XPATH, '//*[@class="ncmp__btn"]')
        self.assertTrue(obj.text, 'Accept')

    def test_hoover_over(self):
        self.scraper.hoover_over(text='Database')
        sleep(2)
        obj = self.scraper.driver.find_element(By.LINK_TEXT, 'NPCs')
        self.assertTrue(obj.text, 'NPCs')

    def test_click_text(self):
        self.scraper.driver.find_element(By.LINK_TEXT, 'About us & contact').click()
        obj = self.scraper.driver.find_element(By.LINK_TEXT, 'Warcraft Tavern')
        self.assertTrue(obj.text, 'Warcraft Tavern')

    def test_click_xpath(self):
        self.scraper.driver.find_element(By.XPATH, '/html/body/div[4]/div/a[1]').click()
        obj = self.scraper.driver.find_element(By.LINK_TEXT, 'Warcraft Tavern')
        self.assertTrue(obj.text, 'Warcraft Tavern')

    def test_input_name(self):
        input = self.scraper.driver.find_element(By.NAME, 'search')
        input.send_keys('lelq veska 47')
        obj = self.scraper.driver.find_element(By.XPATH, '//*[@id="home-search"]/form/input')
        self.assertTrue('lelq veska 47', obj.text)


    def test_reading_elem(self):
        reading = self.scraper.driver.find_element(By.XPATH, '//*[@id="home-menu"]/span/a[4]/span').text
        self.assertTrue(reading, 'More')


    def test_hit_enter(self):
        input = self.scraper.driver.find_element(By.NAME, 'search')
        input.send_keys('lelq milka &&')
        input.send_keys(Keys.ENTER)
        obj = self.scraper.driver.find_element(By.XPATH, '//*[@id="main-contents"]/div/h1/i')
        self.assertTrue('lelq milka &&', obj.text)


if __name__ == "__main__":
    unittest.main()
