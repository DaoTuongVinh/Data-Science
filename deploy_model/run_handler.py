#from handler import SentenceTransformerHandler
from sentence_transformers import SentenceTransformer
import json
import zipfile
from json import JSONEncoder
import numpy as np
import os


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
    
    
class SentenceTransformerHandler(object):
    def __init__(self):
        super(SentenceTransformerHandler, self).__init__()
        self.initialized = False
        self.embedder = None
    def initialize(self, context):
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        
        try:
            with zipfile.ZipFile(model_dir + '/pytorch_model.bin',  'r') as zip_ref:
                zip_ref.extractall(model_dir)
        except:
            print('tried unzipping again')
        self.embedder = SentenceTransformer(model_dir)
        self.initialized = True
    def preprocess(self, data):
        
        inputs = data[0].get("data")
       
        if inputs is None:
            inputs = data[0].get("body")
        inputs = inputs.decode('utf-8')
        inputs = json.loads(inputs)
        sentences= inputs['queries']
        return sentences
    def inference(self, data):
        query_embeddings = self.embedder.encode(data)
        return query_embeddings
    def postprocess(self, data):
        return [json.dumps(data,cls=NumpyArrayEncoder)]




_service = SentenceTransformerHandler()
def handle(data, context):
    """
    Entry point for SentenceTransformerHandler handler
    """
    try:
        if not _service.initialized:
            _service.initialize(context)
            print('ENTERING INITIALIZATION')
        if data is None:
            return None
        data = _service.preprocess(data)
        data = _service.inference(data)
        data = _service.postprocess(data)
        return data
    except Exception as e:
        raise Exception("Unable to process input data. " + str(e))