from scrapy.spider import Spider
from scrapy.selector import Selector
from crimemap.items import CrimemapItem

class CrimeMapSpider(Spider):
    name = "crimemap"
    allowed_domains = ["www.tulsapolice.org",]
    start_urls = [
        "https://www.tulsapolice.org/live-calls-/police-calls-near-you.aspx",
    ]
    
    def parse(self, response):
        sel = Selector(response)
        descriptions = []
        places = []
        divisions = [
            "#ctl00_ctl00_ctl00_ContentPlaceHolderDefault_COTSectionTextpagePlaceHolder_ctl00_COT_LiveCallsInArea_9_grdDivision01",
            "#ctl00_ctl00_ctl00_ContentPlaceHolderDefault_COTSectionTextpagePlaceHolder_ctl00_COT_LiveCallsInArea_9_grdDivision02",
            "#ctl00_ctl00_ctl00_ContentPlaceHolderDefault_COTSectionTextpagePlaceHolder_ctl00_COT_LiveCallsInArea_9_grdDivision03"
        ]
        for d in divisions:
            entries = sel.css(d).xpath('tr/td/text()').extract()
            descriptions += map(str, entries[::2])
            places += map(str, entries[1::2])
        items = zip(descriptions, places)
        for item in items:
            yield CrimemapItem(description=item[0], location=item[1])