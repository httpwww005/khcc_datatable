# -*- coding: utf-8 -*-
import sys
import scrapy
import urlparse
import re
import os
import datetime
from scrapy.utils.project import get_project_settings
import pytz
import time
from scrapy.exceptions import CloseSpider
from scrapy.signals import spider_closed

TZ=pytz.timezone("Asia/Taipei")


class VisitcountSpider(scrapy.Spider):
    name = "visitcount"
	
    allowed_domains = ["http://khvillages.khcc.gov.tw"]
    url_base = "http://khvillages.khcc.gov.tw/"

    def __init__(self):
        self.created_on = datetime.datetime.now(TZ)

	settings = get_project_settings()
        self.is_chromespider = settings.get("CHROME_SPIDER",False)
        self.close_count = 0
        self.block_it = False


        if self.is_chromespider:
            from selenium import webdriver
            chrome_bin_path = os.environ.get('CHROME_BIN', "")
            webdriver.ChromeOptions.binary_location = chrome_bin_path
            self.driver = webdriver.Chrome()
            entry_url = ["http://khvillages.khcc.gov.tw/home02.aspx?ID=$4002&IDK=2&EXEC=L&AP=$4002_SK3-115", "http://khvillages.khcc.gov.tw/home02.aspx?ID=$4012&IDK=2&EXEC=L"]
            for url in entry_url:
                self.driver.get(url)


    def url_generator(self):
        count = 1
    
        url_pat1 = 'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4001&IDK=2&AP=$4001_SK--1^$4001_SK2--1^$4001_PN-%d^$4001_HISTORY-0'
        url_pat2 = 'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4011&IDK=2&AP=$4011_SK-^$4011_SK2--1^$4011_PN-%d^$4011_HISTORY-0'
        #url_pat2 = 'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4011&IDK=2&AP=$4011_SK-^$4011_SK2--1^$4011_PN-%d^$4011_HISTORY-0',
        while self.close_count < 3:
            url = url_pat1 % int(count)
            yield url

            time.sleep(1)
            url = url_pat2 % int(count)
            yield url

            time.sleep(1)
            count += 1



    def start_requests(self):

	urls = [
            'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4001&IDK=2&AP=$4001_SK--1^$4001_SK2--1^$4001_PN-1^$4001_HISTORY-0',
	    'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4001&IDK=2&AP=$4001_SK--1^$4001_SK2--1^$4001_PN-2^$4001_HISTORY-0',
            'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4011&IDK=2&AP=$4011_SK-^$4011_SK2--1^$4011_PN-1^$4011_HISTORY-0',
            'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4011&IDK=2&AP=$4011_SK-^$4011_SK2--1^$4011_PN-2^$4011_HISTORY-0'
	]

        for url in urls:
        #for url in self.url_generator():
            if self.is_chromespider:
                yield scrapy.Request(url=url, callback=self.parse_url_chrome, dont_filter=True)
            else:
                yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)


    def parse_url_chrome(self, response):
        self.driver.get(response.url)

        ax = self.driver.find_elements_by_xpath("//a")

        hrefs = []
        for a in ax:
            href = a.get_attribute("href")
            if href:
                hrefs.append(href)

        hrefs = [url for url in hrefs if(("DATA=" in url) and ("_HISTORY-" in url))]

        if len(hrefs) > 0:
            for url in hrefs:
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        else:
            self.close_count += 1
            if( self.close_count > 2 ):
                raise CloseSpider('No more urls to crawl!')


    def parse_url(self, response):
        #filename = binascii.b2a_hex(os.urandom(8))
        #with open(filename, "w") as f:
        #    f.write(response.body)

        subject = response.xpath("//meta[@name='DC.Subject']/@content")[0].extract()
        self.logger.debug('subject: %s' % subject)

        if u"建物簡介" in subject:
            ax = response.xpath("//a")
            for a in ax:
                try:
                    href = a.xpath("./@href")[0].extract() or ""
                    text = a.xpath("./text()")[0].extract() or ""
                except:
                    pass

                if (("AP=$4011_HISTORY-0" in href) or ("AP=$4001_HISTORY-0" in href)) \
                and ((u"全民修屋" in text) or (u"建業新村" in text)):
                    url = urlparse.urljoin(self.url_base, href)
                    self.logger.debug('url: %s' % url)
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        location_1 = response.xpath("//meta[@name='DC.Title']/@content")[0].extract()

        if u"左營" in location_1:
            location = u"左營"
        else:
            location = u"鳳山"

        self.logger.debug('location: %s' % location)

        address_1 = response.xpath("//meta[@name='DC.Subject']/@content")[0].extract() 
        address = re.match(ur".*村(.*)$",address_1).group(1)
        self.logger.debug('address: %s' % address)

        count_1 = response.xpath("//span[@style='color:#a4a4a4']/text()")[0].extract()
        count = re.match(ur".*已有(.*)人瀏覽.*$",count_1).group(1)
        self.logger.debug('count: %s' % count)

        yield {'location':location,
                'address':address,
                'count':count,
                'created_on':self.created_on
                }

    def spider_closed(self, spider):
        pass
