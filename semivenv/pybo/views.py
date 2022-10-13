from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .diyapi import NaverMovieCrawling, NaverMovieCrawling2
import pandas as pd
from .models import review
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('my')

@csrf_exempt
def index(request):
    if request.method == 'POST':
        page = request.POST.get('page', '1')
    else :
        page = request.GET.get('page', '1')

    MovieInfo = review.objects.all().order_by('viewIdx')
     
    paginator = Paginator(MovieInfo, 10)  # 페이지당 10개씩 보여주기

    page_obj = paginator.get_page(page)
    context = {'MovieInfo': page_obj}

    if request.method == 'POST':
        return render(request, 'pybo/paging.html', context)
    else :
        return render(request, 'pybo/main.html', context)

@csrf_exempt
def index2(request):
    logger.info("INFO 레벨로 출력")
    print('kjy test -------------'+request.method)
    if request.method == 'POST':
        page = request.POST.get('page', '1')
    else :
        page = request.GET.get('page', '1')

    MovieInfo = review.objects.all().order_by('viewIdx')
     
    paginator = Paginator(MovieInfo, 10)  # 페이지당 10개씩 보여주기

    page_obj = paginator.get_page(page)
    context = {'MovieInfo': page_obj}

    if request.method == 'POST':
        return render(request, 'pybo/paging.html', context)
    else :
        return render(request, 'pybo/main_kjy.html', context)
    


def reviewCrawling(request):
    
    NaverMovieCrawling.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main2.html', context)

def reviewCrawling2(request):
    
    NaverMovieCrawling2.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main.html', context)

