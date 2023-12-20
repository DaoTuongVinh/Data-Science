
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

location_list = ['https://devwork.vn/viec-lam?keyword=&province=1&country=vietnam&page=',
                 'https://devwork.vn/viec-lam?keyword=&province=79&country=vietnam&page=']


# QA-QC-in-ha-noi-kl4-page-2-en.html
class LinkedJobsSpider(scrapy.Spider):
    name = "devwork_link"
    count = 0
    api = 'https://jobsgo.vn/viec-lam-',
    list_link = []
    
    list_job = []
    def start_requests(self):
        for location in location_list:
            if '79' in location:
                yield scrapy.Request(
                    url=location + '1', 
                    callback=self.parse_job, 
                    meta={'first_job_on_page': 1}
                )
            else:
                for i in range(1, 6):
                    yield scrapy.Request(
                        url=location + str(i), 
                        callback=self.parse_job, 
                        meta={'first_job_on_page': 1}
                    )                           
        
        print(f"Length link: {len(self.list_link)}")
        json.dump(self.list_link, open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/devwork_link.json', 'w'), ensure_ascii=False)



    def parse_job(self, response):
        print(response.url)
        for item in response.css('.listing'):
            url_job = 'https://devwork.vn' + item.css('a::attr(href)').getall()[0]
            print(url_job)
            self.list_link.append(url_job)
        
        
        json.dump(self.list_link, open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/devwork_link.json', 'w'), ensure_ascii=False)



        
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