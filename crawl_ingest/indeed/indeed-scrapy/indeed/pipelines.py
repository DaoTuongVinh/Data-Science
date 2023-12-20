# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo.mongo_client import MongoClient
import utils
class MongoDBPipeline:
    collection_name = 'indeed'
    ingest_collection_name = 'merged_collections'
    def open_spider(self,spider) :
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["jobs"]
        
    def close_spider(self,spider):
        self.client.close()
    def process_item(self, item, spider):
        processed_item = utils.extract_information(item)
        self.db[self.collection_name].insert(processed_item)
        self.db[self.ingest_collection_name].insert(self.process_for_ingest(item))
        return item
    def process_for_ingest(self,document):
        return  {
        'keyword': document.get('keyword', ''),
        'job_name': document.get('jobTitle', ''),
        'requirements': document.get('requirement', []),
        'salary': document.get('salary', []),
        'offer': document.get('offer', []),
        'location' : document.get('location', ''),
        'company' : document.get('company', ''),
        'from': 'indeed'
    }
    
class IndeedPipeline:
    def process_item(self, item, spider):
        return item
