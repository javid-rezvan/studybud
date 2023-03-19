from django.shortcuts import render,redirect
from . models import Room,Topic,Message
from  django.db.models import Q
from  .forms import RoomForm

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.all()
    
    rooms=Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q) | Q(host__username__icontains=q))
    
    room_messages=Message.objects.filter(room__topic__name__icontains=q)
    context={'topics':topics,'rooms':rooms,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    # room_messages=Message.objects.filter(room__name=room)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            room=room,
            user=request.user,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
    
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    context={'form':form}
    return render(request,'base/room_form.html',context)
    
    
def updateRoom(request):
    context={}
    return render(request,'base/room_form.html',context)

def deleteRoom(request):
    context={}
    return render(request,'base/delete.html',context)    