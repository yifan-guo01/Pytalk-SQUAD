import sys
import os
import json
import argparse
from doctalk.talk import Talker, nice_keys, exists_file, jload, jsave
from doctalk.params import talk_params, ropen, wopen
from doctalk.think import reason_with_File, reason_with_Text


def saveSQuAD_QuestionContent(datafile):
  os.makedirs('dev',exist_ok=True)
  dataset= jload( datafile)
  #data is []
  #print('data[0]:', dataset['data'][0])
  for article in dataset['data']:
      for i, paragraph in enumerate(article['paragraphs']):
         fname = "dev/" + article['title']  + "_" + str(i) + ".txt"
         conext = paragraph['context']
         with wopen(fname) as fcontext :
            fcontext.write(conext + "\n")
         fcontext.close()          
         questions = paragraph['qas']
         fqname = "dev/" + article['title']  + "_" + str(i) + "_quest.txt" 
         with wopen(fqname) as fquest:
           for question in questions:
             q=question['question']
             fquest.write(q + "\n")
           fquest.close()

def createSQuADQuestionIDMap(datafile):
  dataset= jload( datafile)
  #data is []
  #print('data[0]:', dataset['data'][0])
  qidMap = dict()
  for article in dataset['data']:
      for i, paragraph in enumerate(article['paragraphs']):    
         questions = paragraph['qas']
         for question in questions:
             qid = question['id']
             q=question['question']
             qidMap[qid] = article['title']  + "_" + str(i) + "_" + q
  output = json.dumps(qidMap)
  fname =  "qidMap.json"
  with wopen(fname) as f:
    f.write(output + "\n")
  f.close()
   
def create_SQuAD_Prediction_file(datafile):
  dataset= jload(datafile)
  qidans = dict()
  for article in dataset['data']:
    for p in article['paragraphs']:
      for qa in p['qas']:
        qid = qa['id']
        anslen = len(qa['answers'])
        if anslen > 0 :
          answer = qa['answers'][0]['text']
        else:
          answer = ''
        qidans[qid] = answer
  output = json.dumps(qidans)
  fname = "pred.json"
  with wopen(fname) as f:
    f.write(output + "\n")
  f.close()



def answerSQuADByName(filename):
  talkans, thinkans = reason_with_pytalk(filename)

def answerSQuADFromFile(datafile, prediction_pathfile):
  dataset= jload(datafile)
  #data is []
  qidThinkAnswerMap =dict() 
  for acount, article in enumerate(dataset['data']):
    for i, paragraph in enumerate(article['paragraphs']):
      fname = "dev/" + article['title']  + "_" + str(i)
      _, thinkans = reason_with_pytalk(fname)
      print('answerSQuAD:', thinkans )
      qids = []
      for qa in paragraph['qas']:
        qid = qa['id']
        qids.append(qid)
      print('qids length:', len(qids), ', detail:', qids)
      for j, qid in enumerate(qids):
        qidThinkAnswerMap[qid] = thinkans[j]
      if i == 0: break
    if acount ==0: break
  print('\nqidThinkAnswerMap:', qidThinkAnswerMap)
  outputThink = json.dumps(qidThinkAnswerMap)
  with wopen(prediction_pathfile) as fthink:
    fthink.write(outputThink + "\n")
  fthink.close()




def reason_with_pytalk_FromFile(fname) :  
  params = talk_params()
  params.with_answerer=True
  params.answers_by_rank = True
  params.to_prolog = 1 
  talkans, thinkans = reason_with_File(fname, params)
  return talkans, thinkans


  for article in dataset['data']:
      for i, paragraph in enumerate(article['paragraphs']):
         fname = "dev/" + article['title']  + "_" + str(i) + ".txt"
         conext = paragraph['context']
         with wopen(fname) as fcontext :
            fcontext.write(conext + "\n")
         fcontext.close()          
         questions = paragraph['qas']
         fqname = "dev/" + article['title']  + "_" + str(i) + "_quest.txt" 
         with wopen(fqname) as fquest:
           for question in questions:
             q=question['question']
             fquest.write(q + "\n")
           fquest.close()




def answerSQuADFromText(datafile, prediction_pathfile):
  dataset= jload(datafile)
  #data is []
  qidThinkAnswerMap =dict() 
  for count, article in enumerate(dataset['data']):
    for i, paragraph in enumerate(article['paragraphs']):
      conext = paragraph['context']
      qlist = []
      questions = paragraph['qas']
      for question in questions:
        q=question['question']
        qlist.append(q)
      _, thinkans = reason_with_pytalk_FromText(conext, qlist)
      #print('answerSQuAD:', thinkans )
      qids = []
      for qa in paragraph['qas']:
        qid = qa['id']
        qids.append(qid)
      #print('qids length:', len(qids), ', detail:', qids)
      for j, qid in enumerate(qids):
        qidThinkAnswerMap[qid] = thinkans[j]
    #if count==3: break
  #print('\nqidThinkAnswerMap:', qidThinkAnswerMap)
  outputThink = json.dumps(qidThinkAnswerMap)
  with wopen(prediction_pathfile) as fthink:
    fthink.write(outputThink + "\n")
  fthink.close() 


def reason_with_pytalk_FromText(text, qlist) :  
  params = talk_params()
  params.with_answerer=True
  params.answers_by_rank = True
  params.to_prolog = 1 
  talkans, thinkans = reason_with_Text(text, qlist, params)
  return talkans, thinkans



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='python src/eval.py <input-data-json-file> <output-prediction-json-path>')
    parser.add_argument('dataset_file', type=str, help='Dataset file')
    parser.add_argument('prediction_file', type=str, help='Prediction File')

    args = parser.parse_args()
    datafile = args.dataset_file
    prediction_pathfile = args.prediction_file
    print('datafile:', datafile)
    print('prediction_pathfile:', prediction_pathfile)
    '''
    saveSQuAD_QuestionContent(datafile )
    answerSQuAD(datafile, prediction_pathfile)
    '''
    answerSQuADFromText(datafile, prediction_pathfile)
    print('DONE')
 




