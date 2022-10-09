from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from pybo.views2 import NaverMovieCrawling


def reviewCrawling2(request):
    
    NaverMovieCrawling.reviewCrawling()

    context = {'status': '성공'}

    return render(request, 'pybo/main2.html', context)