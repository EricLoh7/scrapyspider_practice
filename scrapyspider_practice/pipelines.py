# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from  scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
from  twisted.enterprise import  adbapi
import MySQLdb.cursors

class ScrapyspiderPracticePipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件导出

    def __init__(self):
        self.file = codecs.open("article.json","w",encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.writelines(lines)
        return item
    def spider_closed(self):
        self.file.close()

class JsonExporterPipeline(object):
    #调用 scrapy 提供的 json exporter导出json文件
    def __init__(self):
        self.file = open("articleexporter.json","wb")
        self.exporter = JsonItemExporter(self.file,encoding="utf-8",ensure_ascii = False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class ArticleImagePipelines(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_path = value.get("path")
            item["img_path"] = image_path
            return item
class MysqlPipeline(object):
    #同步保存
    def __init__(self):
        self.conn =MySQLdb.connect('localhost','root','010771','article_spider',charset = 'utf8',use_unicode = True)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql = """
            insert into excel(title,url,url_object_id,img_url)
            VALUES (%s,%s,%s,%s)
"""
        self.cursor.execute(insert_sql,(item["article_title"],item["article_url"],item["url_object_id"],item["img_url"]))
        self.conn.commit()

class MysqlTwistedPipelines(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        '''#进入此pipelines自动执行，获取settings.py变量，此方法完成后在执行__init__'''
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor
        )

        #adbapi将mysql变为异步操作
        dbpoll = adbapi.ConnectionPool('MySQLdb',**dbparams)
        return cls(dbpoll) #cls其实就是MysqlTwistedPipelines，实例化之后执行__init__

    def process_item(self,item,spider):
        '''使用Twisted将mysql插入变为异步'''
        query = self.dbpool.runInteraction(self.do_insert,item) #第一个参数自定义
        #处理异常
        query.addErrback(self.handle_error) #自定义错误时候处理函数

    def do_insert(self,cursor,item):
        '''执行具体到插入数据库逻辑'''
        insert_sql = """
            insert into excel2(title,url,url_object_id,img_url)
            VALUES (%s,%s,%s,%s)
            """
        cursor.execute(insert_sql, (item["article_title"], item["article_url"], item["url_object_id"], item["img_url"]))

    def handle_error(self,failure):
        '''处理异步插入异常'''
        print(failure)

