import scrapy
from properties.items import PropertiesItem
from scrapy.loader.processors import MapCompose, Join
import datetime
import socket
import urllib.parse
from scrapy.loader import ItemLoader

class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["web"]
    start_urls = (
        'https://www.amazon.in/Amazon-Brand-Solimo-Floral-Bedsheet/dp/B076ZYXQ4R/ref=sr_1_9?dchild=1&pf_rd_p=0a27ce14-93c0-4c59-a898-1c5df980ed3d&pf_rd_r=F9ZG943TVZV814P3ZR9Q&qid=1597306265&refinements=p_n_format_browse-bin%3A19560802031&s=kitchen&sr=1-9',
    )

    def parse(self, response):
    
        
    
        l = ItemLoader(item = PropertiesItem(), response=response)
            
       
        l.add_xpath('title', '//*[@id="productTitle"][1]/text()', MapCompose(unicode.strip, unicode.title))
        
        l.add_xpath('price', '//*[@id="priceblock_ourprice"][1]/text()',  MapCompose(lambda i: i.replace(',', ''), float), re='[.0-9]+')

        l.add_xpath('description','//*[@id="productDescription"]//p/text()', MapCompose(unicode.strip), Join())


        l.add_xpath('availability', '//*[@id="availability"]//span/text()', MapCompose(unicode.strip))

        l.add_xpath('image_urls', '//*[@id="imgTagWrapperId"][1]/@src', MapCompose(lambda i: urlparse.urljoin(response.url, i)))


        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        
        return l.load_item()

