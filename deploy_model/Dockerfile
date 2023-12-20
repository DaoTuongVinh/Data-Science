#dockerfile
FROM pytorch/torchserve:latest
USER root
RUN chmod 777 -R .
COPY requirements.txt .          
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
#copy the .mar file created in previous step
COPY sbert.mar model-store/
#replace the existing config.properties with custom one
COPY config.properties config.properties
#start the server with model named SBERT
CMD ["torchserve", "--start" ,"--model-store", "model-store" ,"--models" ,"SBERT=sbert.mar"]