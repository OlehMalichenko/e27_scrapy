import csv
from e27.gclient import Gclient
from pprint import pprint


class E27Pipeline(object):


    def __init__(self):

        self.client = Gclient()


# =========
    def process_item(self, item, spider):
        if spider.name == 'e27links':
            print(item['link'])

            block_links = list()
            block_links.append(item['link'])
            block_links.append(item['link_general'])
            # block_links.append(item['link_fundings'])
            # block_links.append((item['link_teammembers']))

            self.links.append(block_links)

        elif spider.name == 'e27main':
            print(item['name'])

            block_mains = list()
            block_mains.append(item['name'])
            block_mains.append(item['profile_url'])
            block_mains.append(item['website'])
            block_mains.append(item['location'])
            block_mains.append(item['tags'])
            block_mains.append(item['founding_date'])
            block_mains.append(item['founders'])
            block_mains.append(item['employee'])
            block_mains.append(item['urls'])
            block_mains.append(item['emails'])
            block_mains.append(item['phones'])
            block_mains.append(item['short_description'])
            block_mains.append(item['description'])

            self.main_data.append(block_mains)

        return item


# =========WRITE FROM FIRST CROWLER========= #
    def insert_url_title(self):
        title_row = ['MAIN', 'GENERAL']
        self.links.insert(0, title_row)

    def write_link_sheet(self):
        last_row = len(self.links)
        last_col = len(self.links[0])
        cell_list = self.sheet_url.range(1, 1, last_row, last_col)

        for cell in cell_list:
            try:
                cell.value = self.links[cell.row - 1][cell.col - 1]
            except:
                cell.value = 'error read'

        self.sheet_url.update_cells(cell_list)

    def write_link_csv(self):
        with open('e27links.csv', 'w', newline='\n', encoding='utf8') as file:
            writer = csv.writer(file)

            for link in self.links:
                writer.writerow(link)


# =========WRITE FROM SECOND CROWLER========= #
    def insert_main_title(self):
        title_row = ['company_name', 'profile_url', 'company_website_url',
                     'location', 'tags', 'founding_date',
                     'founders', 'employee_range', 'urls',
                     'emails', 'phones', 'description_short', 'description']
        self.main_data.insert(0, title_row)

    def write_main_sheet(self):
        last_row = len(self.main_data)
        last_col = len(self.main_data[0])
        cell_list = self.sheet_res.range(1, 1, last_row, last_col)

        for cell in cell_list:
            try:
                cell.value = self.main_data[cell.row - 1][cell.col - 1]
            except:
                cell.value = 'error read'

        self.sheet_res.update_cells(cell_list)

    def write_main_csv(self):
        with open('e27main.csv', 'w', newline='\n', encoding='utf8') as file:
            writer = csv.writer(file)

            for block in self.main_data:
                writer.writerow(block)


# =========OPEN-CLOSE SPIDERS========= #
    def open_spider(self, spider):
        print(' pipelines spider open:  ' + spider.name)

        if spider.name == 'e27links':
            self.links = list()
            self.sheet_url = self.client.get_sheet_url()

        elif spider.name == 'e27main':
            self.main_data = list()
            self.sheet_res = self.client.get_sheet_result()
            print('sheet name: ' +str(self.sheet_res.title))

    def close_spider(self, spider):
        print(' pipelines spider close:  ' + spider.name)

        if spider.name == 'e27links':
            self.insert_url_title()
            self.write_link_csv()
            self.write_link_sheet()

        elif spider.name == 'e27main':
            self.insert_main_title()
            self.write_main_sheet()
            self.write_main_csv()