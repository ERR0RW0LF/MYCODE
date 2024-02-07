from tkinter import W
from numpy import less
import webuntis
import datetime
import logging
import time
logging.basicConfig(level=logging.INFO)

# timetable readable


# terminal output style
strikethrough = '\033[09m'
bold = '\033[01m'
underline = '\033[04m'
end = '\033[0m'


# filter timetable output
def filter_tt(tt):
    for i in tt:
        for fach in i.subjects:
            untericht = fach.name
            if untericht != 'sn9.2' and untericht != 'fr9.1' and untericht != 'rk9.1' and untericht != 'wn9.1' and untericht != 'Sch-AG' and untericht != 're9.1' and untericht != 'sn9.1' and untericht != 'Politik im Bili-Band engl.' and untericht != 'rk9.2' and untericht != 'la9.1' and untericht != 'Po (DE)' and untericht != 'Robo-AG' and untericht != 'MINT_KrB':
                anfang = i.start
                faecher[anfang] = [untericht, i.code]
            elif untericht == 'la9.1':
                anfang = i.start
                faecher[anfang] = ['la', i.code]
            elif untericht == 'rk9.2':
                anfang = i.start
                faecher[anfang] = ['rk', i.code]
            elif untericht == 'Po (DE)':
                anfang = i.start
                faecher[anfang] = ['Po', i.code]
            elif untericht == 'Robo-AG':
                anfang = i.start
                faecher[anfang] = ['Rb', i.code]
            elif untericht == 'MINT_KrB':
                anfang = i.start
                faecher[anfang] = ['Mi', i.code]
    return faecher

# group timetable by day and time and filter
def group_tt(tt):
    Monday = {}
    Tuesday = {}
    Wednesday = {}
    Thursday = {}
    Friday = {}
    # example imput for tt:
    '''
    {
        datetime.datetime(2024, 2, 5, 11, 35): 'De', 
        datetime.datetime(2024, 2, 5, 12, 25): 'De', 
        datetime.datetime(2024, 2, 7, 7, 55): 'De', 
        datetime.datetime(2024, 2, 7, 8, 45): 'De', 
        datetime.datetime(2024, 2, 5, 10, 35): 'En', 
        datetime.datetime(2024, 2, 8, 9, 45): 'En', 
        datetime.datetime(2024, 2, 8, 10, 35): 'En', 
        datetime.datetime(2024, 2, 5, 7, 55): 'Ek', 
        datetime.datetime(2024, 2, 5, 8, 45): 'Ek', 
        datetime.datetime(2024, 2, 7, 11, 35): 'Ma', 
        datetime.datetime(2024, 2, 7, 12, 25): 'Ku', 
        datetime.datetime(2024, 2, 9, 7, 55): 'Mu', 
        datetime.datetime(2024, 2, 9, 8, 45): 'Mu', 
        datetime.datetime(2024, 2, 5, 9, 45): 'Ma', 
        datetime.datetime(2024, 2, 8, 7, 55): 'Ma', 
        datetime.datetime(2024, 2, 8, 8, 45): 'Ma', 
        datetime.datetime(2024, 2, 6, 9, 45): 'Ph', 
        datetime.datetime(2024, 2, 6, 10, 35): 'Ph',
        datetime.datetime(2024, 2, 8, 11, 35): 'Bi',
        datetime.datetime(2024, 2, 8, 12, 25): 'Bi',
        datetime.datetime(2024, 2, 6, 7, 55): 'Sp',
        datetime.datetime(2024, 2, 6, 8, 45): 'Sp',
        datetime.datetime(2024, 2, 7, 13, 40): 'Rb', 
        datetime.datetime(2024, 2, 7, 14, 30): 'Rb', 
        datetime.datetime(2024, 2, 9, 9, 45): 'rk', 
        datetime.datetime(2024, 2, 9, 10, 35): 'rk', 
        datetime.datetime(2024, 2, 7, 9, 45): 'la', 
        datetime.datetime(2024, 2, 7, 10, 35): 'la', 
        datetime.datetime(2024, 2, 9, 11, 35): 'la', 
        datetime.datetime(2024, 2, 9, 12, 25): 'la', 
        datetime.datetime(2024, 2, 6, 11, 35): 'Po', 
        datetime.datetime(2024, 2, 6, 12, 25): 'Po'
    }
    '''
    for i in tt:
        if i.weekday() == 0:
            Monday[i] = tt[i]
        elif i.weekday() == 1:
            Tuesday[i] = tt[i]
        elif i.weekday() == 2:
            Wednesday[i] = tt[i]
        elif i.weekday() == 3:
            Thursday[i] = tt[i]
        elif i.weekday() == 4:
            Friday[i] = tt[i]
    
    return Monday, Tuesday, Wednesday, Thursday, Friday

# Print lesson plan
def print_lessen(day: dict, weekday: int):
    dayLessons = []
    for i in lessons:
        dayLessons.append(datetime.datetime.combine(WeekdaysDate[weekday], i))
    for i in dayLessons:
        print(' | ', i.time(), ' | ', end='')
        if i in day:
            if day[i][1] == 'cancelled':
                print(strikethrough, day[i][0], end, ' | ', end='')
            elif day[i][1] == 'irregular':
                print(underline, day[i][0], end, ' | ', end='')
            else:
                print('', day[i][0], '  | ', end='')
            print(day[i][1])
        else:
            print('','--', '  | ')

# print timetable
def print_tt(tt):
    tt = filter_tt(tt)
    MondayS, TuesdayS, WednesdayS, ThursdayS, FridayS = group_tt(tt)
    print('Monday')
    print_lessen(MondayS, 0)
    print()
    print('Tuesday')
    print_lessen(TuesdayS, 1)
    print()
    print('Wednesday')
    print_lessen(WednesdayS, 2)
    print()
    print('Thursday')
    print_lessen(ThursdayS, 3)
    print()
    print('Friday')
    print_lessen(FridayS, 4)
    print('')


# webuntis login
s = webuntis.Session(
    server='mese.webuntis.com',
    username='finn.marquardt',
    password='c:dBta7dr5_X9xzy',
    school='Windthorst-Gym+Meppen',
    useragent='useragent'
)
stundenplan = {}
faecher = {}

today = datetime.datetime.now().date()
Monday = today - datetime.timedelta(days=today.weekday())
Tuesday = Monday + datetime.timedelta(days=1)
Wednesday = Monday + datetime.timedelta(days=2)
Thursday = Monday + datetime.timedelta(days=3)
Friday = Monday + datetime.timedelta(days=4)

Weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
WeekdaysDate = [Monday, Tuesday, Wednesday, Thursday, Friday]

firstLesson = datetime.time(7, 55)
secondLesson = datetime.time(8, 45)
thirdLesson = datetime.time(9, 45)
fourthLesson = datetime.time(10, 35)
fifthLesson = datetime.time(11, 35)
sixthLesson = datetime.time(12, 25)
seventhLesson = datetime.time(13, 40)
eighthLesson = datetime.time(14, 30)

lessons = [firstLesson, secondLesson, thirdLesson, fourthLesson, fifthLesson, sixthLesson, seventhLesson, eighthLesson]

logging.info('IServ Login...')
s.login()

klasse = s.klassen().filter(name='9b')[0]  # schoolclass #1
tt = s.timetable(klasse=klasse, start=Monday, end=Friday)




print(klasse)
print(filter_tt(tt))

Monday, Tuesday, Wednesday, Thursday, Friday = group_tt(filter_tt(tt))

print(Monday)
print_lessen(Monday, 0)

print_tt(tt)


logging.info('IServ Logout...')
s.logout()