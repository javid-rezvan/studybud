from django.shortcuts import render
from . models import Room,Topic,Message

def home(request):
    topics=Topic.objects.all()
    rooms=Room.objects.all()
    room_messages=Message.objects.all()
    context={'topics':topics,'rooms':rooms,'room_messages':room_messages}
    return render(request,'base/home.html',context)