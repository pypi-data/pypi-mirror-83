from konlpy.tag import Okt
from keras.models import load_model
import numpy as np 
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

class Oracle():
    def __init__(self):
        self.model = load_model('model.h5')
        self.twitter = Okt()
        self.stopwords = ['질문', '문의', '관련', '그대로', '계속', '답변', '선생님', '관련문의',
            '한지', '자주', '좀', '쪽', '자꾸', '요즘', '몇개', '무조건', '하나요',
            '안해','요', '경우', '최근', '및', '몇', '달', '일반', '전날', '저번',
            '말', '일어나지', '며칠', '먹기', '지난번', '글', '때문', '너', '무',
            '오늘', '시', '잔', '뒤', '지속', '막', '것', '이건', '뭔가', '다시', '그',
                '무슨', '안', '난', '도', '기', '후', '거리', '이', '뭘', '저', '뭐', '답젼',
                '평생', '회복', '반', '감사', '의사', '보험', '학생', '제발', '살짝',
                '느낌', '제', '대해','갑자기','문제', '전','정도', '왜', '거', '가요',
                '의심', '어제', '추천', '를', '지금', '무엇', '내일', '관해', '리', '세',
                 '로', '목적', '그냥', '거의', '고민', '다음', '이틀', '항상', '뭐', '때',
                '요', '가끔', '이후', '혹시', ]
        self.labeldic =  {0: '피부과',1: '외과',2: '호흡기내과',
                          3: '소화기내과',4: '안과',5: '신경과',
                          6: '이비인후과',7: '신경정신과',8: '혈액종양내과',
                          9: '류마티스내과',10: '재활의학과',11: '신경외과',
                          12: '마취통증의학과',13: '치과',14: '성형외과',
                          15: '흉부외과',16: '감염내과',17: '정형외과',
                          18: '응급의학과',19: '내분비내과',20: '순환기내과',
                          21: '한방과', 22: '산부인과',23: '비뇨기과',
                          24: '알레르기내과',25: '신장내과'}
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
    
    def set_stopwords(self, lst):
    	self.stopwords = lst

    def append_stopwords(self, lst):
    	for word in lst:
    		self.stopwords.append(word)
    		
    def preprocess(self, sentence):
    	nouns = self.twitter.nouns(sentence)
    	for word in nouns:
	        if word in self.stopwords:
	            while word in nouns:
	                nouns.remove(word)
    	return nouns

    def predict(self, sentence):
        payload = self.preprocess(sentence)
        payload_batch = []
        payload_batch.append(payload)

        pre_payload = self.tokenizer.texts_to_sequences(payload_batch)

        sequence_length = 10
        trunc_type = 'post'
        padding_type = 'post'
        padded_pre_payload = tf.keras.preprocessing.sequence.pad_sequences(
        pre_payload, 
        truncating=trunc_type, 
        padding=padding_type, 
        maxlen=sequence_length)
        result = self.model.predict(padded_pre_payload)
        sp = result.argmax()
        val = result.max()
        base = '{0}%확률로 {1}를 방문하셔야 합니다'
        return base.format(val*100, self.labeldic[sp])
