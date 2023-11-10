import webuntis
import datetime
import time

s = webuntis.Session(
    server='mese.webuntis.com',
    username='finn.marquardt',
    password='c:dBta7dr5_X9xzy',
    school='Windthorst-Gym+Meppen',
    useragent='useragent'
)

stundenplan = {}

faecher = {}

s.login()

today = datetime.datetime.now().date()
monday = today - datetime.timedelta(days=today.weekday())
tuesday = monday + datetime.timedelta(days=1)
wednesday = monday + datetime.timedelta(days=2)
thursday = monday + datetime.timedelta(days=3)
friday = monday + datetime.timedelta(days=4)

erstsFach = datetime.time(hour=7, minute=55)
zweitesFach = datetime.time(hour=8, minute=45)
drittesFach = datetime.time(hour=9, minute=45)
viertesFach = datetime.time(hour=10, minute=35)
fuenftesFach = datetime.time(hour=11, minute=35)
saextesFach = datetime.time(hour=12, minute=25)
siebtesFach = datetime.time(hour=13, minute=40)
achtesFach = datetime.time(hour=14, minute=30)

mondayFaecher = {}
tuesdayFaecher = {}
wednesdayFaecher = {}
thursdayFaecher = {}
fridayFaecher = {}

klasse = s.klassen().filter(name='9b')[0]  # schoolclass #1
tt = s.timetable(klasse=klasse, start=monday, end=friday)


for i in tt:
    for fach in i.subjects:
        untericht = fach.name
        if untericht != 'sn9.2' and untericht != 'fr9.1' and untericht != 'rk9.1' and untericht != 'wn9.1' and untericht != 'Schach-AG' and untericht != 're9.1' and untericht != 'sn9.1' and untericht != 'Politik im Bili-Band engl.' and untericht != 'rk9.2' and untericht != 'la9.1' and untericht != 'Po (DE)' and untericht != 'Robo-AG' and untericht != 'MINT_KrB':
            anfang = i.start
            faecher[anfang] = untericht
        elif untericht == 'la9.1':
            anfang = i.start
            faecher[anfang] = 'la'
        elif untericht == 'rk9.2':
            anfang = i.start
            faecher[anfang] = 'rk'
        elif untericht == 'Po (DE)':
            anfang = i.start
            faecher[anfang] = 'Po'
        elif untericht == 'Robo-AG':
            anfang = i.start
            faecher[anfang] = 'Rb'
        elif untericht == 'MINT_KrB':
            anfang = i.start
            faecher[anfang] = 'Mi'

k = 0

for k in sorted(faecher):
    v = faecher.get(k)
    stundenplan[k] = v
    if k == datetime.datetime.combine(monday, erstsFach) or k == datetime.datetime.combine(monday, zweitesFach) or k == datetime.datetime.combine(monday, drittesFach) or k == datetime.datetime.combine(monday, viertesFach) or k == datetime.datetime.combine(monday, fuenftesFach) or k == datetime.datetime.combine(monday, saextesFach) or k == datetime.datetime.combine(monday, siebtesFach) or k == datetime.datetime.combine(monday, achtesFach):
        mondayFaecher[k] = v
    elif k == datetime.datetime.combine(tuesday, erstsFach) or k == datetime.datetime.combine(tuesday, zweitesFach) or k == datetime.datetime.combine(tuesday, drittesFach) or k == datetime.datetime.combine(tuesday, viertesFach) or k == datetime.datetime.combine(tuesday, fuenftesFach) or k == datetime.datetime.combine(tuesday, saextesFach) or k == datetime.datetime.combine(tuesday, siebtesFach) or k == datetime.datetime.combine(tuesday, achtesFach):
        tuesdayFaecher[k] = v
    elif k == datetime.datetime.combine(wednesday, erstsFach) or k == datetime.datetime.combine(wednesday, zweitesFach) or k == datetime.datetime.combine(wednesday, drittesFach) or k == datetime.datetime.combine(wednesday, viertesFach) or k == datetime.datetime.combine(wednesday, fuenftesFach) or k == datetime.datetime.combine(wednesday, saextesFach) or k == datetime.datetime.combine(wednesday, siebtesFach) or k == datetime.datetime.combine(wednesday, achtesFach):
        wednesdayFaecher[k] = v
    elif k == datetime.datetime.combine(thursday, erstsFach) or k == datetime.datetime.combine(thursday, zweitesFach) or k == datetime.datetime.combine(thursday, drittesFach) or k == datetime.datetime.combine(thursday, viertesFach) or k == datetime.datetime.combine(thursday, fuenftesFach) or k == datetime.datetime.combine(thursday, saextesFach) or k == datetime.datetime.combine(thursday, siebtesFach) or k == datetime.datetime.combine(thursday, achtesFach):
        thursdayFaecher[k] = v
    elif k == datetime.datetime.combine(friday, erstsFach) or k == datetime.datetime.combine(friday, zweitesFach) or k == datetime.datetime.combine(friday, drittesFach) or k == datetime.datetime.combine(friday, viertesFach) or k == datetime.datetime.combine(friday, fuenftesFach) or k == datetime.datetime.combine(friday, saextesFach) or k == datetime.datetime.combine(friday, siebtesFach) or k == datetime.datetime.combine(friday, achtesFach):
        fridayFaecher[k] = v

i = 0
print('----------------------------------------------')
for i in range(0, 6):
    print('|  ', mondayFaecher.get(list(mondayFaecher)[i]), '  |  ', tuesdayFaecher.get(list(tuesdayFaecher)[i]), '  |  ', wednesdayFaecher.get(list(wednesdayFaecher)[i]), '  |  ', thursdayFaecher.get(list(thursdayFaecher)[i]), '  |  ', fridayFaecher.get(list(fridayFaecher)[i]), '  |')
    i = i + 1
print('|  ', '//', '  |  ', tuesdayFaecher.get(list(tuesdayFaecher)[i]), '  |  ', wednesdayFaecher.get(list(wednesdayFaecher)[i]), '  |  ', thursdayFaecher.get(list(thursdayFaecher)[i]), '  |  ', '//', '  |')
i = i + 1
print('|  ', '//', '  |  ', tuesdayFaecher.get(list(tuesdayFaecher)[i]), '  |  ', wednesdayFaecher.get(list(wednesdayFaecher)[i]), '  |  ', thursdayFaecher.get(list(thursdayFaecher)[i]), '  |  ', '//', '  |')
print('----------------------------------------------')

s.logout() # see remark below