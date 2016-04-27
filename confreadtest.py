import calendar
import jholiday
import sqlite3
import sys
import configparser

# 0:mon 1:tue 2:wed 3:thu 4:fri 5:sat 6:sun
date_conv_dict = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}

default_config = {
    'weekday':'0.0',
    'holiday':'0.0',
    'weekday before holiday':'0.0',
    'holiday before holiday':'0.0'
}
config = configparser.SafeConfigParser(default_config)
config.read('setting.conf')
# セクション名、キー名を指定して値を取得
print(config.getfloat('worktime', 'weekday'))
print(config.getfloat('worktime', 'holiday'))
print(config.getfloat('worktime', 'weekday before holiday'))
print(config.getfloat('worktime', 'holiday before holiday'))

member = config.get('member','member').split(",")
for i in range(len(member)):
    print("{0}    {1}".format(i,member[i]))
    #print(type(member[i]))
