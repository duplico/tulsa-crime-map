# Scrapy settings for crimemap project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crimemap'

SPIDER_MODULES = ['crimemap.spiders']
NEWSPIDER_MODULE = 'crimemap.spiders'

ITEM_PIPELINES = {
    'crimemap.pipelines.CrimemapPipeline' : 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crimemap (+http://www.yourdomain.com)'
