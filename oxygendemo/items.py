# -*- coding: utf-8 -*-
import scrapy


class OxygendemoItem(scrapy.Item):
    code = scrapy.Field()
    description = scrapy.Field()
    designer = scrapy.Field()
    gender = scrapy.Field()
    images = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    usd_price = scrapy.Field()
    gbp_price = scrapy.Field()
    eur_price = scrapy.Field()
    raw_color = scrapy.Field()
    sale_discount = scrapy.Field()
    stock_status = scrapy.Field()
    type = scrapy.Field()

