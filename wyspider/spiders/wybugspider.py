# -*- coding=utf8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from wyspider.items import WyspiderItem
from scrapy.utils.project import get_project_settings
import re

SETTINGS = get_project_settings()


class WySpider(CrawlSpider):
    name = SETTINGS['SPIDER_NAME']
    allowed_domains = SETTINGS['ALLOWED_DOMAINS']
    start_urls = SETTINGS['START_URLS']
    keywords = SETTINGS['KEYWORDS']

    rules = [
        Rule(LinkExtractor(allow='/wooyun-\d{4}-\d+'), 'start'),
        Rule(LinkExtractor(allow='/page/\d+'), follow=True)
    ]

    def start(self, response):
        keywords = self.keywords
        if keywords:
            for word in keywords:
                if re.findall(word, response.body):
                    return self.parse_bug(response)
        else:
            return self.parse_bug(response)

    @classmethod
    def parse_bug(cls, response):
        item = WyspiderItem()
        item['fbid'] = response.xpath('(//div[@class="content"]/h3)[1]/a/text()').extract()
        item['title'] = response.xpath('//h3[@class="wybug_title"]/text()').extract()[0].split('\t')[2]
        item['description'] = None
        item['detail'] = None
        item['poc'] = None
        item['patch'] = None
        # 为提高抓取速度跳过对漏洞具体内容的爬取,如需要去掉注释即可
        # item['description'] = response.xpath('//p[@class="detail wybug_description"]/text()').extract()
        # item['detail'] = response.xpath('//div[@class="wybug_detail"]').extract()
        # item['poc'] = response.xpath('//div[@class="wybug_poc"]').extract()
        # item['patch'] = response.xpath('//div[@class="wybug_patch"]').extract()
        item['corp'] = response.xpath('//h3[@class="wybug_corp"]/a/@href').re(u'http://www.wooyun.org/corps/(.*)')
        item['author'] = response.xpath('//h3[@class="wybug_author"]/a/@href').re(u'http://www.wooyun.org/whitehats/(.*)')
        item['submit_date'] = response.xpath('//h3[@class="wybug_date"]/text()').extract()[0].split('\t')[2]
        item['open_date'] = response.xpath('//h3[@class="wybug_open_date"]/text()').extract()[0].split('\t')[2]
        item['type'] = response.xpath('//h3[@class="wybug_type"]/text()').extract()[0].split()[1:]
        item['status'] = response.xpath('//h3[@class="wybug_status"]/text()').extract()[0].split()[1]
        item['user_level'] = response.xpath('//h3[@class="wybug_level"]/text()').extract()[0].split()[1]
        item['result_level'] = response.xpath('//div[@class="bug_result"]').re(u'危害等级：(\w)')
        item['user_rank'] = response.xpath('//div[@class="content"]').re(u'自评Rank：\t\t(\d+)')
        item['result_rank'] = response.xpath('//div[@class="bug_result"]').re(u'漏洞Rank：(\d+)\ ')
        item['corp_reply'] = response.xpath('(//div[@class="bug_result"]/p)[4]/text()').extract()
        item['attention_num'] = response.xpath('//span[@id="attention_num"]/text()').extract()
        item['collection_num'] = response.xpath('//a[@id="collection_num"]/text()').extract()
        item['reply_num'] = response.xpath('count(//li[@class="reply clearfix"])').extract()
        item['confirm_date'] = '0000-00-00 00:00:00'
        item['is_lightning'] = '0'
        item['dollar_num'] = '0'

        # 判断是否有闪电和奖金数
        credit = response.xpath('//h3[@class="wybug_title"]/img/@src').re('/images/(\w+)\.png/?')
        if credit:
            for x in credit:
                if x == 'credit':
                    item['is_lightning'] = '1'
                if x[:1] == 'm':
                    item['dollar_num'] = x[-1]
        # 厂商确认/忽略漏洞的时间（直接传null给timestamp字段会生成CURRENT_TIMESTAMP）
        confirm_date = response.xpath('//div[@class="bug_result"]').re(u'[确认|忽略]时间：(\d{4}-\d{2}-\d{2}\ \d{2}:\d{2})')
        if confirm_date:
            item['confirm_date'] = confirm_date
        # 部分厂商没有乌云链接
        if bool(item['title'][0]) is False:
            item['title'] = response.xpath('//h3[@class="wybug_corp"]/a/text()').extract()
        # item全部统一为string类型
        for x in item:
            if bool(item[x]):
                item[x] = ''.join(item[x]).strip()
            else:
                item[x] = None

        yield item
