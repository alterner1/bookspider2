# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os
import time
class BookvoedPipeline:
    def __init__(self):
        self.connection = psycopg2.connect(os.getenv('CONNECTION_STRING'))
        cursor = self.connection.cursor()
        cursor.execute('select 1')
        test_result = cursor.fetchall()
        if test_result != [(1,)]:
            raise Exception('Error while initilizing DB connection')

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_data (
                id serial PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                author VARCHAR(255),
                price VARCHAR(255)             
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        time.sleep(1)
        if 'error' in item:
            print(f'Error item recieved, skip: {item}')
            return item
        
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO book_data (name, author, price) VALUES (%s, %s, %s)', [item['name'], item['author'], item['price']])
        self.connection.commit()

        return item
