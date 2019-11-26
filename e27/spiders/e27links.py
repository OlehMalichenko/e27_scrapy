import scrapy
from e27.items import E27Item
from pprint import pprint
import json


class E27linksSpider(scrapy.Spider):
    name = 'e27links'
    allowed_domains = ['e27.co']



    def start_requests(self):
        return [scrapy.Request('https://e27.co/api/startups/?tab_name=recentlyupdated&start=0&length=1',
                               callback=self.start_parse)]



    def start_parse(self, response):
        try:
            r = json.loads(response.body)
            total_count = int(r['data']['totalstartupcount'])
        except:
            return
        else:
            url_list = self.get_url_list(total_count)

            for url in url_list:
                yield scrapy.Request(url, callback=self.parse)



    def get_url_list(self, total_count: int):
        url_list = list()
        length = 1000

        while total_count < length:
            length = length/10

        for start in range(0, total_count, length):
            url = 'https://e27.co/api/startups/?tab_name=recentlyupdated&start=%s&length=%s' % (str(start), str(length))
            url_list.append(url)

        return url_list

     

    def parse(self, response):
        if response :
            dic_data = json.loads(response.body)

            if len(dic_data['data']['list']) == 0:
                print('data empty' + str(response.url))
                return

            for block in dic_data['data']['list']:

                try:
                    item = E27Item()
                    item['link']             = 'https://e27.co/startups/%s' % block['slug']
                    item['link_general']     = 'https://e27.co/api/startups/get/?slug=%s' \
                                               '&data_type=general' % block['slug']
                    # item['link_fundings']    = 'https://e27.co/api/startups/get/?startup_id=%s' \
                    #                            '&data_type=fundings' % block['id']
                    # item['link_teammembers'] = 'https://e27.co/api/startups/get/?id=%s' \
                    #                            '&data_type=teammembers' % block['id']

                except Exception as ex:
                    print(ex)
                    continue

                else:
                    yield item