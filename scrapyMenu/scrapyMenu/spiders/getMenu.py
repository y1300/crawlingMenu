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

    allowed_domains = ["pidginlondon.com"]
    start_urls = ["http://www.pidginlondon.com"]


    rules = (
        Rule(LxmlLinkExtractor(deny=('')), follow= True), # , restrict_xpaths=('//a[@class="button next"]',)
        Rule(LxmlLinkExtractor(allow=('menu')), callback="parse_items")
    )

    def parse_items(self, response):
        # hxs = HtmlXPathSelector(response)
        # titles = hxs.xpath('//span[@class="pl"]')

        sopa = BeautifulSoup(response.text, 'lxml')
        # logging.error(sopa)
        current_link = ''
        items = []
        for link in sopa.find_all('a'):
            current_link = link.get('href')        
            if current_link.endswith('pdf'):
                logging.error(current_link)
                item = ScrapymenuItem()
                item["title"] = self.allowed_domains
                item["link"] = current_link
                items.append(item)
                yield items


        
        # for titles in titles:
        #     item = ScrapymenuItem()
        #     item["title"] = titles.xpath("a/text()").extract()
        #     item["link"] = titles.xpath("a/@href").extract()
        #     items.append(item)

        return