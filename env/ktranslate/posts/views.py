from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context ={
        'post' : 'sonhm'
    }

    return render(request,'posts/index.html',context)