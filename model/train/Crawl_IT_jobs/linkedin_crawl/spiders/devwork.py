import scrapy
import json
from tqdm import tqdm
import re
import time

class CareerBuilder(scrapy.Spider):
    name = 'devwork'
    start_urls = json.load(open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/devwork_link.json', 'r'))
    jobs = []
    
    def start_requests(self):
        for item in tqdm(self.start_urls):
            time.sleep(0.5)
            yield scrapy.Request(
                url=item, 
                callback=self.parse, 
            )

    def parse(self, response):
        job_infor = {}
        job_infor['link'] = response.url
        job_infor['more_infor'] = []
        job_infor['description'] = []
        block_title = response.css('.block-title')
        block_desc = response.css('.block-desc')
        

        for it1, it2 in zip(block_title[1:7], block_desc):
            job_infor['description'].append({
                'title': it1.css('::text').getall()[0].strip(),
                'descrip': [re.sub(r'\s+', ' ', itm.replace('\n', '').strip()) for itm in it2.css('::text').getall()],
            })
            
        more_infor = response.css('.widget')[1]
        
        for it1, it2 in zip(more_infor.css('strong::text').getall(), more_infor.css('span::text').getall()):
            job_infor['more_infor'].append({
                'type': it1,
                'descrip': it2,
            })
        
        yield job_infor

