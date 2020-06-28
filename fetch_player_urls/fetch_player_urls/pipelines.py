# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FetchPlayerUrlsPipeline:

    def open_spider(self, spider):
        self.f = open('player_urls.txt', 'w')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        self.f.write(item['url'] + '\n')
        return item
