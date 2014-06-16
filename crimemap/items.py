# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import persistent

class CrimemapItem(persistent.Persistent, Item):
    # define the fields for your item here like:
    description = Field()
    location = Field()
    
    geocode = None
    timestamp = None
