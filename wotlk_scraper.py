        self.num_of_items = num_of_items
    def num_of_items_on_the_page(self):
        try:
            num_of_items = int(self.driver.find_element_by_xpath('//*[@class="listview-note"]').text.split()[0])
        except:
             EC.NoSuchElementException('Number of items cannot be determined.')