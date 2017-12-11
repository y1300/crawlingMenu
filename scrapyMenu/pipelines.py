# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import CsvItemExporter
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob import PublicAccess
from scrapyMenu import settings
from urllib.request import urlretrieve
# import logging
import os

class ScrapymenuPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('pdfLinks.csv', 'a+b')
        self.exporter = CsvItemExporter(self.file, include_headers_line=False)
        self.exporter.fields_to_export = ['id', 'time', 'url']
        # logging.error('csv file downloading')
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ScrapyBlobPipeline(object):

    def __init__(self):
        self.block_blob_service = BlockBlobService(account_name=settings.BLOB_ACCOUNT, account_key=settings.BLOB_KEY)

    def process_item(self, item, spider):
        path = "%s/%s/%s" % (settings.LOCAL_STORE, item['id'], item['url'].split('/')[-1])
        # logging.error(settings.LOCAL_STORE)
        try:
            # logging.error(path)
            urlretrieve(item['url'], path)
            # pdf compression
            os.system('pdftrick "%s"' % path)
        except Exception as e:
            print(e)
            return None
        try:
            self.block_blob_service.create_container(item['id'], public_access=PublicAccess.Container)
        except Exception as e:
            print(e)

        self.block_blob_service.create_blob_from_path(
            item['id'],
            path.split('/')[-1],
            path,
            content_settings=ContentSettings(content_type='pdf')
                    )
        return item
