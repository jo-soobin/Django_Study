from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .diyapi import NaverMovieCrawling, NaverMovieCrawling2
import pandas as pd
from .models import review

def index(request):
    
    MovieInfo = review.objects.all()
     
    context = {'MovieInfo': MovieInfo}

    return render(request, 'pybo/main.html', context)


def index2(request):
    
    MovieInfo = review.objects.all()
     
    context = {'MovieInfo': MovieInfo}

    return render(request, 'pybo/main_kjy.html.html', context)


def reviewCrawling(request):
    
    NaverMovieCrawling.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main2.html', context)

def reviewCrawling2(request):
    
    NaverMovieCrawling2.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main2.html', context)

