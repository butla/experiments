# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ForeignPrincipalItem(scrapy.Item):
    # LINK -> a href
    url = scrapy.Field()
    # COUNTRY_NAME
    country = scrapy.Field()
    # STATE
    state = scrapy.Field()
    # REG_NUMBER
    reg_num = scrapy.Field()
    # ADDRESS_1
    address = scrapy.Field()
    # FP_NAME
    foreign_principal = scrapy.Field()
    # FP_REG_DATE
    date = scrapy.Field()
    # REGISTRANT_NAME
    registrant = scrapy.Field()
    # DOCLINK (from view)
    exhibit_url = scrapy.Field()
