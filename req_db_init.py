import calendar
import jholiday
import sqlite3
import sys
import configparser

conn = sqlite3.connect('./day_data.db')
cur = conn.cursor()

# 0:mon 1:tue 2:wed 3:thu 4:fri 5:sat 6:sun
date_conv_dict = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}

# load config file
default_config = {
    'weekday' : '0.0',
    'holiday' : '0.0',
    'weekday before holiday' : '0.0',
    'holiday before holiday' : '0.0'
}
config = configparser.SafeConfigParser(default_config)
config.read('setting.conf')
worktime = {'weekday':config.getfloat('worktime', 'weekday'),
'holiday':config.getfloat('worktime', 'holiday'),
'bh_weekday':config.getfloat('worktime', 'weekday before holiday'),
'bh_holiday':config.getfloat('worktime', 'holiday before holiday')
}
member = config.get('member','member').split(",")
print(member)

#create database
cur.execute("""select count(*) from sqlite_master where type='table' and name='req_data';""")
a = cur.fetchall()
if a[0][0] == 0 :
    cur.execute("""CREATE TABLE req_data(id integer primary key,name text,req text);""")
    for i in range(len(member)):
        cur.execute("""INSERT INTO req_data(name) VALUES('{0}');""".format(member[i]))


print("""
---------------------
   shift req input
---------------------
""")

cur.execute("""SELECT id,name,req FROM req_data;""")
data = cur.fetchall()
req = [0]*len(member)
for i in range(len(member)):
    print("input shif req [ex >>>1,2,4,6,7]")
    req[i] = input('{0}>>>'.format(data[i][1]))
    print("inputed",req[i])
    confirm = input("OK?[y/n]>>>")
    if confirm == "y" or confirm == "":
        cur.execute("""UPDATE req_data SET req="{0}" WHERE id={1};""".format(req[i],data[i][0]))


conn.commit()
conn.close()
