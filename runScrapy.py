# import sys
import os
# from scrapyMenu import cmdline
from scrapy import cmdline
# import subprocess


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

# def intial():
#     os.chdir('scrapyMenu')
#     print(os.getcwd())
#     subprocess.call('scrapy crawl menu')

def run(url, id):
    # print(url,id)
    # os.chdir('scrapyMenu')
    # print(os.getcwd())
    # scrapy_crawl('menu')
    # subprocess.call('redis-cli lpush menu:start_urls http://google.com')
    cmd = "scrapy crawl menu -a url=%s -a id=%s" % (url,id)
    cmdline.execute(cmd.split())
    # os.chdir('..')
    print("finish Run Scrapy")

run("https://11brunswickst.co.uk/brasserie","123")
