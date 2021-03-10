import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import BksbankskItem
from itemloaders.processors import TakeFirst


class BksbankskSpider(scrapy.Spider):
	name = 'bksbanksk'
	start_urls = ['https://www.bksbank.sk/spravy-tlacove-informacie']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class, "news-item-btn")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="news-pagination"]/ul/li/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="content-large"]/h1/text()').get()
		description = response.xpath('//div[@class="portlet-boundary portlet-bordered portlet-journal-content"]//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="content-large"]/p/text()').get()

		item = ItemLoader(item=BksbankskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
