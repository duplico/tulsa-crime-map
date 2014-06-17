from ZODB import DB
from ZEO import ClientStorage
import ZODB.config
from BTrees.OOBTree import OOBTree
from datetime import datetime
import transaction

import json, urllib2

from pygeocoder import Geocoder
from api_key import api_key

def main():
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
    time_format = "%-m/%-d/%Y %-I:%M:%S %p" # TODO: LAME!!! This doesn't work on Windows, supposedly.
    for call in fire_calls:
        k = (call['Address'], call['Problem'])
        print "Got a call:", k
        if k in fire_db:
            print "Already exists."
            continue
        v = dict(
            location=call['Address'], 
            description=call['Problem'], 
            geocode=geo.geocode('%s, Tulsa, OK' % call['Address']).coordinates,
            timestamp=datetime.strptime(call['ResponseDate'], time_format)
        )
        if v['timestamp'] + datetime.timedelta(hours=1) < datetime.now():
            continue # We only care about calls from the last hour, I think.
        print v
        fire_db[k] = v
        keys.add(k)

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
