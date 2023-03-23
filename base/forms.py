from  django.forms import ModelForm
from . models import Room,User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        
        
class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['avatar','name','username','email','bio']
        
        
class myUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name','username','email','password1','password2']        
    
        
                