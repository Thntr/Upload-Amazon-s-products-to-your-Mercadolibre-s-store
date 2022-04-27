                 # -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WinkscraperItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    description = scrapy.Field()
    selledByAmazon = scrapy.Field()
    shippingDate = scrapy.Field()
    tittle = scrapy.Field()
    picture = scrapy.Field()
    availability = scrapy.Field()
    prime = scrapy.Field()
    pass

class CgWinkItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    description = scrapy.Field()
    selledByAmazon = scrapy.Field()
    shippingDate = scrapy.Field()
    tittle = scrapy.Field()
    picture = scrapy.Field()
    availability = scrapy.Field()
    pass

class AmalibreItem(scrapy.Item):
    # define the fields for your item here like:
    amazonLink = scrapy.Field()
    meliMegaCentral = scrapy.Field()

class NewLinksItem(scrapy.Item):
    # define the fields for your item here like:
    amazonLinks = scrapy.Field()

class PostTestSpider(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    description = scrapy.Field()
    selledByAmazon = scrapy.Field()
    shippingDate = scrapy.Field()
    tittle = scrapy.Field()
    picture = scrapy.Field()
    availability = scrapy.Field()
    prime = scrapy.Field()
    pass

    pass
