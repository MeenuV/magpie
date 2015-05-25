import sys
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from spiders import multi_link_title_spider

def start_spider(urlToScrape):
    spider = multi_link_title_spider.MultiLinkTitleSpider(url=urlToScrape)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    reactor.run()