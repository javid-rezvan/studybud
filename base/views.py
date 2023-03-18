from django.shortcuts import render
from . models import Room,Topic,Message

def home(request):
    context={}
    return render(request,'base/home.html',context)