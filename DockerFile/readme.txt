Dockerfile_v1: for doctalk4docker/doctalk_centos:v1
Dockerfile_v1.1: run doctalk4docker/doctalk_centos:v1 docker container,
Since codalab cannot download corenlp and nltk_data, they were downloaded manually
https://www.nltk.org/data.html
https://stanfordnlp.github.io/stanza/client_setup.html
How to download corenlp and nltk_data:
    1. go to src/doctalk/nlp.py and uncomment those lines:

	corenlp_dir = '/root/corenlp'
	stanza.install_corenlp(dir=corenlp_dir)
	import os
	os.environ["CORENLP_HOME"] = corenlp_dir

    2. go to src/doctalk/sim.py, and uncomment those lines:
    	
	from .down import ensure_nlk_downloads


    3. then go to src parent folder, run python src/eval.py dev-v1.1.json predictions.json
      then corenlp and nltk data will be downloaded to /root/corenlp and /root/nltk_data automatically 

How to download bert-large-uncased-whole-word-masking-finetuned-squad into local disk
	/root/squadModel
	wget https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad/resolve/main/config.json
	wget https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad/resolve/main/vocab.txt
	wget https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad/resolve/main/pytorch_model.bin

run doctalk4docker/doctalk_centos:v1 docker container on linux
tar and copy  /root/corenlp, /root/nltk_data, /root/squadModel into doctalk_centos:v1 docker container /root

update docker image based on doctalk_centos:v1 container, create v1.1 docker image

Dockerfile_corenlpnltkbert: for docker pull doctalk4docker/doctalk_centos:corenlpnltkbert, based on v1.1, add env
ENV CORENLP_HOME=/root/corenlp
ENV NLTK_DATA=/root/nltk_data
