from django.urls import path

from . import views
#from .views2 import base_views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='main'), 
    path('test', views.index2, name='test'),
    path('crawling', views.reviewCrawling),
    path('crawling2', views.reviewCrawling2),
    
] 