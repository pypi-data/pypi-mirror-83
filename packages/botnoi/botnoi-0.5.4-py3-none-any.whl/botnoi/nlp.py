import io
import PIL
import pickle
import requests
from sklearn.preprocessing import normalize
import os

def extract_bowtfidf(textList):
  '''extract bow with tfidf vectors'''
  from botnoi import getbow as gb
  modpath = os.path.join(os.path.dirname(gb.__file__),'botnoitfidf_v1.mod')
  mod = pickle.load(open(modpath,'rb'))
  feat = gb.sentencevector(textList,mod)
  feat = normalize(feat)
  return feat

def extract_w2vlight(textList):
  '''extract w2v vectors'''
  from botnoi import getw2v as gw
  modpath = os.path.join(os.path.dirname(gw.__file__),'botnoiw2v_small.mod')
  mod = pickle.load(open(modpath,'rb'))
  feat = gw.sentencevector(textList,mod)
  feat = normalize(feat)
  return feat

def getsentencescore(sentence):
  '''get sentence score'''
  from botnoi import nlpcorrection as nc
  modpath = os.path.join(os.path.dirname(gw.__file__),'botnoidict.p')
  mod = pickle.load(open(modpath,'rb'))
  res = nc.sentencescore(sentence,mod)
  return res


def printhello():
  print('hello')



