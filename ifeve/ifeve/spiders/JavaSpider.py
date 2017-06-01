from scrapy.loader import ItemLoader
from ifeve.items import IfeveItem
import scrapy
import json
import codecs
import sqlite3

class demoSpider(scrapy.Spider):
    name = "ifeve"

    def start_requests(self):
        conn = sqlite3.connect('ifeve.db')
        cursor = conn.cursor()
        cursor.execute('create table ifeve (id integer primary key autoincrement, title varchar(256), url varchar(256), category varchar(32), body text, fav integer)')
        cursor.close()
        conn.commit()
        conn.close()
        urls = ['http://ifeve.com/page/'+str(x)+'/' for x in range(1,100)]
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse)

    def parse(self, response):
        response = response.css("div.clearfix")[0].css("div#left_col")
        for item in response.css("div.post_wrap.clearfix"):
            post = item.css("div.post")
            url = post.css("h3.title").css("a::attr(href)").extract_first()
            title = post.css("h3.title").css("a::text").extract_first()
            categorys = post.css("div.post_meta.clearfix").css("ul.post-category.clearfix").css("li").css("a::text").extract()
            
            for category in categorys:
                conn = sqlite3.connect('ifeve.db')
                cursor = conn.cursor()
                ifeveItem = IfeveItem()
                ifeveItem['category'] = category
                ifeveItem['url']  = post.css("h3.title").css("a::attr(href)").extract_first()
                ifeveItem['title'] = post.css("h3.title").css("a::text").extract_first()
                cursor.execute('insert into ifeve (id, title, url, category, body, fav) values (?, ?, ?, ?, ?,?)', (None, ifeveItem['title'], ifeveItem['url'], ifeveItem['category'], "1","0"))
                cursor.close()
                conn.commit()
                conn.close()
                yield ifeveItem
            
