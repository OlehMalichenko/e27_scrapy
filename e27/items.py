import scrapy


class E27Item(scrapy.Item):
    # first crowler
    link = scrapy.Field()
    link_general = scrapy.Field()
    # link_fundings = scrapy.Field()
    # link_teammembers = scrapy.Field()

    # second crowler
    name = scrapy.Field()
    profile_url = scrapy.Field()
    website = scrapy.Field()
    location = scrapy.Field()
    tags = scrapy.Field()
    founding_date = scrapy.Field()
    urls = scrapy.Field()
    emails = scrapy.Field()
    phones = scrapy.Field()
    short_description = scrapy.Field()
    description = scrapy.Field()
    founders = scrapy.Field()
    employee = scrapy.Field()