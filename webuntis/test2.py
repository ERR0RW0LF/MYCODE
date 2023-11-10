import webuntis
import datetime
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)


try:
    time.sleep(60)
    logging.info("Test start")
    
    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
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
    
    if 1:
        logging.info("E-paper refresh")
        epd.init()
        logging.info("1.Drawing on the image...")
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0,0),(50,50)],outline = 0)
        draw.rectangle([(55,0),(100,50)],fill = 0)
        draw.line([(0,0),(50,50)], fill = 0,width = 1)
        draw.line([(0,50),(50,0)], fill = 0,width = 1)
        draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
        draw.ellipse((55, 60, 95, 100), outline = 0)
        draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
        draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
        draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
        draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
        draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
        draw.text((110, 90), u'微雪电子', font = font24, fill = 0)
        # image = image.rotate(180) # rotate
        epd.display(epd.getbuffer(image))
        time.sleep(2)
    else:
        logging.info("E-paper refreshes quickly")
        epd.init_fast()
        logging.info("1.Drawing on the image...")
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0,0),(50,50)],outline = 0)
        draw.rectangle([(55,0),(100,50)],fill = 0)
        draw.line([(0,0),(50,50)], fill = 0,width = 1)
        draw.line([(0,50),(50,0)], fill = 0,width = 1)
        draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
        draw.ellipse((55, 60, 95, 100), outline = 0)
        draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
        draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
        draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
        draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
        draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
        draw.text((110, 90), u'微雪电子', font = font24, fill = 0)
        # image = image.rotate(180) # rotate
        epd.display_fast(epd.getbuffer(image))
        time.sleep(2)
    
    logging.info('2.show WebUntis ...')
    webUntis_image = Image.new('1', (epd.height, epd.width), 255)
    webUntis_draw = ImageDraw.Draw(webUntis_image)
    epd.displayPartBaseImage(epd.getbuffer(webUntis_image))
    num = 0
    
    logging.info('IServ Login...')
    s.login()
    while(True):
        logging.info('refresh')
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
        
        webUntis_draw.rectangle((0, 0, 250, 122), fill= 255)
        for i in range(0, 6):
            webUntis_draw.text((0, i*15), text='|', font= font15, fill= 0)
            webUntis_draw.text((20, i*15), text= mondayFaecher.get(list(mondayFaecher)[i]), font= font15, fill= 0)
            webUntis_draw.text((40, i*15), text='|', font= font15, fill= 0)
            webUntis_draw.text((60, i*15), text= tuesdayFaecher.get(list(tuesdayFaecher)[i]), font= font15, fill= 0)
            webUntis_draw.text((80, i*15), text='|', font= font15, fill= 0)
            webUntis_draw.text((100, i*15), text= wednesdayFaecher.get(list(wednesdayFaecher)[i]), font= font15, fill= 0)
            webUntis_draw.text((120, i*15), text='|', font= font15, fill= 0)
            webUntis_draw.text((140, i*15), text= thursdayFaecher.get(list(thursdayFaecher)[i]), font= font15, fill= 0)
            webUntis_draw.text((160, i*15), text='|', font= font15, fill= 0)
            webUntis_draw.text((180, i*15), text= fridayFaecher.get(list(fridayFaecher)[i]), font= font15, fill= 0)
            webUntis_draw.text((200, i*15), text='|', font= font15, fill= 0)
            i = i + 1
        webUntis_draw.text((0, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((20, i*15), text='//', font= font15, fill= 0)
        webUntis_draw.text((40, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((60, i*15), text= tuesdayFaecher.get(list(tuesdayFaecher)[i]), font= font15, fill= 0)
        webUntis_draw.text((80, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((100, i*15), text= wednesdayFaecher.get(list(wednesdayFaecher)[i]), font= font15, fill= 0)
        webUntis_draw.text((120, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((140, i*15), text= thursdayFaecher.get(list(thursdayFaecher)[i]), font= font15, fill= 0)
        webUntis_draw.text((160, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((180, i*15), text='//', font= font15, fill= 0)
        webUntis_draw.text((200, i*15), text='|', font= font15, fill= 0)
        i = i + 1
        webUntis_draw.text((0, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((20, i*15), text='//', font= font15, fill= 0)
        webUntis_draw.text((40, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((60, i*15), text= tuesdayFaecher.get(list(tuesdayFaecher)[i]), font= font15, fill= 0)
        webUntis_draw.text((80, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((100, i*15), text= wednesdayFaecher.get(list(wednesdayFaecher)[i]), font= font15, fill= 0)
        webUntis_draw.text((120, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((140, i*15), text= thursdayFaecher.get(list(thursdayFaecher)[i]), font= font15, fill= 0)
        webUntis_draw.text((160, i*15), text='|', font= font15, fill= 0)
        webUntis_draw.text((180, i*15), text='//', font= font15, fill= 0)
        webUntis_draw.text((200, i*15), text='|', font= font15, fill= 0)
        
        epd.displayPartial(epd.getbuffer(webUntis_image))
        num = num + 1
        time.sleep(60*5)
        if(num == 10):
            break
    logging.info('IServ logout...')
    s.logout()
    
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    num = 0
    while (True):
        time_draw.rectangle((120, 80, 220, 105), fill = 255)
        time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        if(num == 1000):
            break
    
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    logging.info('IServ logout...')
    s.logout()
    epd2in13_V4.epdconfig.module_exit()
    exit()