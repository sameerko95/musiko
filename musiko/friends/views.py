from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import time
import pymysql

people = []
friends = []
connection = pymysql.connect("localhost","root","root","musiko")

def view_friends(request):
    print(request.session['username'])
    # if request.session['username']!=None:
    cursor = connection.cursor()
    command = "SELECT id, first_name, last_name, address, birth_date, profile_pic FROM user WHERE id IN (SELECT user_2 FROM friends WHERE user_1=%s OR user_2=%s);" 
    cursor.execute(command, (request.session['username'], request.session['username'],))
    rows = cursor.fetchall()

    for row in rows:
        friend = {}
        row_list = list(row)

        for x in range(len(row_list)):
            if row_list[x]==None or row_list[x]==True or row_list[x]==False:
                    row_list[x] = str(row_list[x])
        friend['username'] = row_list[0]
        friend['first_name'] = row_list[1]
        friend['last_name'] = row_list[2]
        friend['address'] = row_list[3]
        if row_list[3]!="None":
            friend['birth_date'] = row_list[4].strftime("%Y/%m/%d")
        else:
            friend['birth_date'] = row_list[4]
        friend['profile_pic'] = row_list[5]
        friends.append(friend)

    command = "SELECT id, first_name, last_name, address, birth_date, profile_pic FROM user WHERE id IN (SELECT user_2 FROM friends);"
    cursor.execute(command, ())
    rows = cursor.fetchall()
    
    # print(rows)

    for row in rows:
        person = {}
        row_list = list(row)

        for x in range(len(row_list)):
            if row_list[x]==None or row_list[x]==True or row_list[x]==False:
                    row_list[x] = str(row_list[x])
        person['username'] = row_list[0]
        person['first_name'] = row_list[1]
        person['last_name'] = row_list[2]
        person['address'] = row_list[3]
        if row_list[3]!="None":
            person['birth_date'] = row_list[4].strftime("%Y/%m/%d")
        else:
            person['birth_date'] = row_list[4]
        person['profile_pic'] = row_list[5]
        people.append(person)

    print(friends)
    return render(request, "friends/friends_home.html", {"friends": friends,"people": people, "username": request.session['username']})
# else:
#     return render(request, "user_profile/login.html", {})


def add_friend(request):

    print(request.POST)
    info = request.POST
    if 'requestor_id' in info:
        cursor = connection.cursor()
        request_id = info["requestor_id"] +"-" +info["username"]
        command = "UPDATE requests SET status='accepted' WHERE user_id2=%s;"
        cursor.execute(command, (info['username'],))

        command = "INSERT INTO friends VALUES(%s, %s, %s);"
        rel_id = request_id
        cursor.execute(command, (rel_id, info['username'], info['requestor_id'],))

        connection.commit()
        return JsonResponse({"message": "Success"})
    else:
        cursor = connection.cursor()
        request_id = info["username"] +"-" +info["requested_id"]
        
        command = "INSERT INTO requests VALUES(%s, %s, %s, %s, %s);"
        cursor.execute(command, (request_id, info['username'], info['requested_id'], "Pending", "Unseen", ))
        connection.commit()
        
        return JsonResponse({"message": "Success"})


def change_seen(request):
    return JsonResponse({})
