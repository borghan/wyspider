# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WyspiderItem(scrapy.Item):
    fbid = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    detail = scrapy.Field()
    poc = scrapy.Field()
    patch = scrapy.Field()
    corp = scrapy.Field()
    author = scrapy.Field()
    submit_date = scrapy.Field()
    confirm_date = scrapy.Field()
    open_date = scrapy.Field()
    type = scrapy.Field()
    status = scrapy.Field()
    user_level = scrapy.Field()
    result_level = scrapy.Field()
    user_rank = scrapy.Field()
    result_rank = scrapy.Field()
    corp_reply = scrapy.Field()
    attention_num = scrapy.Field()
    collection_num = scrapy.Field()
    reply_num = scrapy.Field()
    is_lightning = scrapy.Field()
    dollar_num = scrapy.Field()





