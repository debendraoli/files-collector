# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import concurrent.futures
from boto3 import resource


class DBPipeline(object):
    data = {}
    cursor = None
    sqs_queue = None

    def open_spider(self, spider):
        spider.logger.info('Spider Opened')

        #  create database cursor
        self.cursor = spider.conn.cursor()

        sqs = resource('sqs')
        self.sqs_queue = sqs.get_queue_by_name(QueueName=spider.settings.get('AWS_SQS_NAME'))

    def process_item(self, item, _):

        data = {"files": {url for url in item.get('links')}, "content": item.get('body'), 'url': item.get('page_url')}
        if company_id := item.get('company_id') in self.data:
            self.data[company_id].append(data)
        else:
            self.data[company_id] = [data]

        return item

    def close_spider(self, spider):
        spider.logger.info('Spider Closed.')
        self.cursor.close()

        messages = []
        for company_id in self.data:
            for index, link in enumerate(self.data[company_id]['links']):
                messages.append({
                    'Id': f'{index}',
                    'MessageBody': link,
                    'MessageAttributes': {
                        'companyId': {
                            'StringValue': f'{company_id}',
                            'DataType': 'Number'
                        }}})
        # group message by 10 so that we can send 10 message in a single request
        grp_msgs = (messages[i:10 + i] for i in range(0, len(messages), 10))
        spider.logger.info('Sending messages to the queue.')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.map(lambda message: self.sqs_queue.send_messages(Entries=message), grp_msgs)
            spider.logger.info('Message sent.')

        # update last run
        self.cursor.executemany("UPDATE company SET last_run = NOW() WHERE id = %s;", self.data.keys())


        spider.logger.info('Fetching downloaded page urls from database.')
        query = 'INSERT INTO scraped_data(company_id, page_url, content) VALUES(%s, %s, %s)'
