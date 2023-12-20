import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import streamlit as st
from langdetect import detect
import altair
import requests
from scipy import spatial

with open('DS_merged_data_deduplicated.json', 'r', encoding='utf8') as file:
    data = json.load(file)
# print(len(data))  

def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Unknown"
# text = "Design, prototype, and test the front-end and back-end of the product"
# language = detect_language(text)
# print("Ngôn ngữ của văn bản là:", language)
    
st.set_page_config(
    page_title="Nhóm 10",
    page_icon="👋",
)
app_mode_1 = st.sidebar.selectbox('Select Page',['Visual','Model'])

if app_mode_1 == 'Visual':
    app_mode_2 = st.sidebar.checkbox('Page')
    app_mode_3 = st.sidebar.checkbox('Location')
    app_mode_4 = st.sidebar.checkbox('Keyword')
    app_mode_5 = st.sidebar.checkbox('Language')
    app_mode_6 = st.sidebar.checkbox('Company')
    app_mode_7 = st.sidebar.checkbox('Requirements')
    st.title('Số tin tuyển dụng: ' + str(len(data)))
        
    if app_mode_2:
        # Đếm số tin tuyển dụng ở mỗi page
        page = []
        count_page = {}
        for i in range(len(data)):
            if data[i]['from'] not in page:
                page.append(data[i]['from'])
                count_page[data[i]['from']] = 1
            else:
                count_page[data[i]['from']] += 1
       
       # Visual
        st.header("Biểu đồ số tin tuyển dụng ở mỗi page")
        for pag in count_page.keys():
            st.write("{}: {}".format(pag, count_page[pag]))
        fig, ax = plt.subplots()
        labels = 'Indeed', 'Jobs365'
        ax.pie(pd.Series(count_page), labels=labels,autopct='%1.1f%%')
        ax.axis('equal')  
        st.pyplot(fig)
        
    if app_mode_3:
        # Đếm số tin tuyển dụng ở mỗi location và số tin tuyển dụng ở mỗi location của mỗi page
        location = []
        count_location = {}
        count_location_page = {}
        for i in range(len(data)):
            if data[i]['location'] not in location:
                location.append(data[i]['location'])
                count_location[data[i]['location']] = 1
                count_location_page[data[i]['location']] = {}
                count_location_page[data[i]['location']][data[i]['from']] = 1
            else:
                count_location[data[i]['location']] += 1
                if data[i]['from'] not in count_location_page[data[i]['location']].keys():
                    count_location_page[data[i]['location']][data[i]['from']] = 1
                else:
                    count_location_page[data[i]['location']][data[i]['from']] += 1
                
        # Visual
        st.header("Biểu đồ số tin tuyển dụng mỗi location")
        for loc in count_location.keys():
            st.write("{}: {}".format(loc, count_location[loc]))
        fig, ax = plt.subplots()
        labels = 'Ha Noi', 'Ho Chi Minh'
        ax.pie(pd.Series(count_location), labels=labels,autopct='%1.1f%%')
        ax.axis('equal')  
        st.pyplot(fig)
        st.header("Biểu đồ số tin tuyển dụng mỗi location của mỗi page")
        st.bar_chart(pd.DataFrame(count_location_page))
        
    if app_mode_4:
        # Đếm số tin tuyển dụng mỗi keyword
        keyword = []
        count_keyword = {}
        count_keyword_HN = {}
        count_keyword_HCM = {}
        for i in range(len(data)):
            if data[i]['keyword'] not in keyword:
                keyword.append(data[i]['keyword'])
                count_keyword[data[i]['keyword']] = 1
                if data[i]['location'] == 'Ha Noi':
                    count_keyword_HN[data[i]['keyword']] = 1
                    count_keyword_HCM[data[i]['keyword']] = 0
                elif data[i]['location'] == 'Ho Chi Minh':
                    count_keyword_HCM[data[i]['keyword']] = 1
                    count_keyword_HN[data[i]['keyword']] = 0
            else:
                count_keyword[data[i]['keyword']] += 1
                if data[i]['location'] == 'Ha Noi':
                    count_keyword_HN[data[i]['keyword']] += 1
                elif data[i]['location'] == 'Ho Chi Minh':
                    count_keyword_HCM[data[i]['keyword']] += 1
        count_keyword = dict(sorted(count_keyword.items(), key=lambda x: x[1], reverse = True))
        count_keyword_HN = dict(sorted(count_keyword_HN.items(), key=lambda x: x[1], reverse = True))
        count_keyword_HCM = dict(sorted(count_keyword_HCM.items(), key=lambda x: x[1], reverse = True))
        keyword = list(count_keyword.keys())
        keyword_HN = list(count_keyword_HN.keys())
        keyword_HCM = list(count_keyword_HCM.keys())
        
        # Visual
        st.header("Biểu đồ số tin tuyển dụng mỗi keyword")
        st.subheader("Số keyword sử dụng: " + str(len(keyword)))
        st.write("Top 5 keyword có số tin tuyển dụng nhiều nhất")
        for i in range(5):
            st.write("{}: {}".format(keyword[i], count_keyword[keyword[i]]))
        st.bar_chart(pd.Series(count_keyword).sort_values(ascending=False))
        
        st.header("Biểu đồ số tin tuyển dụng mỗi keyword tại Hà Nội")
        st.write("Top 5 keyword có số tin tuyển dụng nhiều nhất tại Hà Nội")
        for i in range(5):
            st.write("{}: {}".format(keyword_HN[i], count_keyword_HN[keyword_HN[i]]))
        st.bar_chart(pd.Series(count_keyword_HN).sort_values(ascending=False))
        
        st.header("Biểu đồ số tin tuyển dụng mỗi keyword tại Hồ Chí Minh")
        st.write("Top 5 keyword có số tin tuyển dụng nhiều nhất tại Hồ Chí Minh")
        for i in range(5):
            st.write("{}: {}".format(keyword_HCM[i], count_keyword_HCM[keyword_HCM[i]]))
        st.bar_chart(pd.Series(count_keyword_HCM).sort_values(ascending=False))
        
    if app_mode_5:
        # Đếm số tin tuyển dụng của mỗi ngôn ngữ 
        count_language = {'vi': 0, 'en': 0}
        for i in range(len(data)):
            for text in data[i]['requirements']:
                language = detect_language(text)
                if language == 'vi':
                    count_language['vi'] += 1
                else:
                    count_language['en'] += 1
                break

        # Visual
        st.header("Biểu đồ số tin tuyển dụng mỗi ngôn ngữ")
        st.subheader("Vietnamese: " + str(count_language['vi']))
        st.subheader("English: " + str(count_language['en']))
        fig, ax = plt.subplots()
        labels = 'Vietnamese', 'English'
        ax.pie(pd.Series(count_language), labels=labels,autopct='%1.1f%%')
        ax.axis('equal')  
        st.pyplot(fig)

    if app_mode_6:
        # Đếm số tin tuyển dụng của mỗi công ty 
        company = []
        count_company = {}
        count_company_location = {}
        for i in range(len(data)):
            if data[i]['company'] not in company:
                company.append(data[i]['company'])
                count_company[data[i]['company']] = 1
                count_company_location[data[i]['company']] = {}
                count_company_location[data[i]['company']][data[i]['location']] = 1
            else: 
                count_company[data[i]['company']] += 1
                if data[i]['location'] not in count_company_location[data[i]['company']].keys():
                    count_company_location[data[i]['company']][data[i]['location']] = 1
                else:
                    count_company_location[data[i]['company']][data[i]['location']] += 1
                    
        # Chọn ra top các công ty có nhiều tin tuyển dụng nhất
        count_company = dict(sorted(count_company.items(), key=lambda x: x[1], reverse = True))
        top_company = list(count_company.keys())[:10]
        count_top_company = {}
        for com in top_company:
            count_top_company[com] = count_company[com]
            
        # Đếm số công ty có tin tuyển dụng ở cả 2 location
        count_2location = {'company': [],
                           'Location': [],
                           'Value': []}
        cnt = 0
        for com in count_company_location.keys():
            if len(count_company_location[com]) > 1:
                cnt += 1
                for loc in count_company_location[com].keys():
                    count_2location['company'].append(com)
                    count_2location['Location'].append(loc)
                    count_2location['Value'].append(count_company_location[com][loc])
        # print(count_2location)
        
        # Visual
        st.header("Biểu đồ số tin tuyển dụng của top 10 công ty có nhiều tin tuyển dụng nhất")
        st.subheader("Số công ty đăng tin tuyển dụng: " + str(len(company)))
        for com in count_top_company.keys():
            st.write("{}: {}".format(com, count_top_company[com]))
        st.bar_chart(pd.Series(count_top_company))
        
        st.header("Biểu đồ số tin tuyển dụng của các công ty có tin tuyển dụng ở cả 2 location")
        st.subheader("Số công ty có tin tuyển dụng ở cả 2 location: " + str(cnt))
        bar_chart = altair.Chart(pd.DataFrame(count_2location)).mark_bar().encode(x=altair.X('company', sort="-y"), y='sum(Value)', color='Location', )
        st.altair_chart(bar_chart)
        
    if app_mode_7:
        # Đếm số requirement trong tin tuyển dụng của page jobs365
        requirements_jobs365 = []
        count_requirements_jobs365 = {}
        for i in range(len(data)):
            if(data[i]['from'] == 'jobs365'):
                for require in data[i]['requirements']:
                    if(require not in requirements_jobs365):
                        requirements_jobs365.append(require)
                        count_requirements_jobs365[require] = 1
                    else:
                        count_requirements_jobs365[require] += 1
        count_requirements = dict(sorted(count_requirements_jobs365.items(), key=lambda x: x[1], reverse = True))  
        # st.write(count_requirements)
        
        # Visual
        st.header("Biểu đồ số requirement trong tin tuyển dụng của page jobs365")
        st.subheader("Số requirements: " + str(len(requirements_jobs365)))
        for re in count_requirements.keys():
            st.write("{}: {}".format(re, count_requirements[re]))
        st.bar_chart(pd.Series(count_requirements))
        
