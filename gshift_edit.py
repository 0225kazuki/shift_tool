import sys
import sqlite3
import configparser

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


print("""
Shift Editer
--------------------
""")


def show_shift(day = 0):
    if day == 0:
        cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
        for month,day,name1,name2,name3 in cur.fetchall():
            print("{0}/{1}\n".format(month,day))
            print("\t{0}\n\t{1}\n\t{2}\n".format(name1,name2,name3))
    else:
        cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
        #print(type(cur.fetchall()))
        a = cur.fetchall()
        data = [a[0][x] for x in range(5) ]
        print(data)
        print("{0}/{1}\n".format(data[0],data[1]))
        print("\t{0}\n\t{1}\n\t{2}\n".format(data[2],data[3],data[4]))

def worktime_check(day):
    cur.execute("""SELECT isholi,ispreholi FROM day_data WHERE day = {0};""".format(day))
    a = cur.fetchall()
    if a == [(0,0)]:
        return worktime["weekday"]
    elif a == [(0,1)]:
        return worktime["bh_weekday"]
    elif a == [(1,0)]:
        return worktime["holiday"]
    elif a == [(1,1)]:
        return worktime["bh_holiday"]

def insert_mem():
    print("Insert member into shift\n")

    day = input("insert day:")
    show_shift(day)

    who = input("who:")
    cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = {0};""".format(who))
    a = cur.fetchall()
    data = [a[0][x] for x in range(3) ]
    print(data)
    confirm = input("OK?[y/n]:")
    if confirm == "y":
        cur.execute("""SELECT rest FROM day_data WHERE day = {0};""".format(day))
        a = cur.fetchall()
        rest = a[0][0]
        print("{0} seats remain now".format(4-rest))
        cur.execute("""UPDATE day_data SET name{0} = {1}, rest = {2} WHERE day = {3};""".format(4-rest,who,rest-1,day) )
        cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(data[1]+1,data[2]+worktime_check(day),who) )




conn = sqlite3.connect('./day_data.db')
cur = conn.cursor()
while True:
    var = input(">>>")

    if var == "show":
        show_shift()
        continue
    elif var == "insert":
        insert_mem()
        continue
    elif var == "c":
        ans = worktime_check(input("which day"))
        print(ans)
        exit
    elif var == "q" or "quit":
        conn.commit()
        conn.close()
        exit()

    else:
        print("Command not found")
        continue
