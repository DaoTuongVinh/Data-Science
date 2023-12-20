from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import json
import torch
from tqdm import tqdm
import numpy as np

job = [
    'QA-QC',
    'Solution Architect',
    'Data Architect',
    'product manager',
    'mobile developer',
    'project management',
    'AI Engineer',
    'full-stack developer',
    'embedded engineer',
    'Data Scientist',
    'ERP Engineer',
    'IT Lead',
    'product owner',
    'System Engineer',
    'game developer',
    'Data Engineer',
    'business analyst',
    'IT Consultant',
    'Designer',
    'front-end developer',
    'Tester',
    'System Admin',
    'DevOps Engineer',
    'Data Analyst',
    'back-end developer'
 ]



def evaluate(text_embeddings, label_embeddings, top_k):
    precision = 0
    recall = 0
    mrr = 0

    for text_embedding in text_embeddings:
        # Tính độ tương đồng cosine với tất cả nhãn
        similarities = [(label['label'], np.dot(label['label_embedding'], text_embedding['text_embedding']))
                        for label in label_embeddings]

        # Sắp xếp theo độ tương đồng giảm dần
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Lấy top_k nhãn
        top_k_labels = [label for label, _ in similarities[:top_k]]

        # Tính Precision, Recall và MRR
        if text_embedding['label'] in top_k_labels:
            precision += 1
            recall += 1 / len(text_embedding['label'])
            mrr += 1 / (top_k_labels.index(text_embedding['label']) + 1)

    precision /= len(text_embeddings)
    recall /= len(text_embeddings)
    mrr /= len(text_embeddings)

    return precision, recall, mrr



map_label = []
model = SentenceTransformer('all-MiniLM-L6-v2')
test_examples = []

data = json.load(open('/mnt/p3_translate/data_test.json', 'r'))

for k, v in data.items():
    for x in v:
        test_examples.append({
            'label': k,
            'text': x,
        })
    
count = 0    
for item in job:
    count += 1
    map_label.append({
        'id': count,
        'job': item,
        'embedding': model.encode(item),
    })



# Bước 3: Encode text trong data
text_embeddings = []
for example in test_examples:
    text_embedding = model.encode(example['text'])
    text_embeddings.append({
        'label': example['label'],
        'text_embedding': text_embedding
    })

# Bước 4: Encode labels
label_embeddings = []
for label in job:
    label_embedding = model.encode(label)
    label_embeddings.append({
        'label': label,
        'label_embedding': label_embedding
    })
    
    
results = {}
for top_k in top_k_list:
    precision, recall, mrr = evaluate(text_embeddings, label_embeddings, top_k)
    results[f"Precision@{top_k}"] = precision
    results[f"Recall@{top_k}"] = recall
    results[f"MRR@{top_k}"] = mrr
