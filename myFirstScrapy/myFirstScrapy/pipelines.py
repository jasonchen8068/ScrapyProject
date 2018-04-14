# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  MySQLdb

class MyfirstscrapyPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='scrapydb', charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('truncate table movie')
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("insert into Movie (name,movieInfo,star,number,quote) \
            VALUES (%s,%s,%s,%s,%s)", (item['title'], item['movieInfo'], item['star'],
                                       item['number'], item['quote'])
            )
            self.conn.commit()
            # res = self.cursor.execute("select * from Movie order by id desc limit 1")
            # print res[0]

        except MySQLdb.Error:
            print 'insert error!'
        return item
