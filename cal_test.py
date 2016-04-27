import calendar
import jholiday
text = calendar.TextCalendar()
text.formatmonth(2016,5)

print (calendar.month(2016,5))

# 0:mon 1:tue 2:wed 3:thu 4:fri 5:sat 6:sun
for ele in calendar.Calendar().itermonthdays2(2016,5):
    print ('({0} and {1})'.format(ele[0],ele[1]))
    if ele[0] == 0:
        continue
    print(jholiday.holiday_name(2016,5,ele[0]))
    print(type(jholiday.holiday_name(2016,5,ele[0])))
