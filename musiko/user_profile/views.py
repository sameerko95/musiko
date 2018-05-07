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
    dic= {}
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
                user1 = request.session['username']
                command = "SELECT id,first_name,last_name FROM user WHERE id = %s;"
                cursor = connection.cursor()
                cursor.execute(command, (user1))
                tup=cursor.fetchall()
                # for i in rows
                print(tup)
                dic = { "id": [ x[0] for x in  tup ], "first_name" : [x[1] for x in tup ] , "last_name" : [ x[2] for x in tup ] }
                print(dic)
                return render(request, "news/news_feed.html", {"dic":dic})   
            else:
                return render(request,"user_profile/login.html", {"message": "Invalid Login Credentials"})

        else:
            request.session['username'] = info['r_username']
            user = User.objects.create_user(info['r_username'], info['email'], info['r_password'])
            login(request, user)

            cursor = connection.cursor()
            command = "INSERT INTO user(id, first_name, last_name, password, birth_date) VALUES (%s, %s, %s, %s, %s);"

            response = cursor.execute(command, (info['r_username'], info['r_first_name'], info['r_last_name'],
                                     info['r_password'],info['birth_date']))
            
            connection.commit()
            
            profile_info = {"username": info['r_username'], "first_name": info['r_first_name'], "last_name": info['r_last_name'],"birth_date":info['birth_date']}
            return render(request, "user_profile/profile.html", profile_info)   

    return render(request,"user_profile/login.html", {})


def post_content(request):
    print("REQUEST.POST",request.POST)
    text = request.POST['post']
    cursor = connection.cursor()
    print(request.FILES)

    d = datetime.today()
    ts = time.time()
    t = d.strftime("%d%m%y%H%M%S")
    post_id = t
    comments_id = "c_"+post_id
    # firstname = request.session['firstname']
    # print("FIRST NAME",firstname)
    timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("IUSER",request.POST['username'])

    if 'media' in request.FILES:
        print(request.FILES)
        fil = request.FILES['media']
        fs = FileSystemStorage()
        tags_id = "t_"+post_id
        filename = fs.save('user_posts/'+request.POST['username']+"/"+t+fil.name, fil)
        attachment_id = post_id + filename
        
        uploaded_file_url = fs.url(filename)

        print(uploaded_file_url)

        command = "INSERT INTO posts VALUES(%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(command, (post_id, request.POST['username'], text, attachment_id, comments_id, tags_id, timestamp,))
        
        command = "INSERT INTO photos VALUES(%s, %s, %s, %s, %s, %s);"
        cursor.execute(command, (attachment_id, attachment_id, uploaded_file_url, request.POST['username'], tags_id,attachment_id,))

        connection.commit()
        ######fetching########
        user1 = request.POST['username']
        command = "SELECT first_name,last_name,birth_date FROM user WHERE id = %s;"
        cursor = connection.cursor()
        cursor.execute(command, (user1))
        tup=cursor.fetchall()
        # for i in rows
        print(tup)
        first_name = tup[0][0]
        last_name = tup[0][1]
        birth_date = str(tup[0][2]).replace('datetime.datetime','')
        str(birth_date).strip('(,),0,:') 
        # print(dic)
        print("FIRSTNAME------------------>",first_name)
        print("LASTNAME------------------>",last_name)
        print("BIRTHDATE------------------>",birth_date)
        return render(request,'user_profile/profile.html',{"first_name":first_name, "last_name": last_name, 
            "birth_date":birth_date,"upload_url": uploaded_file_url, "text": text , "username": request.POST['username']})
    else:
        command = "INSERT INTO posts VALUES(%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(command, (post_id, request.POST['username'], text, "null", "null", "null", timestamp,))
        connection.commit()
        return JsonResponse({"text": text})

    
    return JsonResponse({})

    # path = "media/user_posts/"+request.session['username']+"/"+"sample.jpg"
    # with open(path, 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
   
# def profile_view(request):
#     cursor = connection.cursor()
#     user = request.session['username']
#     command = "SELECT id,first_name,last_name FROM user WHERE id=user;"
#     cursor.execute(command, ())
#     tup=cursor.fetchall()
#     # for i in rows
    
#     dic = { "id": [ x[0] for x in tup ], "first name" : [x[1] for x in tup ] , "last name" : [ x[2] for x in tup ] }
#     print(dic)
#     return render(request,"user_profile/profile.html", {"dic":dic})
#     