from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .diyapi import NaverMovieCrawling
import pandas as pd
from .models import review

def index(request):
    
    MovieInfo = review.objects.all()
     
    context = {'question_list': MovieInfo}

    return render(request, 'pybo/main.html', context)


def index2(request):
    
    context = {'question_list': 'question_list'}

    return render(request, 'pybo/main2.html', context)


def reviewCrawling(request):
    
    NaverMovieCrawling.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main2.html', context)