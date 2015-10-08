# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
import logging

SETTINGS = get_project_settings()


class MySQLPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        # Instantiate DB
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host=SETTINGS['MYSQL_HOST'],
            user=SETTINGS['MYSQL_USER'],
            passwd=SETTINGS['MYSQL_PASSWD'],
            port=SETTINGS['MYSQL_PORT'],
            db=SETTINGS['MYSQL_DBNAME'],
            charset=SETTINGS['MYSQL_CHARSET'],
            use_unicode=True,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, conn, item):
        conn.execute(""" SELECT 1 FROM wybugs WHERE fbid=%s""", (item['fbid'], ))
        result = conn.fetchone()
        try:
            if result:
                conn.execute(
	                """ UPDATE wybugs SET title=%s, description=%s, detail=%s, poc=%s, patch=%s, corp=%s,
	                    author=%s, submit_date=%s, confirm_date=%s, open_date=%s, type=%s, status=%s,
	                    user_level=%s, result_level=%s, user_rank=%s, result_rank=%s, corp_reply=%s,
	                    attention_num=%s, collection_num=%s, reply_num=%s, is_lightning=%s, dollar_num=%s
	                    WHERE fbid=%s """,
                    (item['title'], item['description'], item['detail'], item['poc'], item['patch'], item['corp'],
                     item['author'], item['submit_date'], item['confirm_date'], item['open_date'], item['type'],
                     item['status'], item['user_level'], item['result_level'], item['user_rank'], item['result_rank'],
                     item['corp_reply'], item['attention_num'], item['collection_num'], item['reply_num'],
                     item['is_lightning'], item['dollar_num'], item['fbid'])
                )
                self.stats.inc_value('database/items_updated')
            else:
                conn.execute(
                """ INSERT INTO wybugs(fbid, title, description, detail, poc, patch, corp, author, submit_date,
	                confirm_date, open_date, type, status, user_level, result_level, user_rank, result_rank, corp_reply,
	                attention_num, collection_num, reply_num, is_lightning, dollar_num)
	                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                (item['fbid'], item['title'], item['description'], item['detail'], item['poc'], item['patch'], item['corp'],
                 item['author'], item['submit_date'], item['confirm_date'], item['open_date'], item['type'],
                 item['status'], item['user_level'], item['result_level'], item['user_rank'], item['result_rank'],
                 item['corp_reply'], item['attention_num'], item['collection_num'], item['reply_num'], item['is_lightning'], item['dollar_num'])
            )
                self.stats.inc_value('database/items_added')
        except:
            self.stats.inc_value('database/items_failed')
            logging.error(conn._last_executed)

    def _handle_error(self, e):
        logging.error(e)
