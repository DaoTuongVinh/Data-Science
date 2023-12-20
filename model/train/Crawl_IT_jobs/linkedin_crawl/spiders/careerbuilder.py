import scrapy
import json
from tqdm import tqdm

class CareerBuilder(scrapy.Spider):
    name = 'description_careerbuilder'
    start_urls = json.load(open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/careerbuild_link.json', 'r'))
    jobs = []
    
    def start_requests(self):
        for item in tqdm(self.start_urls):
            yield scrapy.Request(
                url=item, 
                callback=self.parse, 
            )

    def parse(self, response):
        job_infor = {}
        job_infor['header'] = {}
        job_infor['header']['infor'] = []
        job_infor['header']['job_name'] = response.css('h1::text').get()
        detail_box = response.css('.detail-box ul li').getall()
        for idx in range(len(detail_box)):
            job_infor['header']['infor'].append({
                'type': response.css('.detail-box ul li')[idx].css('strong::text').get().strip(),
                'descrip': response.css('.detail-box ul li')[idx].css('p::text').get().replace('\r', ' ').replace('\n', ' ').strip()
            })

        description = response.css('.detail-row')

        job_infor['description'] = {}
        job_infor['description']['benefit'] = {}
        job_infor['description']['job_description'] = {}
        job_infor['description']['job_requirement'] = {}
        job_infor['description']['more_infor'] = {}
        
        job_infor['description']['benefit']['title'] = description[0].css('h2::text').get()
        job_infor['description']['benefit']['infor'] = description[0].css('ul li::text').getall()
        
        job_infor['description']['job_description']['title'] = description[1].css('h2::text').get()
        job_infor['description']['job_description']['infor'] = description[1].css('ul li::text').getall()
        
        job_infor['description']['job_requirement']['title'] = description[2].css('h2::text').get()
        job_infor['description']['job_requirement']['infor'] = description[2].css('ul li::text').getall()
        
        job_infor['description']['more_infor']['title'] = description[3].css('h3::text').get()
        job_infor['description']['more_infor']['infor'] = description[3].css('ul li::text').getall()
        
        if job_infor['description']['job_requirement']['infor'] == []:
            job_infor['description']['job_description']['title'] = description[1].css('h2::text').get()
            job_infor['description']['job_description']['infor'] = description[1].css('p::text').getall()
            
            job_infor['description']['job_requirement']['title'] = description[2].css('h2::text').get()
            job_infor['description']['job_requirement']['infor'] = description[2].css('p::text').getall()
            
            job_infor['description']['more_infor']['title'] = description[3].css('h3::text').get()
            job_infor['description']['more_infor']['infor'] = description[3].css('p::text').getall()
        
        
        self.jobs.append(job_infor)
        json.dump(self.jobs, open('/home/luungoc/BTL-2023.1/Data Science/Crawl_IT_jobs/careerbuild_link.json', 'w'), ensure_ascii=False)
        yield job_infor
