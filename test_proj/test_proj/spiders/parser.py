import scrapy
from test_proj.items import HorseRace,Participant
import re


class HorsRaceSpider(scrapy.Spider):
    name = 'works'
    start_urls = ['https://www.betbright.com/']

    def parse(self,response):
        item_lst = []
        for p in response.xpath(".//ul[@id = 'next-x-races']/li"):
            item = HorseRace()
            try:
                name=p.xpath("div/a/span/text()").extract()
                for n in name:
                    t = ':'.join(re.findall("\d+", n))
                    n = ' '.join(re.findall("[a-zA-Z]+",n))
                    item['track_name'] = n
                    item['race_start'] = t

                item['race_id'] = p.xpath("@data-event-id").extract()
                participant_lst = []
                for val in p.xpath("ul//li"):
                    participant = Participant()
                    name = list(map(str.strip,
                            val.xpath("div[@class='runner-details']/span[2]/text()").extract()))
                    participant['name'] = name
                    participant['participant_id'] = val.xpath("div[@class='silk after-silk']/text()").extract()
                    chances = val.xpath("div[4]/a[1]/text()").extract()
                    sp = val.xpath("div[4]/a[2]/text()").extract()
                    participant['chances'] = chances if chances else sp
                    participant_lst.append(participant)
                    item['participants'] = participant_lst
                item_lst.append(item)
            except Exception as esc:
                self.log('item filling exception %s ' % esc)
                continue
        return item_lst