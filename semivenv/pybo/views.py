from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    

    '''
    수빈, 지예 개발

    '''

    context = {'question_list': 'question_list'}

    return render(request, 'pybo/main.html', context)