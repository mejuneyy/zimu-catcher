# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZimucatcherPipeline(object):
    def process_item(self, item, spider):
        url = item['link']
        file_name = url.replace('/', '_').replace(':', '_')
        print("file_name: ", file_name)
        fp = open('result/' + file_name, 'wb')
        fp.write(item['body'])
        fp.close()
        return item
