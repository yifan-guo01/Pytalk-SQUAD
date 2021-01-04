The code is run in codalab for SQuAD1.0 evaluation
1. The docker image is at: doctalk4docker/doctalk_centos:corenlpnltkbert, it is based on centos 7 + python 3.6
2. corenlp and nltk_data cannot be downloaded in codalab, they need to be downloaded manually.

run command :
  python src/eval.py dev-v1.1.json predictions.json 