
import scrapy
import json
import re
from tqdm import tqdm



keyword_list = [
    'back-end-developer' , 
    'front-end-developer' , 
    'full-stack-developer' , 
    'mobile-developer' , 
    'game-developer' , 
    'embedded-engineer' , 
    'product-manager' , 
    'product-owner' , 
    'business-analyst', 
    'project-management' , 
    'IT-Lead' , 
    'IT-Consultant' , 
    'Designer' , 
    'Tester' , 
    'QA-QC' , 
    'System-Engineer' , 
    'System-Admin' , 
    'DevOps-Engineer' , 
    'Data-Engineer' , 
    'Data-Architect' , 
    'Data-Scientist' , 
    'Data-Analyst' , 
    'AI-Engineer' , 
    'ERP-Engineer' , 
    'Solution-Architect'
]

location_list = ['24', '1166']


# QA-QC-in-ha-noi-kl4-page-2-en.html
class LinkedJobsSpider(scrapy.Spider):
    name = "itjobs_link"
    count = 0
    api = 'https://www.itjobs.com.vn/vi/search?Text=',
    list_link = []
    
    list_job = []
    def start_requests(self):
        
        for type_job in tqdm(keyword_list):
            for location in location_list:
                api_url = 'https://www.itjobs.com.vn/vi/search?Text=' + str(type_job) + '&FunctionalLevelKey=&CityId=' + location
                first_job_on_page = 0
                url = api_url
                    

                yield scrapy.Request(
                    url=url, 
                    callback=self.parse_job, 
                    meta={'first_job_on_page': first_job_on_page}
                )
        
        
    def parse_job(self, response):
        # Thu thập thẻ a từ trang ban đầu
        for a_tag in response.css('.jp_job_post_link').css('a::attr(href)').getall():
            self.list_link.append('https://www.itjobs.com.vn' + a_tag)

        print(len(self.list_link))
        json.dump(self.list_link, open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/itjobs_link.json', 'w'), ensure_ascii=False)
        



def get_page_number(url):
    match = re.search(r'page-(\d+)', url)

    if match:
        return match.group(1)
    else:
        return None
    
def change_page_number(url, new_page_number):
    pattern = r'(page-\d+)'
    new_url = re.sub(pattern, f'page-{new_page_number}', url)

    return new_url