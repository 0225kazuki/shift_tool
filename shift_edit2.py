import sys
import sqlite3
import configparser
import time

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

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[31m'
FAIL = '\033[91m'
ENDC = '\033[0m'


class Console():
    def __init__(self):
        conn = sqlite3.connect('./day_data.db')
        cur = conn.cursor()
        '''while True:
            var = input(">>>")
            if var == "":
                continue
            elif hasattr(Console,var) == False:
                print("command not found")
                continue
            else:
                func = getattr(Console,var)
                func(self)
            continue
'''

    def get_name(self,id):
        cur.execute("""SELECT id,name FROM mem_data;""")
        get_name_var = cur.fetchall()
        if id is None:
            return None
        id = int(id)
        for i in range(len(get_name_var)):
            if get_name_var[i][0] == id:
                name = get_name_var[i][1]
                return name
        print("not found id {0}".format(id))
        return None

    def show_worktime(self,name = '',id = 0):
        if name != '':
            cur.execute("""SELECT id,name,worktime,workcnt FROM mem_data WHERE name = '{0}';""".format(name))
            work_time_cnt = cur.fetchall()[0]
        elif id != 0:
            cur.execute("""SELECT id,name,worktime,workcnt FROM mem_data WHERE id = {0};""".format(id))
            work_time_cnt = cur.fetchall()[0]
        else:
            print("name input erorr")
            return
        print("{0:>3}:{1:^5}:{2:^5} h:{3:^5} ".format(work_time_cnt[0],work_time_cnt[1],work_time_cnt[2],work_time_cnt[3]))

    def show_shift(self,day = 0):
        if day == 0:
            cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
            for month,day,name1,name2,name3 in cur.fetchall():
                print("{0}/{1}\n".format(month,day))
                name_id = {name1:get_name(name1),name2:get_name(name2),name3:get_name(name3)}
                print("\t{0}:{1}\n\t{2}:{3}\n\t{4}:{5}\n".format(name1,get_name(name1),name2,get_name(name2),name3,get_name(name3)))
        else:
            cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
            a = cur.fetchall()
            data = [a[0][x] for x in range(5) ]
            #print(data)
            print("{0}/{1}\n".format(data[0],data[1]))
            print("\t{0}:{1}\n\t{2}:{3}\n\t{4}:{5}\n".format(data[2],get_name(data[2]),data[3],get_name(data[3]),data[4],get_name(data[4])))

    def show(self):
        cur.execute("""SELECT month,day,name1,name2,name3,date FROM day_data;""")
        day_data = cur.fetchall()
        cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
        mem_data = cur.fetchall()
        cur.execute("""SELECT id,name,req FROM req_data;""")
        req_data = cur.fetchall()

        day_num = 0
        islastweek = 0
        while islastweek == 0:
            #print mem data
            print("{0:^7}:{1:^6}:{2:^7}".format('name','time','cnt'),end='')
            print('\t',end='')
            #print day header
            for i in range(day_num,day_num+7):
                if i < 31:
                    print("{0:^6}\t".format(str(day_data[i][0])+'/'+str(day_data[i][1])+str(day_data[i][5])),end='')
                else:
                    islastweek = 1
            print('\n')
            #print shift table
            for name,worktime,workcnt,memid in mem_data:
                print("{0:^5}:{1:^6}:{2:^5}\t".format(name,worktime,workcnt),end='')
                for i in range(day_num,day_num+7):
                    if i < 31:
                        if set([memid,]) & set(day_data[i][2:]):
                            print(OKGREEN,"{0:^5}\t".format("Wor"),ENDC,end='')
                        elif str(i+1) in req_data[memid-1][2].split(','):
                            print(WARNING,"{0:^5}\t".format("--"),ENDC,end='')
                        else:
                            print("{0:^5}\t".format(""),end='')
                print("\n")
            #editor control
            while True:
                var = input("[next,back,insert,delete,quit]>>>")
                if var == 'n' or var == 'next':
                    day_num += 7
                    break
                elif var == 'b' or var == 'back':
                    if day_num < 7:
                        print("This is first week")
                    else:
                        day_num -= 7
                        islastweek = 0
                    break
                elif var == 'insert' or var == 'i':
                    insert_mem()
                    cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
                    day_data = cur.fetchall()
                    cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
                    mem_data = cur.fetchall()
                    break
                elif var == 'delete' or var == 'd':
                    delete_mem()
                    cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
                    day_data = cur.fetchall()
                    cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
                    mem_data = cur.fetchall()
                    break
                elif var == 'q' or var == 'quit':
                    islastweek = 1
                    break
                else:
                    print('please input [n,b,i,d,q]')


    def worktime_check(self,day = 0):
        if day == 0:
            day = input('day:')
            print(worktime_check(day))
            return
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

    def insert_mem(self):
        print("\n-----Insert member into shift-----\n")

        while(True):
            day = input("insert day:")
            if (day == 'q'):
                return
            elif day.isdigit() and int(day) < 32:
                break
            print("illegal input")

        while True:
            show_shift(day)
            #free or not in the day
            if get_rest(day) == 0 :
                print("There is no seat in the day",day)
                time.sleep(1.5)
                return

            #open database
            cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
            mem_data = cur.fetchall()
            cur.execute("""SELECT name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
            day_data = cur.fetchall()[0]
            cur.execute("""SELECT id,name,req FROM req_data;""")
            req_data = cur.fetchall()

            #show free member at the day
            freemem_id = []
            print("-----These members are free-----")
            for i in range(len(req_data)):
                if day not in req_data[i][2].split(',') and req_data[i][0] not in day_data:
                    show_worktime(req_data[i][1])
                    freemem_id.append(req_data[i][0])
            #input insert member id
            while True:
                who = input("who[id]:")
                if (who == 'q'):
                    return
                elif who == '':
                    continue
                elif int(who) in freemem_id:
                    break
                print("illegal input")

            cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = {0};""".format(who))
            data = cur.fetchall()[0]

            #confirmation and insert member into shift
            confirm = input("Insert {0}?[y/N]:".format(data[0]))
            if confirm == "y":
                rest = get_rest(day)
                if day_data[0] is None:
                    insert_pos = 1
                elif day_data[1] is None:
                    insert_pos = 2
                elif day_data[2] is None:
                    insert_pos = 3
                cur.execute("""UPDATE day_data SET name{0} = {1} WHERE day = {2};""".format(insert_pos,who,day) )
                cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(data[1]+1,data[2]+worktime_check(day),who) )
                conn.commit()


    def delete_mem(self):
        print("\n-----Delete member from shift-----\n")

        while(True):
            day = input("Delete day:")
            if (day == 'q'):
                return
            elif get_rest(int(day)) == 3:
                print("No member assigned")
                time.sleep(1.5)
                return
            elif day.isdigit() and int(day) < 32:
                break
            print("illegal input")
        show_shift(day)

        cur.execute("""SELECT name1,name2,name3 FROM day_data WHERE day = '{0}';""".format(day))
        name_id = cur.fetchall()[0]
        while(True):
            who = input("who[1,2,3]:")
            if (who == 'q'):
                return
            elif who.isdigit() and int(who) < 4 and name_id[int(who)-1] != None:
                break
            print("illegal input")

        who = int(who)

        cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = '{0}';""".format(name_id))
        mem_data = cur.fetchall()[0]

        confirm = input("Delete {0} OK?[y/N]:".format(mem_data[0]))
        if confirm == "y":
            cur.execute("""UPDATE day_data SET name{0} = NULL WHERE day = {1};""".format(who,day) )
            cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(mem_data[1]-1,mem_data[2]-worktime_check(day),name_id) )
            conn.commit()

    def get_rest(self,day):
        cur.execute("""select sum(name1),sum(name2),sum(name3) from day_data where day == {0}""".format(day))
        a = cur.fetchall()
        #print("rest shift is",(a[0].count(None)))
        return a[0].count(None)

    def quit(self):
        conn.commit()
        conn.close()
        exit()


#for web app
def get_day():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT day,date,isholi FROM day_data;""")
    day_data = cur.fetchall()
    return day_data
    conn.close()

