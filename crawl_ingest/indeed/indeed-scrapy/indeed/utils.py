from bs4 import BeautifulSoup


def extract_requirements_from_data(item):
    requirements = []
    # Định nghĩa danh sách từ khóa yêu cầu
    requirement_keywords = ['requirement', 'skill', 'experience', 'điều kiện', 'kinh nghiệm', 'about you', 'yêu cầu bắt buộc']
    # Lấy nội dung HTML từ trường 'jobDescription'
    html_content = item.get('jobDescription', '')
    # Sử dụng BeautifulSoup để phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    # Tìm thẻ <b> và <p> chứa các từ khóa yêu cầu
    requirement_tags_b = [tag for tag in soup.find_all('b') if any(keyword.lower() in tag.get_text().lower() for keyword in requirement_keywords)]
    requirement_tags_p = [tag for tag in soup.find_all('p') if any(keyword.lower() in tag.get_text().lower() for keyword in requirement_keywords)]
    
    # Kết hợp danh sách requirement_tags_b và requirement_tags_p
    requirement_tags = requirement_tags_b + requirement_tags_p

    # Trích xuất nội dung từ mỗi thẻ chứa từ khóa yêu cầu và lưu vào mảng
    requirements = []
    for tag in requirement_tags:
        skills_li_tags = tag.find_next('ul').find_all('li', recursive=False) if tag.find_next('ul') else []
        requirements.extend([li_tag.get_text().strip() for li_tag in skills_li_tags])
    return requirements

def extract_salarys_from_data(item):
    salary_keywords = ['Lương', 'Salary',  'thu nhập']
    html_content = item.get('jobDescription', '')

    # Sử dụng BeautifulSoup để phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm thẻ <b> và <p> chứa các từ khóa mức lương
    salary_tags_b = [tag for tag in soup.find_all('b') if any(keyword.lower() in tag.get_text().lower() for keyword in salary_keywords)]
    salary_tags_p = [tag for tag in soup.find_all('p') if any(keyword.lower() in tag.get_text().lower() for keyword in salary_keywords)]

    # Kết hợp danh sách thẻ <b> và <p>
    salary_tags = salary_tags_b + salary_tags_p

    # Trích xuất nội dung từ mỗi thẻ chứa từ khóa mức lương và lưu vào mảng
    salaries = []
    for tag in salary_tags:
        #  Lấy nội dung của thẻ và thẻ con bên trong nó
        salary_content = tag.get_text().strip()
        # child_tags = tag.find_all()
        # child_content = ' '.join(child_tag.get_text().strip() for child_tag in child_tags)
        # if child_content:
        #     salary_content += ' ' + child_content
        #salaries.append(salary_content)
        next_sibling = tag.next_sibling
        if(next_sibling and hasattr(next_sibling, 'strip')):
            next_sibling_text = next_sibling.get_text().strip()
            if next_sibling_text:
                salaries.append(next_sibling_text)
            else: salaries.append(tag.get_text())

    return salaries

def extract_offers_from_data(item):
    offer_keywords = [ 'Đãi ngộ', 'offer', 'thỏa thuận', 'phúc lợi', 'chế độ', 'quyền lợi']
    html_content = item.get('jobDescription', '')
    
    # Sử dụng BeautifulSoup để phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Tìm thẻ <b> và <p> chứa các từ khóa mức lương
    offer_tags_b = [tag for tag in soup.find_all('b') if any(keyword.lower() in tag.get_text().lower() for keyword in offer_keywords)]
    offer_tags_p = [tag for tag in soup.find_all('p') if any(keyword.lower() in tag.get_text().lower() for keyword in offer_keywords)]
    
    # Kết hợp danh sách thẻ <b> và <p>
    offer_tags = offer_tags_b + offer_tags_p
    
    # Trích xuất nội dung từ mỗi thẻ chứa từ khóa mức lương và lưu vào mảng
    offers = []
    for tag in offer_tags:
      #  Lấy nội dung của thẻ và thẻ con bên trong nó
        offer_content = tag.get_text().strip()
        # child_tags = tag.find_all()
        # child_content = ' '.join(child_tag.get_text().strip() for child_tag in child_tags)
        # if child_content:
        #     salary_content += ' ' + child_content
        #salaries.append(salary_content)
        next_sibling = tag.next_sibling
        if(next_sibling and hasattr(next_sibling, 'strip')):
            next_sibling_text = next_sibling.get_text().strip()
            if next_sibling_text:
                offers.append(next_sibling_text)
            else: offers.append(tag.get_text())

    return offers

def extract_information(sample_data):
    combined_data = []
    # Extract data from sample_data
    requirement = extract_requirements_from_data(sample_data)
    salary = extract_salarys_from_data(sample_data)
    offer = extract_offers_from_data(sample_data)

    # Combine keywords into a dictionary
    combined_data = {
        "keyword": sample_data.get("keyword", ""),
        "location": sample_data.get("location", ""),
        "page": sample_data.get("page", 0),
        "position": sample_data.get("position", 0),
        "company": sample_data.get("company", ""),
        "jobkey": sample_data.get("jobkey", ""),
        "jobTitle": sample_data.get("jobTitle", ""),
        "requirement": requirement,
        "salary": salary,
        "offer": offer,
    }
    # for key, value in combined_data.items():
    #     print(f"{key}: {value}")
    return combined_data