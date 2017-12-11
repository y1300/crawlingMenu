from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapyMenu.items import ScrapymenuItem
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from urllib.parse import urljoin
# from scrapy_redis.spiders import RedisSpider

class MySpider(CrawlSpider):
    name = "menu"

    rules = (
        Rule(LxmlLinkExtractor(deny=('')), follow= True), # , restrict_xpaths=('//a[@class="button next"]',)
        Rule(LxmlLinkExtractor(allow=('menu')), callback="parse_items")
    )
    allowed_domains = ['']
    start_urls = ['']

    def __init__(self, url, id, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.url = url
        self.id = id
        self.allowed_domains = [url.split("//")[-1].split("/")[0]]
        self.start_urls = [url]

    def parse_items(self, response):

        sopa = BeautifulSoup(response.text, 'lxml')
        # logging.error(sopa)
        current_link = ''

        for link in sopa.find_all('a'):
            current_link = link.get('href')
            # logging.error(current_link)
            try:
                if current_link.endswith('pdf'):
                    current_link = urljoin(response.url, current_link)
                    logging.error(current_link)
                    item = ScrapymenuItem()
                    item["id"] = self.id
                    item["url"] = current_link
                    item["time"] = datetime.now().strftime('%Y-%m-%d')
                    yield item
            except:
                continue

        return
