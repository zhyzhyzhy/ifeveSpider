from scrapy.loader import ItemLoader
from ifeve.items import IfeveItem
import scrapy
import codecs
import sqlite3
import tomd
import html2text
import markdown2

class demoSpider(scrapy.Spider):
    name = "body"

    def start_requests(self):
        conn = sqlite3.connect('ifeve.db')
        cursor = conn.cursor()
        cursor.execute('select url from ifeve')
        urls = cursor.fetchall()
        cursor.close()
        conn.close()
        for url in urls:
            yield scrapy.Request(url = url[0], callback=self.parse)

    def parse(self, response):
        conn = sqlite3.connect('ifeve.db')
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('select * from ifeve where url = ?', (response.url,))
        items = cursor.fetchall()
    
        body = response.css("div.clearfix").css("div.post_content").extract_first().encode("utf-8")
        # body = tomd.Tomd(body).markdown
        body = html2text.html2text(body.decode("utf-8"))
        body = markdown2.markdown(body)
        for item in items:
            cursor.execute('update ifeve set body = ? where id = ?', (body, item[0]))
        conn.commit()
        cursor.close()
        conn.close()
            
