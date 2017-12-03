# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderPracticeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleDetail(scrapy.Item):
    article_title = scrapy.Field()
    article_url = scrapy.Field()
    url_object_id = scrapy.Field()
    #content = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()