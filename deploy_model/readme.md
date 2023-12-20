
# 1. Install torch-model-archiver .
```sh
pip install torch-model-archiver
```
# 2.Create .mar file by running below command on terminal.
```sh
torch-model-archiver --model-name sbert --version 1.0 --serialized-file model/pytorch_model.bin --handler run_handler.py --extra-files "model/config.json,model/vocab.txt" --export-path .
```

# 3. Create a dockerfile packaging all the contents require to serve the model and start the server.

# 4. Build docker image
```sh
docker build -t ptserve-sbert:v1 dockerfile .
```

# 5. Run the container locally
```sh
docker run --rm -it -p 3000:8080 ptserve-sbert:v1
```


# References
https://yashna-shravani.medium.com/deploying-sbert-in-production-using-torchserve-cc1e438a90d