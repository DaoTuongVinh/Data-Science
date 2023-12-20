from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import json
import torch

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
train_examples = []

data = json.load(open('/mnt/p3_translate/new_train.json', 'r'))


for item in data:
    train_examples.append(InputExample(texts=[item['query'], item['text']],
        label=float(item['label'])
    ))
    
    
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

model.fit(train_objectives=[(train_dataloader, train_loss)],
          epochs=5,
          evaluation_steps=50,
          warmup_steps=100,
          output_path='./Checkpoint/22k_sample_model_2')