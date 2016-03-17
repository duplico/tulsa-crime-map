from ZODB import DB
from ZEO import ClientStorage
import ZODB.config
from BTrees.OOBTree import OOBTree
from datetime import datetime, timedelta
import transaction

import json, urllib2

from pygeocoder import Geocoder
from api_key import api_key

def normalize_timestamp(timestamp):
    final_date_pieces = []
    pieces = timestamp.split(' ')
    date_pieces = pieces[0].split('/')
    for piece in date_pieces:
        if len(piece) < 2:
            final_date_pieces.append('0%s' % piece)
        else:
            final_date_pieces.append(piece)

    time_pieces = pieces[1].split(':')
    for piece in time_pieces:
        if len(piece) < 2:
            final_date_pieces.append('0%s' % piece)
        else:
            final_date_pieces.append(piece)

    final_date_pieces.append(pieces[2]) # AM/PM

    final_date = "%s/%s/%s %s:%s:%s %s" % tuple(final_date_pieces)
    return final_date

def main():
    import logging
    logging.basicConfig()

    # Set up DB connection:
    storage = ZODB.config.databaseFromURL('zeoclient.config')
    connection = storage.open()
    dbroot = connection.root()
    if not dbroot.has_key('fires'):
        dbroot['fires'] = OOBTree()
    fire_db = dbroot['fires']

    geo = Geocoder(api_key=api_key)
    keys = set()

    # Load up our OpenTulsa data
    fire_calls = urllib2.urlopen("https://www.cityoftulsa.org/cot/opendata/tfd_dispatch.jsn")
    fire_calls = json.load(fire_calls)['Incidents']['Incident']
    time_format = "%m/%d/%Y %I:%M:%S %p"
    for call in fire_calls:
        k = (call['Address'], call['Problem'])
        timing = datetime.strptime(normalize_timestamp(call['ResponseDate']), time_format)
        if timing + timedelta(hours=1) < datetime.now():
            print "Aging off", k
            continue
        keys.add(k)
        if k in fire_db:
            print "Already exists."
            continue
        v = dict(
            location=call['Address'], 
            description=call['Problem'], 
            geocode=geo.geocode('%s, Tulsa, OK' % call['Address']).coordinates,
            timestamp=timing
        )
        print "Got a call:", k
        fire_db[k] = v

    # Delete stale entries:
    # TODO: Use ResponseDate
    del_keys = set()
    for k in fire_db:
        if k not in keys:
            del_keys.add(k)
    for k in del_keys:
        del fire_db[k]
    transaction.commit()
    connection.close()

if __name__ == "__main__":
    main()
