from django.shortcuts import render
from . models import Room,Topic,Message
from  django.db.models import Q

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    
    topics=Topic.objects.all()
    rooms=Room.objects.filter(topic__name__icontains=q)
    room_messages=Message.objects.filter()
    context={'topics':topics,'rooms':rooms,'room_messages':room_messages}
    return render(request,'base/home.html',context)