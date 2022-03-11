import re
import sys
import psycopg2
import scrapy
import hashlib

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from scrapy.mail import MailSender
from itemadapter import ItemAdapter


class SnkPipeline:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="snk",
            user="bhaven",
            password="")
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == 'funds':
            self.store_fund(item)
        if spider.name == 'greyipo':
            self.store_ipo(item)
        if spider.name == 'forex':
            self.store_forex(item)
        return item

    def store_fund(self, item):
        self.cur.execute("""
            INSERT INTO mutual_funds (
                 fund_name, 
                 crisil_rank, 
                 category, 
                 subcategory, 
                 type
            ) VALUES ( %s, %s, %s, %s, %s );
        """, (
            item['fund_name'],
            str(item['crisil_rank']),
            item['category'],
            item['subcategory'],
            item['type'])
        )
        self.conn.commit()

    def store_ipo(self, item):
        self.cur.execute("""
            INSERT INTO grey_ipo (
                 ipo_name, 
                 gmp_price, 
                 kostak_price, 
                 sauda_price
            ) VALUES ( %s, %s, %s, %s );
        """, (
            item['ipo_name'],
            item['gmp_price'],
            item['kostak_price'],
            item['sauda_price'])
        )
        self.conn.commit()

    def store_forex(self, item):
        self.cur.execute("""
            INSERT INTO forex (
                 cur_name, 
                 cur_code, 
                 cur_rate
            ) VALUES ( %s, %s, %s );
        """, (
            item['cur_name'],
            item['cur_code'],
            item['cur_rate'])
        )
        self.conn.commit()
