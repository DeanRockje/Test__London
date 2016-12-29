# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import CsvItemExporter

class CsvExportPipeline(object):

    def __init__(self):
        self.files = {}
        fields_to_export = ['track_name','race_id','time','name','participant_id','chances']


    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        file = open('%s_races.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file,fields_to_export=['race_id','track_name','race_start',
                                                               'name','participant_id','chances'])
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self,item,spider):
        for value in item['participants']:
            num_of_participants = len(item['participants'])
            counter = 0
            while counter < num_of_participants:
                   item['chances'] = value['chances']
                   item['participant_id'] = value['participant_id']
                   item['name'] = value['name']
                   counter+=1
            self.exporter.export_item(item)
        return item