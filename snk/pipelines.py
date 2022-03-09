import psycopg2

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
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
        self.store(item)
        return item

    def store(self, item):
        self.fund_name = item['fund_name']
        self.crisil_rank = str(item['crisil_rank'])
        self.level_1_category = item['level_1_category']
        self.level_2_category = item['level_2_category']
        self.level_3_category = item['level_3_category']

        self.cur.execute("""
            INSERT INTO mutual_funds (
                 fund_name, 
                 crisil_rank, 
                 level_1_category, 
                 level_2_category, 
                 level_3_category
            ) VALUES ( %s, %s, %s, %s, %s );
        """, (
            self.fund_name,
            self.crisil_rank,
            self.level_1_category,
            self.level_2_category,
            self.level_3_category
        )
        )
        self.conn.commit()
