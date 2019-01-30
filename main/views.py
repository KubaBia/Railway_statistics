from django.views import View
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.response import TemplateResponse
from .models import *
from psycopg2 import connect,OperationalError
import re

import pandas as pd
from sqlalchemy import *

class testpy(View):
    def get(self,request):
        var = request.GET.get("raz")
        return HttpResponse(var)
    def post(self,request):
        print("post")


def connectToDB():
    username = "XXX"
    passwd = "XXX"
    hostname = "XXX"
    db_name = "XXX"
    try:
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        print("Połączenie udane.")
        return cnx
    #     cnx.close()
    except OperationalError:
        print("Nieudane połączenie.")

class homeView(View):
    def get(self,request):
        regex_con = []
        cnx = connectToDB()
        cursor = cnx.cursor()
        cnx.autocommit = True
        sql = "SELECT connection, COUNT(*) FROM train11 GROUP BY connection ORDER BY COUNT(connection)"
        cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        cnx.close()
        for connection_name in result:
            test = re.match(r"^(\d+)",connection_name[0])
            name = test.group(0)
            regex_con.append(name)
        newTable = []
        for i in range(0,len(result)):
            newTable.append([result[i][0],result[i][1],regex_con[i]])
        print(newTable)
        result = newTable
        return render(request,"main/home.html",{"result":result})


class connectionView(View):
    def get(self,request,id):
        cnx = connectToDB()
        cursor = cnx.cursor()
        cnx.autocommit = True
        print(id,"id")
        sql = "SELECT db FROM regex WHERE re = '{}'".format(id)
        cursor.execute(sql)
        name_connection=cursor.fetchone()
        print(name_connection)
        sql = "SELECT index_small,arrival_delay,arrival_time,departure_delay,departure_time,station_name,connection \
                        FROM train11 WHERE connection = '{}'  \
                        ORDER BY arrival_delay ASC".format(name_connection[0])
        cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        cnx.close()
        return TemplateResponse(request,"main/connection.html",{"result":result})