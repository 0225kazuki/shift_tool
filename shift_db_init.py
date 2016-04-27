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


#create database and distinguish holiday,before holiday
cur.execute("""select count(*) from sqlite_master where type='table' and name='day_data';""")
a = cur.fetchall()
if a[0][0] == 0 :
    cur.execute("""CREATE TABLE day_data(year int,month int,day int,date text,isholi int,ispreholi int,name1 int,name2 int,name3 int,primary key (month,day));""")
    for ele in calendar.Calendar().itermonthdays2(2016,5):
        if ele[0] == 0:
            continue
        cur.execute("""INSERT INTO day_data(year,month,day,date,isholi,ispreholi) VALUES(2016,5,{0},"{1}",0,0);""".format(ele[0],date_conv_dict[ele[1]]))
    cur.execute("""SELECT month,day,date FROM day_data;""")
    for month,day,date in cur.fetchall():
        print("month {0}, day {1}".format(month,day))
        if (jholiday.holiday_name(2016,month,day)) != None or date == "Sat" or date == "Sun":
            #print('{0}-{1} = holiday'.format(month,day))
            cur.execute("""UPDATE day_data SET isholi=1 WHERE day={0};""".format(day))
            cur.execute("""UPDATE day_data SET ispreholi=1 WHERE day={0};""".format(day-1))

#create each member's database
cur.execute("""select count(*) from sqlite_master where type='table' and name='mem_data';""")
a = cur.fetchall()
if a[0][0] == 0 :
    cur.execute("""CREATE TABLE mem_data(id integer primary key,name text,workcnt int,worktime int);""")
    for i in range(len(member)):
        cur.execute("""INSERT INTO mem_data(name,workcnt,worktime) VALUES('{0}',0,0);""".format(member[i]))

conn.commit()
conn.close()