if app_mode_1 == 'Model':
    # load text embedding
    sbert_api = "http://localhost:3000"
    # with open('DS_merged_data_deduplicated.json', 'r', encoding='utf8') as file:
    # data = json.load(file)
    text_ebd = json.load(open('../text_ebd.json','r',  encoding='utf8'))
    embeddings = {}
    for x in text_ebd:
        if x['label'] not in embeddings:
            embeddings[x['label']] = []
        embeddings[x['label']].append(x['embedding_label'])
    my_skill = st.text_input("Enter to skill:")
    st.write('My skill: '+ str(my_skill))
    mode_search = st.button('Search')
    response = requests.post(sbert_api + '/predictions/SBERT',data = {'data' : json.dumps({'queries' : [my_skill]})})
    result = {}       
    if response.status_code:
        my_skill_vector = response.json()[0]
        # calculate mean similarity score over labels
        
        for label in embeddings:
            similarity_scores = []
            for embed in embeddings[label]:
                similarity_scores.append(1- spatial.distance.cosine(my_skill_vector,embed))
            result[label] = np.mean(similarity_scores)
    result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1],reverse=True)}
    if mode_search:
        st.header('Top 5 công việc phù hợp: ')
        for job in list(result.keys())[:5]:
            st.subheader(job)
        # visualize
        st.header('Biểu đồ độ tương đồng: ')
        st.bar_chart(pd.Series(result).sort_values(ascending=False))
        
            
        