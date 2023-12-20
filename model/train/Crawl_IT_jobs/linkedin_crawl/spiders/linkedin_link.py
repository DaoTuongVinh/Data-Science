
import scrapy
import json
import time

keyword_list = [
    'back-end developer' , 
    'front-end developer' , 
    'full-stack developer' , 
    'mobile developer' , 
    'game developer' , 
    'embedded engineer' , 
    'product manager' , 
    'product owner' , 
    'business analyst', 
    'project management' , 
    'IT Lead' , 
    'IT Consultant' , 
    'Designer' , 
    'Tester' , 
    'QA-QC' , 
    'System Engineer' , 
    'System Admin' , 
    'DevOps Engineer' , 
    'Data Engineer' , 
    'Data Architect' , 
    'Data Scientist' , 
    'Data Analyst' , 
    'AI Engineer' , 
    'ERP Engineer' , 
    'Solution Architect'
]

location_list = ['Hà Nội', 'Ho Chi Minh']

        
class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    count = 0
    list_api = [
        'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=',
        '&location=',
        '&start=',
    ]
    
    list_job = []
    def start_requests(self):
        
        for type_job in keyword_list:
            for location in location_list:
                api_url = self.list_api[0] + type_job + self.list_api[1] + location + self.list_api[2]
                first_job_on_page = 0
                url = api_url + str(first_job_on_page)

                time.sleep(0.2)
                yield scrapy.Request(
                    url=url, 
                    callback=self.parse_job, 
                    meta={'first_job_on_page': first_job_on_page}
                )

    def check_link(self, url):
        start_index = url.find('start=')

        if start_index != -1:
            url_before_start = url[:start_index]
        return url_before_start + 'start='

    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']
        job_item = {}
        jobs = response.css("a::attr(href)").getall()

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(f"Đây là link: {response.url}")
        print(f"Tổng số jobs: {len(self.list_job)}")
        print('*********************************')
        count = 0
        for job in jobs:
            if '/jobs/view' in job:
                job_item['list_jobs_' + str(count)] = job
                self.list_job.append(job)
                count += 1
            yield job_item
        # yield jobs
        
    
        #### REQUEST NEXT PAGE OF JOBS HERE ######
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.check_link(response.url) + str(first_job_on_page)
            time.sleep(3) 
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})