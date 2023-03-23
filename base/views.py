from django.shortcuts import render,redirect
from . models import Room,Topic,Message,User
from  django.db.models import Q
from  .forms import RoomForm,UserForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


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
    topics=Topic.objects.all()
    form=RoomForm()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room=Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
            
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)
    
    
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.topic=topic
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')   
    context={'form':form,'room':room,'topics':topics}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context={'obj':room}
    return render(request,'base/delete.html',context)    

def loginPage(request):
    page='login'
    if request.method== 'POST':
        email=request.POST.get('username')
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
            user=authenticate(request,username=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'password is not correct')    
        except:
            messages.error(request,'user dose not exist')
            
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logouUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
        
    context={'form':form}
    return render(request,'base/login_register.html',context)

def topics(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    
    topics=Topic.objects.filter(Q(name__icontains =q))
    context={'topics':topics}
    return render(request,'base/topics.html',context)

def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.method=='POST':
        message.delete()
        return redirect('room',pk=message.room.id)
    context={'obj':message}
    return render(request,'base/delete.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    topics=Topic.objects.filter(room__host__username=user.username)
    rooms=Room.objects.filter(host__username=user.username)
    room_messages=Message.objects.filter(room__host__username=user.username)
    
    # rooms=user.room_set.all()
    # room_messages=user.message_set.all()
    # topics=Topic.objects.all()
    
    context={'topics':topics,'rooms':rooms,'room_messages':room_messages,'user':user}
    return render(request,'base/profile.html',context)


def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
       form=UserForm(request.POST,request.FILES,instance=user)
       if form.is_valid():
           form.save()
           return redirect('profile',pk=user.id)
        
    context={'form':form}
    return render(request,'base/edit-user.html',context)