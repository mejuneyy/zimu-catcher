import scrapy
from zimucatcher.items import ZimucatcherItem

class ZimuSpider(scrapy.spiders.Spider):
    name = "zimuzu"
    allowed_domains = ["zimuzu.tv"]
    start_urls = [
        "http://www.zimuzu.tv/subtitle"
    ]

    def parse(self, response):
        #pageHrefs = response.selector.xpath('//div[@class="pages"]/div/b/a/@href').extract()
        for s in range(8, 2189):
            href = "?page=%d&category=&format=&lang=&sort=" % (s)
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.sub_parse)
            yield request

    def sub_parse(self, response):
        hrefs = response.selector.xpath('//div[@class="box subtitle-list"]/ul/li/dl/dt/strong/a/@href').extract()
        for href in hrefs:
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        url = response.selector.xpath('//div[@class="subtitle-links tc"]/h3/a/@href').extract()[0]
        title = response.selector.xpath('//div[@class="subtitle-links tc"]/h3/a/text()').extract()[0]
        desc = response.selector.xpath('//div[@class="box subtitle-con"]/h2[@class="subtitle-tit"]/text()').extract()[0]
        item = ZimucatcherItem()
        item['title'] = title
        item['desc'] = desc
        print( "downloading: ", url)
        request = scrapy.Request(url, callback=self.parse_file, dont_filter = True)
        yield request

    @staticmethod
    def parse_file(response):
        body = response.body
        item = ZimucatcherItem()
        item['link'] = response.url
        item['body'] = body

        file_name = response.url.replace('/', '_').replace(':', '_')
        print("file_name: ", file_name)
        fp = open('result/' + file_name, 'wb')
        fp.write(item['body'])
        fp.close()
        return item