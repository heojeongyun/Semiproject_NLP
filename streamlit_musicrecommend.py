import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import streamlit as st
import keras as keras
from keras.models import load_model
from keras import backend as K
from keras_bert import get_custom_objects
from keras_radam import RAdam
from keras_bert import Tokenizer
import tensorflow
import transformers
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import tensorflow_addons as tfa #활성함수와 관련
from tensorflow.keras import layers, initializers, losses, optimizers, metrics, callbacks 
from transformers import TFBertModel # BertTokenizer 제외
import codecs
import sentencepiece as spm

# 한글 폰트 설정
plt.rcParams['font.family'] = "AppleGothic"
# Windows, 리눅스 사용자
# plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False
vocab_path = os.path.join('/root/project/bert/vocab.txt')
token_dict = {}

with codecs.open(vocab_path, 'r', 'utf8') as reader:
    for line in reader:
        token = line.strip()
        if "_" in token:
          token = token.replace("_","")
          token = "##" + token
        token_dict[token] = len(token_dict)

class inherit_Tokenizer(Tokenizer):
  def _tokenize(self, text):
        if not self._cased:
            text = text
            
            text = text.lower()
        spaced = ''
        for ch in text:
            if self._is_punctuation(ch) or self._is_cjk_character(ch):
                spaced += ' ' + ch + ' '
            elif self._is_space(ch):
                spaced += ' '
            elif ord(ch) == 0 or ord(ch) == 0xfffd or self._is_control(ch):
                continue
            else:
                spaced += ch
        tokens = []
        for word in spaced.strip().split():
            tokens += self._word_piece_tokenize(word)
        return tokens

tokenizer = inherit_Tokenizer(token_dict)

class MusicData:
    # def __init__(self, filepath, input_result):
    def __init__(self, input_result):
        self.df = pd.read_csv('/root/project/music_total_labeled_2.csv')
        self.input_result = input_result
        

    def find_lyrics(self,input_result):
        if self.input_result == '분노':
            print("분노에서 기쁨으로 변경")
            return self.df.loc["기쁨",:].reset_index(drop=True)
        else:
            print(self.df)
            return self.df.loc[input_result,:].reset_index(drop=True)
        
    
    def preprocess(self):
        df = self.df.set_index('emotion')
        self.df = df
        result = self.find_lyrics(self.input_result)
        return result 


class UserData:
    def __init__(self, todays_feeling):
        self.todays_feeling = todays_feeling
        custom_objects = get_custom_objects()
        custom_objects.update({'RAdam':RAdam})
        self.bert_model = load_model("/root/project/bert-sentence-model.h5",custom_objects=custom_objects)
    #입력 데이터 분류용


    #문장 분류해서 결과 내기
    def sentence_convert_data(self, data):
        global tokenizer
        #입력데이터 토큰화, 패딩 추가해서 seq_len=150에 맞게 변환함
        indices = [tokenizer.encode(data, max_len=150)]
        #numpy array로 변환하기
        indices = np.array(indices)
        indices = np.squeeze(indices)
        #segment는 다 0으로
        segments = np.zeros_like(indices)
        segments = np.squeeze(segments)
        return [indices, segments]

    def sentence_predict_save(self):
        data_x = self.sentence_convert_data(self.todays_feeling)
        predict = self.bert_model.predict(data_x)
        predict_answer = np.argmax(np.ravel(predict))
        #print(predict_answer)
        if predict_answer == 0:
            return "불안"
        elif predict_answer == 1:
            return "분노"
        elif predict_answer ==2:
            return "상처"
        elif predict_answer ==3:
            return "슬픔"
        elif predict_answer ==4:
            return "당황"
        elif predict_answer ==5:
            return "기쁨"
          
    def music_recommend():
        sentence = input("오늘의 기분을 한줄로 입력")
        output_val = howareyou(sentence)
        emotion = output_val.iloc[0]['emotion']
        print(f"감정:{emotion}")
        if emotion == '불안':
            return song_list_tot[song_list_tot['emotion'] == '불안']
        elif emotion == '분노':
            return song_list_tot[song_list_tot['emotion'] == '기쁨']
        elif emotion == '상처':
            return song_list_tot[song_list_tot['emotion'] == '상처']
        elif emotion == '슬픔':
            return song_list_tot[song_list_tot['emotion'] == '슬픔']
        elif emotion == '당황':
            return song_list_tot[song_list_tot['emotion'] == '기쁨']
        elif emotion == '기쁨':
            return song_list_tot[song_list_tot['emotion'] == '기쁨']
         



todays_feeling = st.text_input('오늘은 어떤 감정을 느꼈나요', placeholder='오늘의 감정은?')
# todays_feeling = "어서 동작해"
btn_clicked = st.button("음악 추천 받기")
if btn_clicked:
    user_data = UserData(todays_feeling)
    # output = MusicData(user_data)
    # output = read_musicdata(user_data)
    
    output = user_data.sentence_predict_save()
    print(1)
    if output:
        print(2)
        st.subheader(f"당신이 오늘 느낀 감정은 {(output)}")
        st.subheader("오늘의 기분에 맞는 음악을 추천해드릴게요 ↓ ↓")
        music_data = MusicData(output)
        output_data = music_data.preprocess()
        # print(int(output_data)
        print(type(output_data))
        st.dataframe(output_data.round(0), use_container_width=True)
    else:
        st.subheader('검색결과가 없습니다')