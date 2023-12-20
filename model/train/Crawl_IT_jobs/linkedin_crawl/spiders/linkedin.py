
import scrapy
import json
from tqdm import tqdm
import time
import requests
from bs4 import BeautifulSoup


class TerminalFormatting:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m' 

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin"    
    list_job = []


    # def get_descriptions(self, url):
    #     text = BeautifulSoup(requests.get(url).text, 'html.parser')
    #     description = ''

    #     for item in text.find_all('div', attrs={'class': 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden'})[0] \
    #         .find_all(['p', 'ul', 'span']):
    #             if(item.name == 'p'):
    #                 description += (item.text + '\n')
    #             else:
    #                 for itm in item.find_all('li')[0]:
    #                     description + (item.text + '\n')
    #     return description
                
    def get_links(self, url):
        return url.replace('vn.linkedin.com', 'www.linkedin.com')
    
    def start_requests(self):
        list_link = json.load(open('/home/luungoc/BTL-2023.1/Data Science/linkedin_crawl/linkedin_link.json', 'r'))
        
        for link in tqdm(list_link):
            time.sleep(2)
            yield scrapy.Request(
                url=self.get_links(link), 
                callback=self.parse_job
            )

    def parse_job(self, response):
        job_item = {}
        
        print(TerminalFormatting.OKGREEN + '*********************************' + TerminalFormatting.ENDC)
        
        try:
            job_item['url'] =  response.css('meta[property="lnkd:url"]::attr(content)').getall()[0]
        except:
            job_item['url'] = None
        
        try:
            job_item['title'] =  response.css('meta[name="twitter:title"]::attr(content)').get(default=None)
        except:
            job_item['title'] = response.css('meta[property="og:title"]::attr(content)').get(default=None)
            
            
        try:
            job_item['job_name'] = response.css('h1::text').getall()[0]
        except:
            job_item['job_name'] = None
        

        item = response.css('li span::text').getall()
        job_item['job_detail'] = {
            'time': item[1].strip() if len(item) >=2 else None,
            'type': item[0].strip() if len(item) >=1 else None,
        }
        job_item['description'] = response.css('li::text').getall()
        
        self.list_job.append(job_item)
        print(f"Total current: {len(self.list_job)}")
             
        print(TerminalFormatting.OKGREEN + '***************Done!*************' + TerminalFormatting.ENDC)
        
        yield job_item
