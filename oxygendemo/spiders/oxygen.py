# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest, Request
from pyquery import PyQuery as pq
from oxygendemo.items import OxygendemoItem


SOLD_OUT = 'Sold Out'
FEMALE = 'F'

COLORS = [
    'brown', 'burgundy', 'beige', 'cerulean', 'champagne', 'chocolate',
    'coffee', 'cream', 'coral', 'cyan', 'emerald', 'gold', 'gray',
    'gradient', 'grey', 'green', 'indigo', 'ivory', 'jade', 'lavender',
    'lemon', 'orange', 'pink', 'purple', 'red', 'rose', 'salmon', 'silver',
    'snake', 'violet', 'white', 'yellow', 'turquoise', 'smoking', 'olive'
    ]


APPARELS =  [
    'beachwear', 'bottom', 'cardigan', 'crew', 'denim', 'dress',
    'lingerie', 'outewear', 'top', 'skirt', 'sportwear','jacket',
    'short', 'pant', 'trouser', 'pantalon', 'coat', 'vest',
    'blouse', 'sweatshirt', 'jumper', 'sweater', 'tunic', 'bikini',
    'pyjamas', 'romper', 'pinni','pinny', 'shirt', 'jumpsuit',
    'corset', 'minidress', 'pool','biker', 'frilltop', 'hoody',
    'bralet', 'knicker', 'playsuit', 'culotte', 'tee', 'robe',
    'pini', 'bodysuit', 'blazer', 'slipper', 'pullover', 'pull'
    ]

SHOES = [
    'sneaker', 'boot', 'heel', 'brogue', 'flat', 'sandal', 'wedges',
    'mocassin', 'suede'
    ]

ACCESSORIZES = [
    'bracelet', 'tattoo', 'earrings', 'hats', 'case', 'necklace', 'ring',
    'collier', 'bangles', 'bangle', 'ear jacket', 'box', 'scents', 'candle'
    ]

ITEM_TYPES = {'A': APPARELS, 'S': SHOES, 'R': ACCESSORIZES}

CURRENCY_URL = "http://www.oxygenboutique.com/Currency.aspx"

CURRENCIES = {
    'usd_price': {'value':'503329C6-40CB-47E6-91D1-9F11AF63F706',
            'sign': u'\x24'},
    'eur_price': {'value': 'b2dd6e5d-5336-4195-b966-2c81d2b34897',
            'sign': u'\u20ac'},
    'gbp_price': {'value': 'b2dd6e5d-5336-4195-b966-2c81d2b34899',
            'sign': u'\xa3'}}



class OxygenSpider(CrawlSpider):
    name = "oxygenboutique.com"

    allowed_domains = ["oxygenboutique.com"]

    start_urls = [
        "http://www.oxygenboutique.com/Sale-In.aspx?S=1&ViewAll=1",
        "http://www.oxygenboutique.com/accessories-all.aspx",
        "http://www.oxygenboutique.com/Shoes-All.aspx",
        "http://www.oxygenboutique.com/clothing.aspx?ViewAll=1"
        ]

    rules = (Rule(LinkExtractor(restrict_xpaths=('//div[@class="itm"]//a')),
                                    callback='parse_item'),)


    def parse_item(self, resp):
        sel = pq(resp.body)

        currencies = CURRENCIES.keys()

        item = OxygendemoItem()
        item['designer'] = ''.join(sel.find('div.brand_name').text().split()[2:])
        item['gender'] = FEMALE
        item['link'] = resp.url
        item['code'] = resp.url.split('/')[-1][:-5]

        name = sel.find('h2').text()
        description = sel.find('meta[name="description"]').attr('content')

        item['type'] = None
        item['raw_color'] = None
        item['name'] = name
        item['description'] = description

        for item_type in ITEM_TYPES.keys():
            for subtype in ITEM_TYPES[item_type]:
                if subtype in name.lower():
                    item['type'] = item_type

        for color in COLORS:
            if color in description.lower():
                item['raw_color'] = color


        prices_info = sel.find('span.price.geo_16_darkbrown').text()
        currency = prices_info[0]
        prices = prices_info[1:].split()

        for curr in CURRENCIES.keys():
            for sign in CURRENCIES[curr]['sign']:
                if currency ==  sign:
                    currency = curr
                    break

        if len(prices) > 1:
            item[currency] = float(prices[1])
            if currency == 'usd_price':
                discount = float(prices[1])/(float(prices[0])/100)
                item['sale_discount'] =  round(discount, 2)
        else:
            item[currency] = float(prices[0])

        currencies.remove(currency)

        stock_statuses = [option.text for option in sel.find('option')[1:]]
        stock_dict = {}

        for status in stock_statuses:
            stock_dict[status.split()[0]] = 1 if SOLD_OUT in status else 3

        item['stock_status'] = stock_dict

        item['images'] = ([resp.urljoin(img.attr('href'))
                            for img in sel.find('a.cloud-zoom-gallery').items()])

        yield Request(
                CURRENCY_URL, callback=self.handle_currency_page,
                dont_filter=True,
                meta= {'item': item, 'currencies': currencies})



    def handle_currency_page(self, resp):
        yield FormRequest.from_response(
                resp, callback=self.handle_change_currency,
                formdata={
                    'ddlCurrency': CURRENCIES[resp.meta['currencies'][0]]['value'],
                    '__EVENTTARGET': 'lnkCurrency'},
                dont_filter=True,
                meta={
                    'item': resp.meta['item'],
                    'currencies': resp.meta['currencies']
                    })


    def handle_change_currency(self, resp):
        yield Request(
                url=resp.meta['item']['link'],
                callback=self.parse_extra_price,
                dont_filter = True,
                meta={
                    'item': resp.meta['item'],
                    'currencies': resp.meta['currencies']
                    })


    def parse_extra_price(self, resp):
        sel = pq(resp.body)
        item = resp.meta['item']
        currencies = resp.meta['currencies']

        prices_info = sel.find('span.price.geo_16_darkbrown').text()
        prices = prices_info[1:].split()
        currency = prices_info[0]

        for curr in CURRENCIES.keys():
            for sign in CURRENCIES[curr]['sign']:
                if currency ==  sign:
                    currency = curr
                    break

        if currency not in  currencies:
            yield Request(
                CURRENCY_URL, callback=self.handle_currency_page,
                dont_filter=True,
                meta={'item': item, 'currencies': currencies})

            return
        elif currency == currencies[0]:
            currencies.pop(0)
        else:
            currencies.pop(1)


        if len(prices) > 1:
            item[currency] = float(prices[1])
            if currency == 'usd_price':
                discount = float(prices[1])/(float(prices[0])/100)
                item['sale_discount'] =  round(discount, 2)
        else:
            item[currency] = float(prices[0])

        if not currencies:
            yield item
        else:
            yield Request(
                    CURRENCY_URL, callback=self.handle_currency_page,
                    dont_filter=True,
                    meta={'item': item, 'currencies': currencies})


