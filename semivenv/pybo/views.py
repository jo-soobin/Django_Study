from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .diyapi import NaverMovieCrawling, NaverMovieCrawling2
import pandas as pd
from .models import review
from django.core.paginator import Paginator

def index(request):
    
    MovieInfo = review.objects.all()
     
    context = {'MovieInfo': MovieInfo}

    return render(request, 'pybo/main.html', context)


def index2(request):
    page = request.GET.get('page', '1')
    MovieInfo = review.objects.all().order_by('viewIdx')
     
    paginator = Paginator(MovieInfo, 10)  # 페이지당 10개씩 보여주기
    
    page_obj = paginator.get_page(page)
    context = {'MovieInfo': page_obj}

    return render(request, 'pybo/main_kjy.html', context)


def reviewCrawling(request):
    
    NaverMovieCrawling.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main2.html', context)

def reviewCrawling2(request):
    
    NaverMovieCrawling2.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main2.html', context)

