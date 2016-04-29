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
        self.conn = sqlite3.connect('./day_data.db')
        self.cur = self.conn.cursor()
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
        self.cur.execute("""SELECT id,name FROM mem_data;""")
        get_name_var = self.cur.fetchall()
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
            self.cur.execute("""SELECT id,name,worktime,workcnt FROM mem_data WHERE name = '{0}';""".format(name))
            work_time_cnt = self.cur.fetchall()[0]
        elif id != 0:
            self.cur.execute("""SELECT id,name,worktime,workcnt FROM mem_data WHERE id = {0};""".format(id))
            work_time_cnt = self.cur.fetchall()[0]
        else:
            print("name input erorr")
            return
        print("{0:>3}:{1:^5}:{2:^5} h:{3:^5} ".format(work_time_cnt[0],work_time_cnt[1],work_time_cnt[2],work_time_cnt[3]))

    def show_shift(self,day = 0):
        if day == 0:
            self.cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
            for month,day,name1,name2,name3 in self.cur.fetchall():
                print("{0}/{1}\n".format(month,day))
                name_id = {name1:self.get_name(name1),name2:self.get_name(name2),name3:self.get_name(name3)}
                print("\t{0}:{1}\n\t{2}:{3}\n\t{4}:{5}\n".format(name1,self.get_name(name1),name2,self.get_name(name2),name3,self.get_name(name3)))
        else:
            self.cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
            a = self.cur.fetchall()
            data = [a[0][x] for x in range(5) ]
            #print(data)
            print("{0}/{1}\n".format(data[0],data[1]))
            print("\t{0}:{1}\n\t{2}:{3}\n\t{4}:{5}\n".format(data[2],self.get_name(data[2]),data[3],self.get_name(data[3]),data[4],self.get_name(data[4])))

    def show(self):
        self.cur.execute("""SELECT month,day,name1,name2,name3,date FROM day_data;""")
        day_data = self.cur.fetchall()
        self.cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
        mem_data = self.cur.fetchall()
        self.cur.execute("""SELECT id,name,req FROM req_data;""")
        req_data = self.cur.fetchall()

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
                    self.insert_mem()
                    self.cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
                    day_data = self.cur.fetchall()
                    self.cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
                    mem_data = self.cur.fetchall()
                    break
                elif var == 'delete' or var == 'd':
                    self.delete_mem()
                    self.cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
                    day_data = self.cur.fetchall()
                    self.cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
                    mem_data = self.cur.fetchall()
                    break
                elif var == 'q' or var == 'quit':
                    islastweek = 1
                    break
                else:
                    print('please input [n,b,i,d,q]')


    def worktime_check(self,day = 0):
        if day == 0:
            day = input('day:')
            print(self.worktime_check(day))
            return
        self.cur.execute("""SELECT isholi,ispreholi FROM day_data WHERE day = {0};""".format(day))
        a = self.cur.fetchall()
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
            self.show_shift(day)
            #free or not in the day
            if self.get_rest(day) == 0 :
                print("There is no seat in the day",day)
                time.sleep(1.5)
                return

            #open database
            self.cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
            mem_data = self.cur.fetchall()
            self.cur.execute("""SELECT name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
            day_data = self.cur.fetchall()[0]
            self.cur.execute("""SELECT id,name,req FROM req_data;""")
            req_data = self.cur.fetchall()

            #show free member at the day
            freemem_id = []
            print("-----These members are free-----")
            for i in range(len(req_data)):
                if day not in req_data[i][2].split(',') and req_data[i][0] not in day_data:
                    self.show_worktime(req_data[i][1])
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

            self.cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = {0};""".format(who))
            data = self.cur.fetchall()[0]

            #confirmation and insert member into shift
            confirm = input("Insert {0}?[y/N]:".format(data[0]))
            if confirm == "y":
                rest = self.get_rest(day)
                if day_data[0] is None:
                    insert_pos = 1
                elif day_data[1] is None:
                    insert_pos = 2
                elif day_data[2] is None:
                    insert_pos = 3
                self.cur.execute("""UPDATE day_data SET name{0} = {1} WHERE day = {2};""".format(insert_pos,who,day) )
                self.cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(data[1]+1,data[2]+self.worktime_check(day),who) )
                self.conn.commit()


    def delete_mem(self):
        print("\n-----Delete member from shift-----\n")

        while(True):
            day = input("Delete day:")
            if (day == 'q'):
                return
            elif self.get_rest(int(day)) == 3:
                print("No member assigned")
                time.sleep(1.5)
                return
            elif day.isdigit() and int(day) < 32:
                break
            print("illegal input")
        self.show_shift(day)

        self.cur.execute("""SELECT name1,name2,name3 FROM day_data WHERE day = '{0}';""".format(day))
        name_id = self.cur.fetchall()[0]
        while(True):
            who = input("who[1,2,3]:")
            if (who == 'q'):
                return
            elif who.isdigit() and int(who) < 4 and name_id[int(who)-1] != None:
                break
            print("illegal input")

        who = int(who)

        self.cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = '{0}';""".format(name_id))
        mem_data = self.cur.fetchall()[0]

        confirm = input("Delete {0} OK?[y/N]:".format(mem_data[0]))
        if confirm == "y":
            self.cur.execute("""UPDATE day_data SET name{0} = NULL WHERE day = {1};""".format(who,day) )
            self.cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(mem_data[1]-1,mem_data[2]-self.worktime_check(day),name_id) )
            self.conn.commit()

    def get_rest(self,day):
        self.cur.execute("""select sum(name1),sum(name2),sum(name3) from day_data where day == {0}""".format(day))
        a = self.cur.fetchall()
        #print("rest shift is",(a[0].count(None)))
        return a[0].count(None)

    def quit(self):
        self.conn.commit()
        self.conn.close()
        exit()




def main():
    console = Console().show()

if __name__ == '__main__':
    print("""
    --------------------
        Shift Editer
    --------------------
    """)
    main()
