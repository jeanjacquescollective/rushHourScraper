from datetime import datetime
import time
import re
array = ['6\u202fam.', '7\u202fam.', '8\u202fam.', '9\u202fam.', '0\u202fam.', '1\u202fam.', '2\u202fpm.', '1\u202fpm.', '3\u202fpm.', '4\u202fpm.', '5\u202fpm.', '6\u202fpm.', '7\u202fpm.', '8\u202fpm.', '9\u202fpm.', '0\u202fpm.', ' at .']


def formatHours(array):
    array = list(filter(lambda x: 'at' not in x, array))
    for i in range(len(array)):
        array[i] = formatHour(array[i])
        
    l = [datetime.strptime(date,'%I:%M %p') for date in array]
    l.sort()
    l =  [date.strftime('%I:%M %p') for date in l]
    return l


def formatHour(hour):
    hour = hour.replace('\u202f', ':00 ')
    hour = hour.replace('.', '')
    hour = hour.replace('am', 'AM')
    hour = hour.replace('pm', 'PM')
    hour = hour.replace('0:00', '12:00')
    return hour

print(formatHours(array))