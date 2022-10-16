# ReviewTicon(리뷰티콘)
### Django 를 활용한 영화 리뷰 이모티콘 분류기 웹사이트

#### 사용한 기술:
- Crawling: Celenium, BeautifulSoup
- Data:Numpy, Pandas, Tensorflow, Konply
- Front-End: HTML, CSS, Javascript, Ajax, jQuery
- Back-End: Python3, Django, Apache2.4, mod_wsgi, Flask

#### How to use?
1. 관리자권한 명령 프롬프트 켜기
2. `httpd -k start` (Apache 서버 실행)
3. 새 명령 프롬프트 켜기
4. 사전에 만들어둔 가상환경 진입
5. emoji.py 가 저장된 위치로 이동하여 python emoji.py로 Flask 실행
6. `localhost/pybo` 접속
7. `localhost/pybo/crawling2` 새 Data 크롤링 페이지