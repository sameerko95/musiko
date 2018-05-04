from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import time
import pymysql

connection = pymysql.connect("localhost","root","root","musiko")
user = None
def signup(request):
    profile_info = {}
    
    if request.method=="POST":
        info = request.POST
        print(request.POST)
        if 'username' in request.POST:
            print("in login")

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                request.session['username'] = username
                login(request, user)
                profile_info = {"username": info['username']}
                return render(request, "user_profile/profile.html", profile_info)   
            else:
                return render(request,"user_profile/login.html", {"message": "Invalid Login Credentials"})

        else:
            
            user = User.objects.create_user(info['r_username'], info['email'], info['r_password'])
            login(request, user)

            cursor = connection.cursor()
            command = "INSERT INTO user(id, first_name, last_name, password) VALUES (%s, %s, %s, %s);"

            response = cursor.execute(command, (info['r_username'], info['r_first_name'], info['r_last_name'],
                                     info['r_password'],))
            
            connection.commit()
            
            profile_info = {"username": info['r_username'], "first_name": info['r_first_name'], "last_name": info['r_last_name']}
            return render(request, "user_profile/profile.html", profile_info)   

    return render(request,"user_profile/login.html", {})


def post_content(request):
    print(request.POST)
    text = request.POST['post']
    cursor = connection.cursor()
    print(request.FILES)

    d = datetime.today()
    ts = time.time()
    t = d.strftime("%d%m%y%H%M%S")
    post_id = t
    comments_id = "c_"+post_id
   
    timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    if 'media' in request.FILES:
        print(request.FILES)
        fil = request.FILES['media']
        fs = FileSystemStorage()
        tags_id = "t_"+post_id
        filename = fs.save('user_posts/'+request.session['username']+"/"+t+fil.name, fil)
        attachment_id = post_id + filename
        
        uploaded_file_url = fs.url(filename)

        print(uploaded_file_url)

        command = "INSERT INTO posts VALUES(%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(command, (post_id, request.session['username'], text, attachment_id, comments_id, tags_id, timestamp,))
        
        command = "INSERT INTO photos VALUES(%s, %s, %s, %s, %s, %s);"
        cursor.execute(command, (attachment_id, attachment_id, uploaded_file_url, request.session['username'], tags_id,attachment_id,))

        connection.commit()
        return JsonResponse({"upload_url": uploaded_file_url, "text": text})
    else:
        command = "INSERT INTO posts VALUES(%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(command, (post_id, request.session['username'], text, "null", "null", "null", timestamp,))
        connection.commit()
        return JsonResponse({"text": text})

    print(request.session['username'])

    return JsonResponse({})

    # path = "media/user_posts/"+request.session['username']+"/"+"sample.jpg"
    # with open(path, 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
   