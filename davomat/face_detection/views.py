from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .forms import UpdateUserForm , AddUserForm
from django.http.response import StreamingHttpResponse
from dataset.test import extract_embeddings,train_model
from .camera import VideoCamera, Camera
import subprocess


def hello(request):
    return HttpResponse("Hello world!")

def index(request):
     return render(request, "index.html")

def users(request):
     
     users = User.objects.prefetch_related('imagemodel_set').all()

     context = {
          'users':users,
     }

     return render(request, "users.html",context)

def user(request, id):
    if request.method == 'POST':
          # id = request.user.id
          current_user = User.objects.get(id=id)
          form = UpdateUserForm(request.POST, instance=current_user)
          if form.is_valid():
               form.save()
          return redirect('/users')
    else:
          user = User.objects.prefetch_related('imagemodel_set').get(id=id)
          user_form = UpdateUserForm(request.POST or None, instance = user)

          context = {
               'user_form':user_form,
               'id': id
          }
          
          return render(request,'user.html',context)

def add_user(request):
     if request.method == 'POST':
          form = AddUserForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request,("New user successfully added!!!"))
               return redirect('/users')
     else:
          form = AddUserForm()
     return render(request,'add_user.html',{"form":form})

def gen(camera,username):
     k = 0
     while True:
          k=k+1
          frame = camera.get_frame(k,username)
          yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
          print("k=",k)
          if k > 100:
               break


def live(camera):
     while True:
          # frame,name,proba = camera.live_frame()
          frame = camera.live_frame()
          
          # yield name, proba
          yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request,username):
	return StreamingHttpResponse(gen(VideoCamera(),username),
					content_type='multipart/x-mixed-replace; boundary=frame')

def video(request):
     cam = live(Camera())
     # name, proba = next(cam)
     # print(name, proba)
     cam = StreamingHttpResponse(cam,
					content_type='multipart/x-mixed-replace; boundary=frame')
     return cam

	# return StreamingHttpResponse(live(Camera()),
	# 				content_type='multipart/x-mixed-replace; boundary=frame')

def open_live(request):
     return render(request, 'live-camera.html')


def restartmodel(request):
     
     extract_embeddings()
     train_model()

     return redirect('/users')