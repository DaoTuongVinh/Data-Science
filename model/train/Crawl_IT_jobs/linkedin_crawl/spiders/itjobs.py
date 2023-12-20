import scrapy
import json
from tqdm import tqdm
import re
import time
import string

def clean_and_format_text(texts, formatting_options=None):
    new_text = []
    
    for text in texts:
        # Mặc định các tùy chọn định dạng
        if formatting_options is None:
            formatting_options = {
                'replace_whitespace': True,
                'remove_special_chars': True,
                'lowercase': True,
                'strip_whitespace': True
            }

        # Xóa khoảng trắng nếu được yêu cầu
        if formatting_options['replace_whitespace']:
            text = re.sub(r'\s+', ' ', text)

        # Xóa ký tự đặc biệt nếu được yêu cầu
        if formatting_options['remove_special_chars']:
            text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)


        # Loại bỏ khoảng trắng ở đầu và cuối nếu được yêu cầu
        if formatting_options['strip_whitespace']:
            text = text.strip()
            
        # print(text)
        new_text.append(text)
        
    return new_text[0]



class CareerBuilder(scrapy.Spider):
    name = 'itjobs'
    start_urls = json.load(open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/itjobs_link.json', 'r'))
    jobs = []
    
    def start_requests(self):
        for item in tqdm(self.start_urls):
            time.sleep(0.01)
            yield scrapy.Request(
                url=item, 
                callback=self.parse, 
            )

    def parse(self, response):
        job_infor = {}
        job_infor['link'] = response.url
        job_infor['more_infor'] = []
        
        job_infor['description'] = []
        
        infor_head = response.css('.col-lg-9')[0].css('.col-lg-12')[1]
        for item in response.css('.col-lg-9')[0].css('.col-lg-12')[2:4]:
            if item.css('.jp_overview_wrapper')[0].css('ul li::text').getall() != []:
                job_infor['description'].append({
                    'type': item.css('h2::text').getall()[0],
                    'description': item.css('.jp_overview_wrapper')[0].css('ul li::text').getall(),
                })
            else:
                job_infor['description'].append({
                    'type': item.css('h2::text').getall()[0],
                    'description': item.css('.jp_overview_wrapper')[0].css('p::text').getall(),
                })
        
        for item in response.css('.col-lg-9')[0].css('.col-lg-12')[4:5]:
            job_infor['description'].append({
                'type': item.css('h2::text').getall()[0],
                'description': [clean_and_format_text([itm]) for itm in item.css('.jp_overview_content_wrapper')[0].css('ul li p::text').getall()]
            })
        
        for item in response.css('.col-lg-9')[0].css('.col-lg-12')[5:6]:
            job_infor['description'].append({
                'type': item.css('h2::text').getall()[0],
                'description': item.css('.jp_skills_slider_wrapper')[0].css('ul li::text').getall(),
            })
        
        job_infor['job_name'] = infor_head.css('h3::text').getall()[0]
        for itm in response.css('.col-lg-9')[0].css('.col-lg-12')[1].css('ul li span::text').getall():
            job_infor['more_infor'].append(itm.strip())
        
        yield job_infor

