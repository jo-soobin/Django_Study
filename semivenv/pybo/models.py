from django.db import models

# Create your models here.
class review(models.Model):
    mvcode = models.TextField()     # 영화코드
    index = models.IntegerField()   # index
    review = models.TextField()     # 리뷰
    star = models.IntegerField()    # 별점
    emoji = models.CharField(max_length=20) # 이모티콘 긍정/부정
    img = models.TextField() # 이미지 서버 경로 
    create_date = models.DateTimeField()


class POST(models.Model):
    message = models.TextField(blank=True)
    # ex) WOW.png 파일을 업로드할 경우, 
    # instagram/post/20210901/WOW.png 경로에 저장되며
    # DB에는 "WOW.png" 문자열을 저장한다.
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y%m%d')   
    is_public = models.BooleanField(default=False, verbose_name='공개여부') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mvcode = models.TextField()     # 영화코드

    def __str__(self):
        # return f"Custom Post object ({self.id})"
        return self.message 