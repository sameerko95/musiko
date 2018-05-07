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

def news_feed(request):
	return render(request,'news/news_feed.html')