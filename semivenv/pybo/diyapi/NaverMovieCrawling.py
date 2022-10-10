
"""
# 네이버 영화
# 평점,리뷰 크롤링


필요한 라이브러리 import
pip install beautifulsoup4
pip install selenium
pip install chromedriver_autoinstaller
pip install lxml 
pip install requests
"""
from pybo.models import review as reviewModel
import pandas as pd

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from pathlib import Path

import re
import time
import urllib.request
import os
import shutil
from IPython.display import Image

import requests as req
from bs4 import BeautifulSoup as bs
from django.utils import timezone

# BeautifulSoup은 response.text를 통해 가져온 HTML 문서를 탐색해서 원하는 부분을 뽑아내는 역할 (컴퓨터가 이해할 수 있는 html 언어로 변경)

# 폴더 이름 특수문자 및 기호 제외
def clean_text(inputString):
    text_rmv = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·\b]', '', inputString)
    return text_rmv

# 폴더(디렉토리) 생성
def createDirectory(directory):
    print('directory : '+directory)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


# selenium 드라이버 가져와서 크롬 띄우기
def reviewCrawling() :

    print('~~~reviewCrawling start~~~')
    
    # 옵션 생성
    option = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    option.add_argument("headless")
    
    #import chromedriver_autoinstaller
    chrome_path = chromedriver_autoinstaller.install()
    if chrome_path is None or chrome_path == '' :
        chrome_path = 'C:\\venvs\\venvsemi\\lib\\site-packages\\chromedriver_autoinstaller\\105\\chromedriver.exe'

    print('chrome_path :'+chrome_path)
    driver = webdriver.Chrome(chrome_path, options=option)

    mvdf = pd.DataFrame(columns=['mvcode', 'index', 'imgpath'])
    df = pd.DataFrame(columns=['mvRank','mvcode', 'mvNm', 'index', 'review', 'star', 'emoji', 'img', 'create_date'])
    today = timezone.now()

    try:

        """
        # 이미지 크롤링
        """
        # 데이터 수집
        # 크롬으로 네이버 영화 홈페이지 접속(평점순)
        driver.get("https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=point")
        ele = driver.find_elements(By.CLASS_NAME, "thumb")

        # 각 영화 페이지, 제목 리스트 저장하기
        img_codes, img_titles = [], []
        for index in range(20):   
            tmp_code = ele[index].find_element(By.TAG_NAME,'a').get_attribute('href').split('=')[1]
            img_codes.append(tmp_code)
            
            tmp_title = ele[index].find_element(By.TAG_NAME, 'img').get_attribute('alt')
            img_titles.append(tmp_title)

        movie_cnt = 1
        imgcode = []
        for code, title in zip(img_codes, img_titles):
            img_type, img_cnt = [], []
            
            collect_cnt = 10 #default 사진 10장
            a_index = 0
            
            driver.get("https://movie.naver.com/movie/bi/mi/photoView.naver?code="+ code) # 포토 화면 
            try :
                next_btn = driver.find_elements(By.CSS_SELECTOR,'#photo_area > div > div.img_src._img_area > div > div > a.pic_next._photo_next._NoOutline')[0]
                
                #폴더 생성(이름:"movie+영화 순위")
                #directory_file_path = 'movie/img/img'
                #createDirectory(directory_file_path + str(movie_cnt)) 
                
                #사진 그룹(스틸컷 + 프로모션 + 포스터 )
                photo_group = driver.find_elements(By.CSS_SELECTOR, '#photoTypeGroup > li')
                photo_a = driver.find_elements(By.CSS_SELECTOR, '#photoTypeGroup > li > a')
                
                # 사진 그룹 각 요소 선택
                for i in photo_group:
                    img_type.append(i.get_attribute('imagetype'))        
                    img_cnt.append(int(i.find_element(By.CSS_SELECTOR,'a > em').text))
                    
                
                for t, c in zip(img_type, img_cnt):
                    photo_a[a_index].click()
                    time.sleep(0.1)
                            
                    if c > collect_cnt:
                        c = collect_cnt

                    for click_cnt in range(c):
                        img = driver.find_element(By.CSS_SELECTOR,'#photo_area > div > div.img_src._img_area > div > div > div > img')#이미지 영역
                        if click_cnt > 0 and next_btn != "": # 
                            next_btn.click()
                            time.sleep(0.3)                
                        # imgcode.append(f"{str(movie_cnt)}\t{str(click_cnt)}\t{img.get_attribute('src')}") # 번호/코드/제목/평점/리뷰 순서로 출력
                        tmp = pd.DataFrame({'mvcode':[movie_cnt], 'index':[click_cnt], 'imgpath':[img.get_attribute('src')]})
                        mvdf = pd.concat([mvdf, tmp])
                        # urllib.request.urlretrieve(img.get_attribute('src'), directory_file_path + str(movie_cnt) + "\\" + t + "_"+ str(click_cnt) + ".jpg")     

                    a_index += 1
                    
                movie_cnt += 1
            except :
                pass
        '''
        with open(txtfile_path+'/Movieimg.txt', 'w') as fp:
            for Line in imgcode:
                # write each item on a new line
                fp.write(Line + '\n')
        '''
        
        driver = webdriver.Chrome(chrome_path, options=option)
        # 크롬으로 네이버 영화 홈페이지 접속(평점순)
        driver.get("https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=point")
        ele = driver.find_elements(By.CLASS_NAME, "thumb")

        codes, titles = [], []
        for index in range(20): # 각 영화 페이지 링크(코드), 제목 리스트에 저장
            tmp_code = ele[index].find_element(By.TAG_NAME,'a').get_attribute('href').split('=')[1]
            codes.append(tmp_code)
            
            tmp_title = ele[index].find_element(By.TAG_NAME, 'img').get_attribute('alt')
            titles.append(tmp_title)

        count = 0 
        Data = []
        for code, title in zip(codes, titles):
            count += 1
            for i in range(1,6): # 1~6 페이지 리뷰 수집
                res = req.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=' + code + '&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=' + str(i))
                soup = bs(res.text, 'lxml')  # lxml은 구문을 분석하기 위한 파서(parser) # html 형식으로 변환
                viewer = soup.select('span.ico_viewer') # '관람객' 요소 선택
                for i in viewer:
                    i.extract() # '관람객' 요소 추출해서 삭제하기
                review = soup.select("div.score_result > ul > li") # '관람객' 요소가 삭제된 해당 요소 선택 후 추출

                emoji = '0' #이모티콘 import 해서 0 부정 1 긍정
                for idx, i in enumerate(review):
                    point = i.select_one('.star_score > em').text.strip() # 평점
                    ment = i.select_one('.score_reple span[id^=_filtered_ment_]').text.strip().replace('\t',"") # 리뷰 내용 개행(공백)문자 삭제
                    Data.append(f"{count}\t{code}\t{title}\t{point}\t{ment}") # 번호/코드/제목/평점/리뷰 순서로 출력
                    imgtmp = mvdf[mvdf['mvcode']==count]
                    if len(imgtmp) > 0 : 
                        imgtmp = imgtmp['imgpath'].sample(n=1).values[0]
                    else :
                        imgtmp = 'https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png'
                    tmp = pd.DataFrame({'mvRank':[count], 'mvcode':[code], 'mvNm':[title], 'index':[idx], 'review':[ment], 'star':[point], 'emoji':[emoji], 'img':[imgtmp], 'create_date':[today]})
                    df = pd.concat([df, tmp])


        # 총 영화 20개, 영화 한 편당 리뷰 50개씩 텍스트 파일로 저장(번호/코드/제목/평점/리뷰)
        '''
        txtfile_path = r'movie'
        
        if os.path.exists(txtfile_path):
            shutil.rmtree(txtfile_path)
        
        createDirectory(txtfile_path)

        
        with open(txtfile_path+'/MovieReview.txt', 'w') as fp:
            for Line in Data:
                # write each item on a new line
                fp.write(Line + '\n')
                
            print('---------------Done')
        '''

        

        driver.quit()
        
        for i in range(len(df)) :
            data = df.iloc[i]
            r = reviewModel(mvRank=data['mvRank'], mvcode=data['mvcode'], mvNm=data['mvNm'], index=data['index'], review=data['review'], star=data['star'], emoji=data['emoji'], img=data['img'], create_date=today)
            r.save()
        
    
    except Exception as ex:
        print('에러가 발생 했습니다', ex)
        driver.quit()