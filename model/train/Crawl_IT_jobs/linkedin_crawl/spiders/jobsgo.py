import scrapy
import json
from tqdm import tqdm
import re
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
    name = 'jobsgo'
    start_urls = json.load(open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/jobsgo_link.json', 'r'))
    jobs = []
    
    def start_requests(self):
        for item in tqdm(self.start_urls):
            yield scrapy.Request(
                url=item, 
                callback=self.parse, 
            )

    def parse(self, response):
        job_infor = {}
        
        job_infor['link'] = response.url
        job_infor['location'] = []
        job_infor['title_name'] = response.css('h1::text').getall()[0]
        job_infor['list_skill'] = []
        job_infor['description'] = []
        job_infor['requirement'] = []
        job_infor['benefit'] = []
        job_infor['more_infor'] = []
        
        for item in response.css('.col-sm-4')[2:7]:
            job_infor['more_infor'].append({
                'type': item.css('p::text').getall()[0].strip(),
                'descrip': item.css('p::text').getall()[1].strip(),
            })

        
        for item in response.css('.content-group')[2].css('a::text').getall():
            job_infor['list_skill'].append(item)
        
        
    
        if len(response.css('.content-group')[3].css('p::text').getall()) != 0: 
            for item in response.css('.content-group')[3].css('p::text').getall():
                job_infor['description'].append(item)
        elif len(response.css('.content-group')[3].css('ul li::text').getall()) != 0:
            for item in response.css('.content-group')[3].css('ul li::text').getall():
                job_infor['description'].append(item)
        else:
            for item in response.css('.content-group')[3].css('div::text').getall():
                if clean_and_format_text([item]) != '':
                    job_infor['description'].append(item)    
                    
               
        if len(response.css('.content-group')[4].css('p::text').getall()) != 0: 
            for item in response.css('.content-group')[4].css('p::text').getall():
                job_infor['requirement'].append(item)
        elif len(response.css('.content-group')[3].css('ul li::text').getall()) != 0:
            for item in response.css('.content-group')[4].css('ul li::text').getall():
                job_infor['requirement'].append(item)
        else:
            for item in response.css('.content-group')[4].css('div::text').getall():
                if clean_and_format_text([item]) != '':
                    job_infor['requirement'].append(item)   
        
        
        if len(response.css('.content-group')[5].css('p::text').getall()) != 0: 
            for item in response.css('.content-group')[5].css('p::text').getall():
                job_infor['benefit'].append(item)
        elif len(response.css('.content-group')[5].css('ul li::text').getall()) != 0:
            for item in response.css('.content-group')[5].css('ul li::text').getall():
                job_infor['benefit'].append(item)
        else:
            for item in response.css('.content-group')[5].css('div::text').getall():
                if clean_and_format_text([item]) != '':
                    job_infor['benefit'].append(item)   
            
            
        for item in response.css('.data')[0].css('small::text').getall():
            job_infor['location'].append(item)

            
        # print(response.css('.content-group').getall()[3])
        yield job_infor

