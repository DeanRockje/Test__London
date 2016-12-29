# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FlexibleItem(scrapy.Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(FlexibleItem, self).__setitem__(key, value)



class HorseRace(FlexibleItem):
    track_name = scrapy.Field()
    race_id = scrapy.Field()
    race_start = scrapy.Field()
    participants = scrapy.Field()


class Participant(scrapy.Item):
    name = scrapy.Field()
    participant_id = scrapy.Field()
    chances = scrapy.Field()