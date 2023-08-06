import io
import PIL
import pickle
import requests
from sklearn.preprocessing import normalize
import os

from botnoi import getbow as gb
tfidfpath = os.path.join(os.path.dirname(gb.__file__),'botnoitfidf_v1.mod')

def extract_bowtfidf(textList):
  '''extract bow with tfidf vectors'''

  mod = pickle.load(open(tfidfpath,'rb'))
  feat = gb.sentencevector(textList,mod)
  feat = normalize(feat)
  return feat

from botnoi import getw2v as gw
w2vpath = os.path.join(os.path.dirname(gw.__file__),'botnoiw2v_small.mod')
def extract_w2vlight(textList):
  '''extract w2v vectors'''
  mod = pickle.load(open(w2vpath,'rb'))
  feat = gw.sentencevector(textList,mod)
  feat = normalize(feat)
  return feat

from botnoi import nlpcorrection as nc
sencor = os.path.join(os.path.dirname(nc.__file__),'botnoidict.p')
def getsentencescore(sentence):
  '''get sentence score'''
  mod = pickle.load(open(sencor,'rb'))
  res = nc.sentencescore(sentence,mod)
  return res


def printhello():
  print('hello')



