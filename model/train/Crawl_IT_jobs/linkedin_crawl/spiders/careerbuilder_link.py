
import scrapy
import json
import time
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

location_list = ['ha-noi-kl4', 'ho-chi-minh-kl8']


# QA-QC-in-ha-noi-kl4-page-2-en.html
class LinkedJobsSpider(scrapy.Spider):
    name = "link_careerbuilder"
    count = 0
    api = 'https://careerbuilder.vn/jobs/',
    list_link = []
    
    list_job = []
    def start_requests(self):
        
        for type_job in tqdm(keyword_list):
            for location in location_list:
                for i in range(20):
                    api_url = 'https://careerbuilder.vn/jobs/' + str(type_job) + '-in-' + location + '-page-' + str(i) + '-en.html'
                    first_job_on_page = 0
                    url = api_url
                    
                    yield scrapy.Request(
                        url=url, 
                        callback=self.parse_job, 
                        meta={'first_job_on_page': first_job_on_page}
                    )
        
        print(f"Length link: {len(self.list_link)}")
        json.dump(self.list_link, open('/home/luungoc/BTL-2023.1/Data Science/linkedin_crawl/linkedin_crawl/spiders/vl.json', 'w'), ensure_ascii=False)



    def parse_job(self, response):
        print(response.url)
        # count_page = self.get_page_number(response.url)
        
        for item in response.css('.job_link'):
            self.list_link.append(item.css('::attr(href)').get())
            yield item.css('::attr(href)').get()
        
        
        json.dump(self.list_link, open('/home/luungoc/BTL-2023.1/Data Science/linkedin_crawl/linkedin_crawl/spiders/vl.json', 'w'), ensure_ascii=False)
        # count_page += 1



        
def get_page_number(url):
    # Sử dụng regex để tìm giá trị của tham số 'page'
    match = re.search(r'page-(\d+)', url)

    # Kiểm tra xem có phù hợp hay không và trả về giá trị
    if match:
        return match.group(1)
    else:
        return None
    
def change_page_number(url, new_page_number):
    # Sử dụng regex để tìm và thay thế giá trị của tham số 'page'
    pattern = r'(page-\d+)'
    new_url = re.sub(pattern, f'page-{new_page_number}', url)

    return new_url