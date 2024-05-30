from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .forms import UpdateUserForm , AddUserForm
from django.http.response import StreamingHttpResponse
from dataset.test import  model
from .camera import VideoCamera, Camera
from face_detection.models import ImageModel,AttendanceModel
from datetime import datetime, date



def hello(request):
    return HttpResponse("Hello world!")

def eda(request):
     import subprocess 

     #+++++++++++++++++++++++++++++++++++++++++++++++++

     #Filedan malumotlarni table ko'rinishiga o'tkazish

     import pandas as pd
     from pathlib import Path

     data = r'C:/Users/Pbl4/pbl4/davomat/dataset/origin_images'

     paths = [path.parts[-2:] for path in
          Path(data).rglob('*.*')]                             #writing purpose ('*.*') so that all image formats can be retrieved
     df = pd.DataFrame(data=paths, columns=['Class','Images'])     #create column names for dataframe
     df = df.sort_values('Class',ascending=True)                   #sort class name
     df.reset_index(drop=True, inplace=True)                       #sort index of each row

     #++++++++++++++++++++++++++++++++++++++++++++++++++

     #malumotlarni table da korsatish


     import os
     import pandas as pd

     class_counts = df['Class'].value_counts()
    
     output_html = 'image_dataset_statistics.html'
     filename = r'C:/Users/Pbl4/pbl4/davomat/templates/'+output_html

     if os.path.exists(filename):
          os.remove(filename)

     # Creating HTML content
     html_content = '''
     <h6>Count the number of image datasets</h6>
     <p>Image Count: {}</p>
     <p>Class Count: {}</p>

     <table class="table table-bordered mytable" style="width: 500px; margin: auto;">
     <thead>
          <tr>
          <th scope="col">#</th>
          <th scope="col">Class</th>
          <th scope="col">Image number</th>
          </tr>
     </thead>
     <tbody>
     '''.format(len(df.Images), len(class_counts))

     # Adding class counts to HTML content
     for i,( class_name, count) in enumerate(class_counts.items()):
          html_content += '''
               <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
               </tr>
          '''.format(i+1, class_name, count)


     # Closing HTML content
     html_content += '''

     </tbody>
     </table>
     '''

     # Writing HTML content to file
     with open(filename, 'w') as f:
          f.write(html_content)

     #+++++++++++++++++++++++++++++++++++++++++++++++++
          
     #statistika ustun

     import os
     import seaborn as sns
     from matplotlib import pyplot as plt

     filename = r'C:/Users/Pbl4/pbl4/davomat/static/eda_img/eda.png'

     # Check if the file exists and delete it if it does
     if os.path.exists(filename):
          os.remove(filename)

     # Create the plot
     fig, ax = plt.subplots(figsize=(15, 9))
     sns.countplot(data=df, x='Class', ax=ax)
     plt.title('Attendance dataset dagi har bir classning son grafigi')
     plt.xlabel('\n Image Class')
     plt.ylabel('Rasimlar soni')

     plt.savefig(filename, dpi=300, bbox_inches='tight')

     #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

     #modelda classning %zi

     import os
     import plotly.express as px
     import plotly.io as pio

     filename = r'C:/Users/Pbl4/pbl4/davomat/templates/fig.html'

     if os.path.exists(filename):
          os.remove(filename)

     class_counts = df['Class'].value_counts(sort=False)

     fig = px.pie(
          df,
          values=class_counts.values,
          names=class_counts.index,
          hole=0.5
     )

     fig.update_layout(
     title='Data Distribution of Padang Cuisine Image Dataset',
     font_size=15,
     title_x=0.45,
     annotations=[
          dict(
               text='Padang Cuisine Image Dataset',
               font_size=10,
               showarrow=False,
               height=1000,
               width=1000
          )
     ]
     )
     fig.update_traces(
     textfont_size=15,
     textinfo='percent'
     )
     pio.write_html(fig, filename, auto_open=False)

     #++++++++++++++++++++++++++++++++++++++++++++++++++++++++

     return render(request, "eda.html")

def index(request):
     today = datetime.today()

     users = AttendanceModel.objects.filter(date_came__year=today.year, date_came__month=today.month, date_came__day=today.day).select_related('user').all()
     context = {
          'users':users,
     }
     print(users)

     return render(request, 'index.html',context)

def users(request):
     
     users = User.objects.prefetch_related('imagemodel_set').order_by('username').all()

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

def attendance(request):
     today = datetime.today()


     with open(r"C:\Users\Pbl4\pbl4\davomat\static\userlist.txt", "r") as file:
          for line in file:
               
               parts = line.strip().split(",")
               
               if len(parts) == 2:
                    name, date = parts
                    print(name)
                    print(date)

                    date = AttendanceModel()
                    usr = User.objects.filter(username=name).first()
                    date.user=usr
                    date.date_came=date
                    date.save()
               else:
                    print("Invalid line format:", line)

     file.close()
     f = open(r'C:\Users\Pbl4\pbl4\davomat\static\userlist.txt', 'r+')
     f.truncate(0)

     users = AttendanceModel.objects.filter(date_came__year=today.year, date_came__month=today.month, date_came__day=today.day).select_related('user').all()
     context = {
          'users':users,
     }

     return render(request, 'index.html',context)

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

def uploadeimage(request,username):
     if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        for uploaded_file in uploaded_files:
            im = ImageModel()
            usr = User.objects.filter(username=username).first()
            im.user = usr
            im.image = uploaded_file
            im.save()
            print(uploaded_file,username)
        return redirect('/users')
     else:
        messages.error(request,("Not data!!!"))
        pass
     return redirect('/users')

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


import os

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def restartmodel(request):
     import subprocess # just to call an arbitrary command e.g. 'ls'

     # enter the directory like this:
     with cd("C:/Users/Pbl4/pbl4/davomat/dataset"):
     # we are in ~/Library
          subprocess.call("python test.py")


     return redirect('/users')