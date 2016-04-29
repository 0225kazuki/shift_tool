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

class Console():
    def __init__(self):
        self.conn = sqlite3.connect('./day_data.db')
        self.cur = self.conn.cursor()
        #self.func = Func()
        while True:
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

    def show_shift(self,day = 0):
        print('show_shift_called')
        if day == 0:
            self.cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
            for month,day,name1,name2,name3 in self.cur.fetchall():
                print("{0}/{1}\n".format(month,day))
                name_id = {name1:self.get_name(name1),name2:self.get_name(name2),name3:self.get_name(name3)}
                print("\t{0}:{1}\n\t{2}:{3}\n\t{4}:{5}\n".format(name1,self.get_name(name1),name2,self.get_name(name2),name3,self.get_name(name3)))
        else:
            self.cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
            #print(type(cur.fetchall()))
            a = self.cur.fetchall()
            data = [a[0][x] for x in range(5) ]
            print(data)
            print("{0}/{1}\n".format(data[0],data[1]))
            print("\t{0}:{1}\n\t{2}:{3}\n\t{4}:{5}\n".format(data[2],self.get_name(data[2]),data[3],self.get_name(data[3]),data[4],self.get_name(data[4])))

    def show(self):
        self.cur.execute("""SELECT month,day,name1,name2,name3 FROM day_data;""")
        day_data = self.cur.fetchall()
        self.cur.execute("""SELECT name,worktime,workcnt,id FROM mem_data;""")
        mem_data = self.cur.fetchall()





        x = 0
        for j in range(5):
            print("{0:^7}:{1:^6}:{2:^7}".format('name','time','cnt'),end='')
            print('\t',end='')
            for i in range(x,x+7):
                if i < 31:
                    print("{0:^5}\t".format(str(day_data[i][0])+'/'+str(day_data[i][1])),end='')
            print('\n')
            for name,worktime,workcnt,memid in mem_data:
                print("{0:^5}:{1:^6}:{2:^5}\t".format(name,worktime,workcnt),end='')
                for i in range(x,x+7):
                    if i < 31:
                        if set([memid,]) & set(day_data[i][2:]):
                            print("{0:^5}\t".format("Work"),end='')
                        else:
                            print("{0:^5}\t".format(""),end='')
                print("\n")
            input("next>>>")
            x += 7

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
        print("Insert member into shift\n")

        day = input("insert day:")
        self.show_shift(day)

        self.cur.execute("""SELECT name1,name2,name3 FROM day_data WHERE day = {0};""".format(day))
        a = self.cur.fetchall()[0]
        print(a)
        if self.get_rest(day) == 0 :
            print("There is no seat in day",day)
            return

        who = input("who:")
        self.cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = {0};""".format(who))
        data = self.cur.fetchall()[0]
        #data = [b[0][x] for x in range(3) ]
        print(data)

        confirm = input("OK?[y/n]:")
        if confirm == "y":
            print(a)
            rest = self.get_rest(day)
            if a[0] is None:
                insert_pos = 1
            elif a[1] is None:
                insert_pos = 2
            elif a[2] is None:
                insert_pos = 3
            self.cur.execute("""UPDATE day_data SET name{0} = {1} WHERE day = {2};""".format(insert_pos,who,day) )
            self.cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(data[1]+1,data[2]+self.worktime_check(day),who) )

    def delete_mem(self):
        print("Delete member from shift\n")

        day = input("Delete day:")
        self.show_shift(day)

        who = input("who[1,2,3]:")
        while who != '1' and who != '2' and who != '3':
            print("Illegal Number")
            who = input("who[1,2,3]:")
        who = int(who)
        self.cur.execute("""SELECT name{0} FROM day_data WHERE day = '{1}';""".format(who,day))
        name_id = self.cur.fetchall()[0][0]
        if name_id == None:
            return
        self.cur.execute("""SELECT name,workcnt,worktime FROM mem_data WHERE id = '{0}';""".format(name_id))
        a = cur.fetchall()[0]
        print(a)
        confirm = input("OK?[y/n]:")
        if confirm == "y":
            self.cur.execute("""UPDATE day_data SET name{0} = NULL WHERE day = {1};""".format(who,day) )
            self.cur.execute("""UPDATE mem_data SET workcnt = {0}, worktime = {1} WHERE id = {2};""".format(a[1]-1,a[2]-worktime_check(day),name_id) )

    def get_rest(self,day):
        self.cur.execute("""select sum(name1),sum(name2),sum(name3) from day_data where day == {0}""".format(day))
        a = self.cur.fetchall()
        print("rest shift is",(a[0].count(None)))
        return a[0].count(None)

    def quit(self):
        self.conn.commit()
        self.conn.close()
        exit()




def main():
    console = Console()
    '''conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    while True:
        var = input(">>>")
        if var == "show":
            show_shift()
            continue
        elif var == "":
            continue
        elif var == "insert":
            insert_mem()
            continue
        elif var == "del":
            delete_mem()
            continue
        elif var == "q" or var == "quit":
            conn.commit()
            conn.close()
            exit()
        elif var == "c":
            ans = worktime_check(input("which day"))
            print(ans)
        elif var == "gn":
            name = get_name(input("which id >>>"))
            print(name)
        elif var == "gr":
            get_rest(input("which day >>>"))
        else:
            print("Command not found")
            continue'''

if __name__ == '__main__':
    print("""
    --------------------
        Shift Editer
    --------------------
    """)
    main()
