from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapyMenu.items import ScrapymenuItem
from bs4 import BeautifulSoup
import logging

class MySpider(CrawlSpider):
    name = "menu"

    # allowed_domains = ["11brunswickst.co.uk"]
    # start_urls = ["https://11brunswickst.co.uk/brasserie"]

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
                    logging.error(current_link)
                    item = ScrapymenuItem()
                    item["title"] = self.id
                    item["link"] = current_link
                    yield item
            except:
                continue

        return