def get_mem():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
    mem_data = cur.fetchall()
    return mem_data
    conn.close()

def get_id():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT id,name FROM mem_data;""")
    id_data = cur.fetchall()
    return id_data
    conn.close()

def get_time():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT id,name,workcnt,worktime FROM mem_data;""")
    time_data = cur.fetchall()
    return time_data
    conn.close()

def get_req():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT id,name,req FROM req_data;""")
    req_data = cur.fetchall()
    return req_data
    conn.close()


def insert(day,who):
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    #open database
    cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
    mem_data = cur.fetchall()
    cur.execute("""SELECT name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
    day_data = cur.fetchall()[0]
    cur.execute("""SELECT id,name,req FROM req_data;""")
    req_data = cur.fetchall()
    cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = {0};""".format(who))
    data = cur.fetchall()[0]

    print(day_data)
    if day_data[0] is None:
        insert_pos = 1
    elif day_data[1] is None:
        insert_pos = 2
    elif day_data[2] is None:
        insert_pos = 3
    print (insert_pos,'day',day)

    cur.execute("""UPDATE day_data SET name{0} = {1} WHERE day = {2};""".format(insert_pos,who,day) )
    cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(data[1]+1,data[2]+worktime_check(day),who) )
    conn.commit()
    conn.close()

def worktime_check(day):
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
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

def delete(day,memid):
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT name1,name2,name3 FROM day_data WHERE day = '{0}';""".format(day))
    name_id = cur.fetchall()[0]
    who = 0
    print('fetch',memid)
    if name_id[0] == int(memid):
        who = 1
    elif name_id[1] == int(memid):
        who = 2
    elif name_id[2] == int(memid):
        who = 3
    print('del pos ',who)

    cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = '{0}';""".format(memid))
    mem_data = cur.fetchall()[0]
    print(mem_data)

    cur.execute("""UPDATE day_data SET name{0} = NULL WHERE day = {1};""".format(who,day) )
    cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(mem_data[1]-1,mem_data[2]-worktime_check(day),memid) )
    # print(mem_data[1]-1,'/',mem_data[2]-worktime_check(day),memid)

    conn.commit()
    conn.close()

def main():
    console = Console().show()

if __name__ == '__main__':
    print("""
    --------------------
        Shift Editer
    --------------------
    """)
    main()
