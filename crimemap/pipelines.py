# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import ZODB, ZODB.FileStorage
from BTrees.OOBTree import OOBTree
from datetime import datetime
import transaction

from pygeocoder import Geocoder
from api_key import api_key

class CrimemapPipeline(object):
    def __init__(self, *args, **kwargs):
        pass

    def open_spider(self, spider):
        self.connection = ZODB.connection('crimemap.fs')
        self.dbroot = self.connection.root()
        if not self.dbroot.has_key('crimes'):
            self.dbroot['crimes'] = OOBTree()
        self.crime_db = self.dbroot['crimes']
        self.geo = Geocoder(api_key=api_key)
        self.keys = set()
        
    def close_spider(self, spider):
        del_keys = set()
        for k in self.crime_db:
            if k not in self.keys:
                del_keys.add(k)
        for k in del_keys:
            del self.crime_db[k]
        transaction.commit()
        self.connection.close()

    def process_item(self, item, spider):
        k = (item['location'], item['description'])
        self.keys.add(k)
        if k in self.crime_db:
            return item # CRIME STILL IN PROGRESS
        else:
            item.geocode = self.geo.geocode('%s, Tulsa, OK' % item['location']).coordinates
            item.timestamp = datetime.now()
            self.crime_db[k] = item
        # TODO: delete the stuff that doesn't exist anymore
        return item
