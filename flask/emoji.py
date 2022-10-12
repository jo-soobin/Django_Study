from flask import Flask, render_template, request

# 3. 리뷰 예측

# 모델 불러오기
import re
from konlpy.tag import Okt
import pickle
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model


app = Flask(__name__)

okt = Okt()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','을', '를','으로','자','에','와','한','하다'] # 불용어 정의

tokenizer = Tokenizer()

max_len = 30

loaded_model = load_model('best_model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

#model = Sequential()

emoticon_po = ["😍", "😘", "😙", "😃"] # 긍정적인 리뷰의 이모티콘 리스트
emoticon_ne = ["😐", "😥", "😭", "😤"] # 부정적인 리뷰의 이모티콘 리스트

# 감정 분류 및 이모티콘 랜덤 출력 함수

@app.route('/')
def index() :
    new_sentence = request.args.get('sentence', default = '긍정', type = str)
    print(new_sentence)
    
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    print(new_sentence)
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    print(encoded)
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    print(pad_new)
    score = float(loaded_model.predict(pad_new)) # 예측
    print(score)
    # 긍정, 부정 리뷰 분류
    result = '0'
    if(score > 0.5): # 긍정 리뷰
        result = '1'
    
    return {'emojiResult' : result}
    

if __name__=="__main__":
    #app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    app.run(host="127.0.0.1", port="5000", debug=True)
    #app.run(host='127.0.0.1', port=5000)

