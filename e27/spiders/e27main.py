import scrapy
import json
from e27.items import E27Item
from e27.gclient import Gclient
from pprint import pprint
import random

# =============!!!!!!!!!!!!!!!   RANDOM   !!!!!!!!!!!!!================== #

# =============!!!!!!!!!!!!!!!   git hub   !!!!!!!!!!!!!================== #

class E27TttSpider(scrapy.Spider):

    name = 'e27main'
    allowed_domains = ['e27.co']



#               =========START=========
    def start_requests(self):
        client = Gclient()
        sheet_url = client.get_sheet_url()

        random_url_list = self.get_random_url_list(sheet_url)

        for url_general in random_url_list:
            yield scrapy.Request(url_general)




    def get_random_url_list(self, sheet_url):
        all_rows_list = sheet_url.get_all_values()

        count_rows = len(all_rows_list)
        indexes = self.get_random_indexes(count_rows)

        r_url_list = list()

        for index in indexes:
            url = all_rows_list[index][1]
            if url is None or url is '':
                continue

            r_url_list.append(url)

        return r_url_list



    def get_random_indexes(self, last: int):
        set_rand = set()

        while len(set_rand) <= 250:
            r = random.randint(2, last)
            set_rand.add(r)

        return set_rand



    def parse(self, response):
        if response:
            try:
                # preparation data and get id
                dic_data = json.loads(response.body)
                data = dic_data['data']
                id = data['id']

                # get data from body
                item = E27Item()
                item['name'] = data['name']
                item['tags'] = self.get_market(data['market'])
                item['profile_url'] = 'https://e27.co/startups/%s' % data['slug']
                item['website'] = data['metas']['website']
                item['emails'] = data['metas']['email']
                item['location'] = self.get_location(data['location'])
                item['urls'] = self.get_urls(data['metas'])
                description_tupl = self.get_description(data['metas'])
                item['description'] = description_tupl[0]
                item['short_description'] = description_tupl[1]
                item['founding_date'] = self.get_date(data['metas'])
                item['phones'] = ''

            except:
                return

            # preparation urls for next steps
            url_fundings = 'https://e27.co/api/startups/get/?startup_id=%s&data_type=fundings' % id
            url_team = 'https://e27.co/api/startups/get/?id=%s&data_type=teammembers' % id

            # go to next step with item
            yield scrapy.Request(url=url_fundings,
                                 callback=self.step_1_fundings,
                                 meta={'item': item, 'url_team': url_team})



#               =========NEXT STEPS=========
    def step_1_fundings(self, response):
        if response:
            # pull out item
            item = response.meta['item']

            try:
                # get body for transform to dict
                body = response.body
                dic = json.loads(body)
                blocks = dic['data']

            except:
                # return empty item_founders
                item['founders'] = ''

            else:
                if len(blocks) == 0:
                    item['founders'] = ''
                else:
                    item['founders'] = self.get_investors(blocks)

            finally:
                # pull out url for next step
                url_team = response.meta['url_team']

                # go to next step
                yield scrapy.Request(url=url_team,
                                     callback=self.step_2_employee,
                                     meta={'item': item})


    def step_2_employee(self, response):
        if response:
            # pull out item
            item = response.meta['item']

            try:
                # get body for transform to dict
                body = response.body
                dic = json.loads(body)
                blocks = dic['data']

            except:
                item['employee'] = ''

            else:

                if len(blocks) == 0:
                    item['employee'] = ''
                else:
                    item['employee'] = self.get_employee(blocks)

            finally:
                yield item




#               =========GET DATA=========
    def get_date(self, metas_block):
        try:
            year = metas_block['found_year'].strip()
            month = metas_block['found_month'].strip()
        except:
            return ''
        else:
            if year is '' or year is '0':
                return ''
            if len(month) == 1:
                month = '0' + month
            return year + '-' + month


    def get_description(self, metas_block):
        try:
            description = metas_block['description']
            short_description = metas_block['short_description']
        except:
            return ('', '')
        else:
            return (description, short_description)


    def get_urls(self, metas_block):
        try:
            linkedin = metas_block['linkedin'] + '\n' if metas_block['linkedin'] is not '' else ''
            twitter = 'Twitter: ' + metas_block['twitter'] + '\n' if metas_block['twitter'] is not '' else ''
            facebook = metas_block['facebook'] if metas_block['facebook'] is not '' else ''
        except:
            return ''
        else:
            return linkedin + twitter + facebook


    def get_location(self, location_block):
        try:
            zero_block = location_block[0]
            location = zero_block['text']
        except:
            return ''
        else:
            return location


    def get_market(self, market_crude):
        try:
            market = market_crude.replace('[', '').replace(']', '')
        except:
            return ''
        else:
            return market


    def get_investors(self, blocks):
        count_nonames = 0
        names = str()

        for b in blocks:
            for i in blocks[b]['investors']:

                try:
                    name = i['name'] + '\n'
                    names = names + name
                except:
                    count_nonames += 1

        if count_nonames != 0:
            names = names + 'No names investors: %s' % str(count_nonames)

        return names


    def get_employee(self, blocks):
        count_nonames = 0
        names = str()

        for b in blocks:

            try:
                name = b['name'] + '\n'
                names = names + name
            except:
                count_nonames += 1

        if count_nonames != 0:
            names = names + 'No names employee: %s' % str(count_nonames)

        return names