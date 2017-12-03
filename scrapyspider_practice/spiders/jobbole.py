# -*- coding: utf-8 -*-
import scrapy
from scrapyspider_practice.items import JobBoleArticleDetail
from urllib import parse
from scrapyspider_practice.utils.common import get_md5
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['python.jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        article_urls = response.xpath('//a[@class = "archive-title"]/@href').extract()
        img_urls = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a/img/@src').extract()
        while len(img_urls) < len(article_urls):
            img_urls.append("")
        for (article_url,img_url) in zip(article_urls,img_urls):
            try:
                yield scrapy.Request(parse.urljoin(response.url,article_url),meta={"img_url":img_url},callback = self.find_article)
            except Exception as e:
                pass
        next_page_url = response.xpath("//a[@class = 'next page-numbers']/@href").extract_first()
        if next_page_url:
            yield scrapy.Request(parse.urljoin(response.url,next_page_url),callback = self.parse)


    def find_article(self, response):
        article_items = JobBoleArticleDetail()

        front_img =response.meta.get("img_url")
        article_title = response.xpath('//div[@class = "entry-header"]/h1/text()').extract()[0]
        #content = response.xpath('//div[@class = "entry"]').extract()[0]

        article_items["article_title"] = article_title
        #article_items["content"] = content
        article_items["img_url"] = [front_img]
        article_items["article_url"] = response.url
        article_items["url_object_id"] = get_md5(response.url)

        yield article_items





