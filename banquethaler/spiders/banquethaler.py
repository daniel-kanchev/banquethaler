import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from banquethaler.items import Article


class BanquethalerSpider(scrapy.Spider):
    name = 'banquethaler'
    start_urls = ['http://www.banquethaler.ch/investment-letters']

    def parse(self, response):
        links = response.xpath('//a[@class="readmore"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = "".join(response.xpath('//h1//text()').getall())
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="datum"]/text()').get()
        if date:
            date = date.strip()
        else:
            return

        content = response.xpath('//article//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
