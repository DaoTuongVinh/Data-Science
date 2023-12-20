from sentence_transformers import SentenceTransformer
import json
import numpy as np

def evaluate_model(model_name, data_path, label_list, top_k_list=[1, 3, 5, 10]):
    # Bước 1: Load model
    model = SentenceTransformer(model_name)

    # Bước 2: Load data
    data = json.load(open(data_path, 'r'))
    test_examples = []

    for k, v in data.items():
        for x in v:
            test_examples.append({
                'label': k,
                'text': x,
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
    for label in label_list:
        label_embedding = model.encode(label)
        label_embeddings.append({
            'label': label,
            'label_embedding': label_embedding
        })

    # Bước 5: Tính toán các chỉ số đánh giá
    results = {}
    for top_k in top_k_list:
        precision, recall, mrr = evaluate(text_embeddings, label_embeddings, top_k)
        results[f"Precision@{top_k}"] = precision
        results[f"Recall@{top_k}"] = recall
        results[f"MRR@{top_k}"] = mrr

    return results

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

# Example usage:
model_name = '/mnt/p3_translate/Checkpoint/22k_sample_model_2'
data_path = '/mnt/p3_translate/data_test.json'
label_list = [
    'QA-QC', 'Solution Architect', 'Data Architect', 'product manager', 'mobile developer', 'project management',
    'AI Engineer', 'full-stack developer', 'embedded engineer', 'Data Scientist', 'ERP Engineer', 'IT Lead',
    'product owner', 'System Engineer', 'game developer', 'Data Engineer', 'business analyst', 'IT Consultant',
    'Designer', 'front-end developer', 'Tester', 'System Admin', 'DevOps Engineer', 'Data Analyst',
    'back-end developer'
]

xx = []
results = evaluate_model(model_name, data_path, label_list, top_k_list=[1, 3, 5, 10])
for metric, value in results.items():
    print(f"{metric}: {value}")
    xx.append({
        metric: value
    })
    
json.dump(xx, open('/mnt/p3_translate/hh.json', 'w'), ensure_ascii=False)