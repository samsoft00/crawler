import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from shopping.spiders.femtechit_crawler import FemtechitCrawlerSpider
from shopping.spiders.konga_crawler import KongaCrawlerSpider
from shopping.spiders.jumia_crawler import JumiaCrawlerSpider

configure_logging()
runner = CrawlerRunner()

############## Runs multiple spiders simultaneously #############
runner.crawl(FemtechitCrawlerSpider)
runner.crawl(KongaCrawlerSpider)
runner.crawl(JumiaCrawlerSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
#################################################################

#Running the spiders sequentially by chaining the deferreds:
# @defer.inlineCallbacks
# def crawl():
# 	runner.crawl(FemtechitCrawlerSpider)
# 	runner.crawl(KongaCrawlerSpider)
# 	runner.crawl(JumiaCrawlerSpider)
# 	reactor.stop()

# crawl()
reactor.run() # the script will block here until the last crawl call is finished