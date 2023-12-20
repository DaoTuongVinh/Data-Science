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
    name = 'itnavi'
    start_urls = [
        'https://itnavi.com.vn/job-detail/it-data-analytics-specialist', 
        'https://itnavi.com.vn/job-detail/data-engineer'
    ]
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
        job_infor['job_name'] = response.css('h3::text').getall()[0]

        if response.css('.job-requirements').get() == []:
            return None
        
        job_infor['infor'] = []
        
        try:
            job_infor['infor'].append({
                'type': 'Mô tả công việc',
                'descrip': [clean_and_format_text([itm]) for itm in response.css('.job-description')[0].css('.description::text').getall()]
            })
        except:
            None
        
        job_infor['infor'].append({
            'type':response.css('.job-requirements')[0].css('h2::text').get(),
            'descrip': [clean_and_format_text([itm]) for itm in response.css('.job-requirements')[0].css('.requirements::text').getall()]
        })
        
        yield job_infor

