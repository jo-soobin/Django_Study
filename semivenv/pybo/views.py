from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    context = {'question_list': 'question_list'}
    return render(request, 'pybo/main.html', context)