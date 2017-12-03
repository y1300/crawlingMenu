import sys
import os
from scrapyMenu import cmdline

# from twisted.internet import reactor
# from scrapy import log, signals
# from scrapy.crawler import Crawler as ScrapyCrawler
# from scrapy.settings import Settings
# from scrapy.xlib.pydispatch import dispatcher
# from scrapy.utils.project import get_project_settings
#
# def scrapy_crawl(name):
#     def stop_reactor():
#         reactor.stop()
#     dispatcher.connect(stop_reactor, signal=signals.spider_closed)
#     scrapy_settings = get_project_settings()
#     crawler = ScrapyCrawler(scrapy_settings)
#     crawler.configure()
#     spider = crawler.spiders.create(name)
#     crawler.crawl(spider)
#     crawler.start()
#     log.start()
#     reactor.run()

def run(url, id):
    print(url,id)
    os.chdir('scrapyMenu')
    # scrapy_crawl('menu')
    cmd = "scrapy crawl menu -a url=%s -a id=%s" % (url,id)
    cmdline.execute(cmd.split())
    os.chdir('..')
    print(os.getcwd())
