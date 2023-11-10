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

s.login() # see remark below:
# prefered: with webuntis.Session(...).login() as s:

for klasse in s.klassen():
    print(klasse.name)

print('--------------')

print(s.klassen().filter(name='9b')[0])

print('--------------')

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
friday = monday + datetime.timedelta(days=4)

klasse = s.klassen().filter(name='9b')[0]  # schoolclass #1
tt = s.timetable(klasse=klasse, start=monday, end=friday)

print(tt)

print('--------------')

print(s.subjects().filter(id=7)[0])
print(type(tt))

faecher = {}

for i in tt:
    print('##########')
    for fach in i.subjects:
        untericht = fach.long_name
        if untericht != 'sn9.2' and untericht != 'fr9.1' and untericht != 'rk9.1' and untericht != 'wn9.1' and untericht != 'Schach-AG' and untericht != 're9.1' and untericht != 'sn9.1' and untericht != 'Politik im Bili-Band engl.':
            anfang = i.start
            faecher[anfang] = untericht
            print(untericht)


print(faecher)

for k in sorted(faecher):
    v = faecher.get(k)
    print(k, v)
    time.sleep(1)


s.logout() # see remark below