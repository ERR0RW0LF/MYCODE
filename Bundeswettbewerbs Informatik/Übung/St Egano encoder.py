from PIL import Image, ImageDraw
import numpy as np
import math
import random
import time
import os
import sys

def encode_image(image: Image, message: str):
    # message to ascii decimal
    messageText = message
    message = []
    for c in messageText:
        # check if c can be converted to ascii
        if ord(c) <= 255:
            message.append(ord(c))
        else:
            print(f"Character '{c}' can't be converted to ascii")
        
    # r = ascii, g = nach rechts, b = nach unten
    # wenn g und b = 0, dann ist das ende des textes erreicht
    # durch g und b wird die position des nächsten buchstaben bestimmt
    # wenn g über den rand geht dann geht es auf der linken seite weiter
    # wenn b über den rand geht dann geht es auf der oberen seite weiter
    # Bild in numpy array umwandeln
    img = np.array(image)
    print(len(message))
    # Text einfügen
    curserG = 0
    curserB = 0
    g = random.randint(1, 255)
    b = random.randint(1, 255)
    altertPositions = [(curserG, curserB)]
    img[curserB, curserG, 1] = g
    img[curserB, curserG, 2] = b
    img[curserB, curserG, 0] = message[0]
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    draw.point((curserG, curserB), fill=(message[0], g, b))
    img = np.array(img)
    print(message[0])
    for i in range(1,len(message)):
        
        
        while g + curserG >= img.shape[1]:
            if g + curserG > img.shape[1] - 1:
                g = g - (img.shape[1] - curserG)
                curserG = 0
        
        while b + curserB >= img.shape[0]:
            if b + curserB > img.shape[0] - 1:
                b = b - (img.shape[0] - curserB)
                curserB = 0
        
        curserG += g
        curserB += b
        while (curserG, curserB) in altertPositions:
            b = random.randint(1, 255)
            g = random.randint(1, 255)
            while g + curserG >= img.shape[1]:
                if g + curserG > img.shape[1] - 1:
                    g = g - (img.shape[1] - curserG)
                    curserG = 0

            while b + curserB >= img.shape[0]:
                if b + curserB > img.shape[0] - 1:
                    b = b - (img.shape[0] - curserB)
                    curserB = 0
            
            curserG += g
            curserB += b
            random.seed(time.time() + random.randint(1, 1000) + time.time() + random.randint(1, 1000) + (time.time() + random.randint(1, 1000) + time.time() + random.randint(1, 1000))/random.randint(1, 1000))
        
        altertPositions.append((curserG, curserB))
        
        img[curserB, curserG, 2] = g
        img[curserB, curserG, 1] = b
        #if i % 100 >= 0:
        #    print(f"{i}/{len(message)}")
        
        img[curserB, curserG, 0] = message[i]
        
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        draw.point((curserG, curserB), fill=(message[i], g, b))
        img = np.array(img)
    img[curserB, curserG, 1] = 0
    img[curserB, curserG, 2] = 0
    img[curserB, curserG, 0] = message[i]
    # Bild speichern
    return Image.fromarray(img)

# load massage and ignore errors and skip them
text = """
Meppen
Der Titel dieses Artikels ist mehrdeutig. Weitere Bedeutungen sind unter Meppen (Begriffsklärung) aufgeführt.
Wappen 	Deutschlandkarte
	
Meppen
Deutschlandkarte, Position der Stadt Meppen hervorgehoben
Basisdaten
Koordinaten: 	♁52° 42′ N, 7° 18′ OKoordinaten: 52° 42′ N, 7° 18′ O | | OSM
Bundesland: 	Niedersachsen
Landkreis: 	Emsland
Höhe: 	14 m ü. NHN
Fläche: 	188,4 km2
Einwohner: 	36.117 (31. Dez. 2022)[1]
Bevölkerungsdichte: 	192 Einwohner je km2
Postleitzahl: 	49716
Vorwahl: 	05931
Kfz-Kennzeichen: 	EL
Gemeindeschlüssel: 	03 4 54 035
Stadtgliederung: 	13 Ortschaften
Adresse der
Stadtverwaltung: 	Markt 43
49716 Meppen
Website: 	www.meppen.de
Bürgermeister: 	Helmut Knurbein (parteilos)
Lage der Stadt Meppen im Landkreis Emsland
Karte

Meppen ist die Kreisstadt des Landkreises Emsland und eine selbständige Gemeinde im Westen des Landes Niedersachsen, nahe der Grenze zu den Niederlanden.
Inhaltsverzeichnis

    1 Geografie
        1.1 Geografische Lage
        1.2 Klima
        1.3 Nachbargemeinden
        1.4 Stadtgliederung
    2 Geschichte
        2.1 Vorgeschichte
        2.2 Namensherkunft
        2.3 Historische Daten
        2.4 Kriegsende 1945
        2.5 Einwohnerentwicklung
    3 Politik
        3.1 Rat
        3.2 Bürgermeister
        3.3 Wappen
        3.4 Städtepartnerschaften
    4 Kultur und Sehenswürdigkeiten
        4.1 Theater
        4.2 Museen
        4.3 Shantychor
        4.4 Bauwerke
        4.5 Parks
        4.6 Naturdenkmäler
        4.7 Sport
            4.7.1 Sportvereine
            4.7.2 Sportanlagen
            4.7.3 Inklusion
        4.8 Regelmäßige kulturelle Veranstaltungen
    5 Wirtschaft und Infrastruktur
        5.1 Wirtschaft
        5.2 Beschäftigte
        5.3 Verkehr
            5.3.1 Straße
            5.3.2 Schienenverkehr
            5.3.3 Busse
            5.3.4 Fahrrad
            5.3.5 Schiffsverkehr
        5.4 Medien
            5.4.1 Printmedien
            5.4.2 Onlinemedien
            5.4.3 Hörfunk und Fernsehen
        5.5 Gesundheit
        5.6 Öffentliche Einrichtungen
        5.7 Bildung
            5.7.1 Gymnasien
            5.7.2 Oberschule
            5.7.3 Haupt- und Realschulen
            5.7.4 Grundschulen
            5.7.5 Förderschulen und Tagesbildungsstätte
            5.7.6 Berufsbildende Schulen
            5.7.7 Weitere Schulen
        5.8 Kirchen
    6 Persönlichkeiten
        6.1 Ehrenbürger
        6.2 In Meppen geborene Personen
        6.3 Persönlichkeiten, die vor Ort gewirkt haben
    7 Trivia
    8 Literatur
    9 Weblinks
    10 Einzelnachweise

Geografie
Geografische Lage
Die Höltingmühle markiert die Hasemündung

Meppen liegt im Zentrum des Emslandes an der Mündung der Hase in die Ems. Etwa einen halben Kilometer vor ihrer Mündung in die Ems nimmt die Hase den Dortmund-Ems-Kanal auf, der südlich von Meppen in einem künstlich erstellten Gewässerbett verläuft. Nördlich von Meppen wird für den Dortmund-Ems-Kanal größtenteils der ausgebaute Flusslauf der Ems genutzt.

Naturräumlich befindet sich Meppen im Norddeutschen Tiefland in der Dümmer-Geestniederung. Längs der Flussläufe von Ems und Hase erstrecken sich schmale Talsandgebiete, welche vielerorts überdeckt sind durch Dünen. Diese sind heute größtenteils durch Aufforstung mit Nadelbäumen bewaldet. Im Nordosten des Stadtgebietes hat Meppen Anteil an Ausläufern des Geestrückens Hümmling, im Südosten am Lingener Land. Am Westrand des Stadtgebietes beginnt das weitgehend kultivierte Bourtanger Moor, östlich des Emstals befindet sich im Norden des Stadtgebietes ein kleiner Teil des unter Naturschutz stehenden Hochmoorgebietes Tinner Dose.[2]

Das Stadtzentrum befindet sich 18 Kilometer östlich der niederländischen Grenze. Die Stadt Lingen (Ems) liegt Luftlinie 20 Kilometer südlich, die Stadt Papenburg 45 Kilometer nördlich.

Durch das Gebiet der Stadt Meppen verlaufen in Ost-West-Richtung die Europastraße E 233 – in diesem Streckenabschnitt als Bundesstraße 402, in Nord-Süd-Richtung die Bundesautobahn A 31 und die Bundesstraße 70.

Meppen wird von einer Kulturroute des Europarats, nämlich der Straße der Megalithkultur berührt.
Klima

In Meppen herrscht ein gemäßigtes Seeklima vor, das durch Nordwestwinde von der Nordsee beeinflusst wird. Im langjährigen Mittel erreicht die Lufttemperatur an der Station Meppen 8,9 °C und es fallen etwa 740 Millimeter Niederschlag. Die tiefsten Temperaturen werden zwischen Dezember und Februar, die Höchstwerte werden im Juli und August erreicht.
Klimatabelle für Meppen
	Jan 	Feb 	Mär 	Apr 	Mai 	Jun 	Jul 	Aug 	Sep 	Okt 	Nov 	Dez 		
Mittl. Tagesmax. (°C) 	3 	4 	8 	13 	18 	21 	22 	22 	19 	14 	8 	4 	⌀ 	13
Mittl. Tagesmin. (°C) 	−2 	−2 	0 	3 	7 	10 	12 	12 	9 	6 	2 	−1 	⌀ 	4,7
Niederschlag (mm) 	65,9 	43,7 	53,9 	49,1 	57,2 	72,9 	70,8 	67,9 	59,6 	58,8 	67,6 	72,1 	Σ 	739,5
Sonnenstunden (h/d) 	1 	2 	3 	5 	7 	7 	6 	6 	5 	3 	2 	1 	⌀ 	4
Regentage (d) 	11 	9 	10 	10 	10 	11 	10 	10 	9 	9 	11 	12 	Σ 	122
Quelle: [3]
Nachbargemeinden

Meppen grenzt an folgende Städte und Gemeinden: die Stadt Haren (Ems) im Norden, die Samtgemeinde Sögel im Nordosten, die Stadt Haselünne im Osten, die Gemeinde Geeste im Süden und die Gemeinde Twist im Westen.
Stadtgliederung
Meppen in den Grenzen vom 1. Juli 1967 – Nummerierung der Stadtteile innerhalb der Kernstadt – Grau: Bebaute Fläche (Stand 2006).

Am 1. Juli 1967 schlossen sich die Stadt Meppen und die Gemeinde Vormeppen auf freiwilliger Basis zusammen. Heute sind diese beiden ehemaligen Gemeinden überwiegend zusammengewachsen, eine Abgrenzung ist kaum noch möglich. Die so gebildete „Kernstadt“, also ohne die am 1. März 1974 eingemeindeten Ortsteile, gliedert sich in folgende Stadtteile:

    Die Altstadt ist der historische Stadtkern unmittelbar südlich des Zusammenflusses von Ems und Hase. Sie ist umgeben vom Stadtwall, einem Relikt der ehemaligen Stadtbefestigung, heute eine baumbestandene Promenade. Im Zentrum der Altstadt befindet sich der Marktplatz und auf diesem freistehend das historische Rathaus. In unmittelbarer Nähe des Rathauses befindet sich östlich die Gymnasialkirche, etwas weiter entfernt südlich die Propsteikirche. Traditionell ist der Marktplatz und seit den 1980er Jahren zunehmend auch die westliche Altstadt geprägt vom Einzelhandel. Die nördliche Altstadt dominieren Banken und Behörden, am Ostrand befindet sich das Windthorst-Gymnasium, während der Südosten vom Krankenhaus Ludmillenstift eingenommen wird. Direkt an der Ems liegen außerhalb des Stadtwalls ein Campingplatz sowie das Emsbad (Frei- und Hallenbad).
    Esterfeld liegt im Westen der Kernstadt am linken Emsufer und ist durch rege Bautätigkeit vor allem in den 1960er und 1970er Jahren zum Stadtteil mit den meisten Einwohnern geworden.
    Feldkamp/Helter Damm ist ein Wohngebiet im Südosten der Kernstadt, das seit Mitte der 1980er-Jahre als Neubaugebiet ausgebaut wird.
    Die Kuhweide südlich der Altstadt wurde ab Ende der 1950er-Jahre bebaut – nach der Eindeichung des Überschwemmungsgebietes der Ems und dem Bau eines Schöpfwerkes.
    Die Neustadt liegt am rechten Hase- und Emsufer im Nordosten der Kernstadt. In der Neustadt befinden sich der Bahnhof Meppen und die Kreisverwaltung des Landkreises Emsland. 2013 wurde in der Fußgängerzone Bahnhofstraße die Einkaufspassage MEP eröffnet mit 45 Einzelhandelsgeschäften und Gastronomiebetrieben auf über 13.000 Quadratmeter Verkaufsfläche.[4] In den Jahren vor dem Bau der MEP hatte sich dieser Teil der Bahnhofstraße zunehmend zu einem städtebaulichen Problemgebiet entwickelt, gekennzeichnet durch Leerstände und verfallende Bausubstanz.[5] Um Platz für das MEP zu schaffen, wurde die alte Bausubstanz großflächig abgerissen.
    Nödike befindet sich im Süden der Kernstadt links des Dortmund-Ems-Kanals. Hier befindet sich das größte Gewerbegebiet der Stadt.
    Schleusengruppe im Süden der Kernstadt liegt gegenüber von Nödike rechts des Dortmund-Ems-Kanals. Die Siedlung ist benannt nach der Schleusengruppe aus der Kleinen Schleuse Meppen und der Großen Schleuse Meppen.

Am 1. Juli 1970 wurde ein kleiner Teil der aufgelösten Gemeinde Groß Fullen mit damals etwa 20 Einwohnern eingegliedert. Infolge der Gemeindereform gehören seit dem 1. März 1974 die am 1. Juli 1970 aus den bis dahin selbständigen Gemeinden Groß Fullen (teilweise), Klein Fullen, Rühle und Versen neu gebildete Gemeinde Emslage ohne Rühlerfeld und Rühlermoor sowie die Dörfer Apeldorn, Bokeloh, Borken, Helte, Hemsen, Holthausen, Hüntel, Schwefingen und Teglingen zu Meppen.[6]
Gliederung Meppens – Nummerierung der 1974 eingemeindeten Ortsteile

    Apeldorn (777)
    Bokeloh (1253)
    Borken (545)
    Groß Fullen (1072)
    Klein Fullen (401)
    Helte (596)
    Hemsen (750)
    Holthausen (142)
    Hüntel (328)
    Rühle (1397)
    Schwefingen (442)
    Teglingen (771)
    Versen (1795)

(in Klammern die Einwohnerzahlen am 9. März 2005)
Geschichte
Vorgeschichte
Großsteingrab „Der Steinerne Schlüssel“ in Apeldorn

    Der Wohnplatz von Meppen-Nödike stammt aus der späten Altsteinzeit.
    In Emslage befindet sich der mesolithische Wohnplatz von Meppen-Emslage.
    In Apeldorn steht das neolithische Großsteingrab „Der Steinerne Schlüssel“. Es bildet die Station 13 der Straße der Megalithkultur und ist unter der Sprockhoff-Nummer 852 registriert.
    In Teglingen wurde der Grabhügel von Meppen-Teglingen der jungneolithischen Einzelgrabkultur ausgegraben.
    Eine Siedlung der vorrömischen Eisenzeit wurde im Ortsteil Esterfeld ausgegraben.

Namensherkunft

Es wurde verschiedentlich versucht, den Namen Meppen herzuleiten.

Eine Erklärung führt den Namen Meppen auf das altsächsische Wort Mappe oder Meppe zurück, das Mund und davon abgeleitet auch Mündung bedeutet haben soll. Da bis zum Mittelalter die Hase in drei Armen in die Ems mündete, lag die dortige Ansiedlung „an den Mündungen“. In einer in lateinischer Sprache abgefassten Urkunde vom 30. Mai 946, mit welcher König Otto der Große dem Kloster Corvey für Meppen Markt- und Bannrechte verlieh, ist von Meppiun die Rede. Dies kann im Altsächsischen als Dativ Plural des oben genannten Meppe aufgefasst werden und würde dann (Ort an) den Mündungen bedeuten.[7][8]

Eine andere Erklärung leitet den Namen Meppen von Mepelte ab, einer alten niederdeutschen Bezeichnung für den Feldahorn, der im Siedlungsgebiet heimisch gewesen sein könnte.[9]

Spätestens seit dem 13. Jahrhundert wird in Urkunden und auf Karten durchgängig der Name Meppen gebraucht.

Der Ort Meppen (Illinois) in den USA wurde nach Meppen benannt.[10]
Historische Daten

Erste urkundliche Erwähnung fand Meppen im Jahre 834 in einer Schenkungsurkunde von Kaiser Ludwig dem Frommen, in der die Missionszelle Meppen dem Kloster Corvey übertragen wurde. 945 verlieh Otto der Große Meppen Münz- und Zollrecht sowie 946 Marktrechte. Gräfin Jutta von Vechta-Ravensberg verkaufte 1252 ihre Besitzungen an den Bischof von Münster, Meppen wurde Teil des Niederstifts Münster. Als Ministerialen verwalteten die Herren von Meppen und nach ihrem Absterben ab 1392 die Herren von Langen den Ort.
Festung Meppen im 16. Jahrhundert

1360 wurde Meppen durch den Bischof Adolf von Münster das Recht zur Stadtbefestigung verliehen und somit das Stadtrecht. Bis 1660 wurde Meppen zur Festungsstadt ausgebaut. 1762, gegen Ende des Siebenjährigen Krieges, wurden die Festungsanlagen geschleift, der Gegenwall blieb bis heute erhalten. 1803 wurde das Amt Meppen zusammen mit dem Vest Recklinghausen auf Grund der Beschlüsse des Reichsdeputationshauptschlusses dem Herzog von Arenberg als Ersatz für den Verlust seiner linksrheinischen Gebiete zugeteilt. Meppen wurde Hauptstadt des Herzogtums Arenberg-Meppen. Seit 1811 gehörte Meppen als Teil des Département de l’Ems-Supérieur zum französischen Kaiserreich und war Hauptort eines Kantons.

Von 1813 bis 1814 war Meppen preußisch besetzt. Das Herzogtum Arenberg-Meppen wurde 1814/15 durch die Beschlüsse auf dem Wiener Kongress dem Königreich Hannover zugeteilt. Mit der Eröffnung der Hannoverschen Westbahn erhielt Meppen 1855 Anschluss an das Eisenbahnnetz. Nach dem Deutschen Krieg wurde das Königreich Hannover 1866 von Preußen annektiert und damit zu einer preußischen Provinz. Der Kreis Meppen wurde am 1. April 1885 aus den ehemaligen hannoverschen Ämtern Meppen und Haselünne gebildet. Das Land Preußen wurde nach dem Zweiten Weltkrieg 1946 aufgelöst, Meppen gehörte nun zum neu geschaffenen Land Niedersachsen. Die Gemeinde Vormeppen und die Stadt Meppen schlossen sich 1967 zur Stadt Meppen zusammen. Im Zuge der Gebietsreform am 1. März 1974 kamen 13 Gemeinden nach Meppen. Bei der niedersächsischen Kreisreform am 1. August 1977 wurden die damaligen Landkreise Lingen, Meppen und Aschendorf-Hümmling zum Landkreis Emsland vereinigt und Meppen Sitz der Kreisverwaltung.

Sofort nach der Machtergreifung Hitlers wurde durch den NSDAP-Kreisleiter Josef Egert versucht, den Bürgermeister Heinrich Lesker abzusetzen. Am 7. April 1933 besetzte ein Trupp der örtlichen SA das Rathaus und erklärte Lesker für abgesetzt, dieses wurde jedoch vom Osnabrücker Regierungspräsidenten Bernhard Eggers nicht akzeptiert, so dass Lesker zunächst noch im Amt blieb. Am 19. Juni ließ sich Josef Egers zum Ehrenbürgermeister wählen, um das Amt nach dem offiziellen Ausscheiden Leskers in 1935 zu übernehmen, jedoch blieb auch dieses für ihn erfolglos, da diese Option der Stadt zu teuer war und Eggers auch diesem Vorgang nicht zustimmte. Nach weiteren Provokationen gegen Lesker seitens der Nationalsozialisten, wie der Entfernung des Ludwig-Windthorst-Denkmals vom Marktplatz, wurde er mit dem Gesetz zur Wiederherstellung des Berufsbeamtentums am 18. November 1933 entlassen. Jedoch wurde nicht Josef Egert als Bürgermeister ernannt, sondern kommissarisch der Regierungsrat Max Bontemps eingesetzt. Am 31. Januar 1934 wurde Hans Kraneburg als Bürgermeister für die NSDAP eingesetzt.[11]

Auf dem Gebiet der heutigen Stadt Meppen befanden sich in der NS-Zeit die Emslandlager IX Versen und X Fullen.
Kriegsende 1945

Die Stadt Meppen wurde in der Endphase des Zweiten Weltkrieges nicht kampflos an die Alliierten übergeben, so dass es in der Stadt zu schweren Kämpfen kam.

Am 6. April 1945 setzten kanadische Pioniere den Kanalübergang bei der Kirchbrücke in Schöninghsdorf instand, welche zuvor von der Wehrmacht zerstört worden war, und rückten dann mit Panzerspähwagen über die Provinzialstraße nach Klein- und Groß Fullen vor. Dort kam es zu ersten Feuergefechten, bevor die Lager Versen und Fullen befreit wurden. Auf dem Schullendamm vor der zerstörten Emsbrücke wurden die Kanadier von Wehrmachtssoldaten unter starken Beschuss genommen, welche sich an der Marktstiege und beim Nagelshof verschanzt hatten.

Am 7. April gelang es den Kanadiern zwar, an anderer Stelle über Rühlermoor, Rühlerfeld und Rühle nach Esterfeld vorzurücken, jedoch gingen die Gefechte auf dem Schullendamm weiter, und letztendlich wurde die Gustav-Adolf-Kirche zerstört sowie die Propsteikirche St. Vitus schwer beschädigt. Auch in Esterfeld kam es zeitgleich zu erneuten Gefechten, als deutsche Soldaten damit begannen, die vorgerückten Kanadier unter Beschuss zu nehmen.

Nach einem weiteren von Straßenkämpfen geprägten Tag wurde Meppen schließlich am 8. April durch kanadische Verbände eingenommen.[12]
Einwohnerentwicklung

Einwohnerentwicklung einschließlich der bis 1974 eingemeindeten Gemeinden:
Einwohnerentwicklung Meppens zwischen 1821 und 2016
Jahr[13][14][15] 	Einwohner
1821 	4815
1848 	5130
1871 	5085
1885 	6268
1905 	7687
	
Jahr 	Einwohner
1925 	9645
1933 	11.745
1939 	15.045
1946 	17.173
1950 	19.141
	
Jahr 	Einwohner
1956 	20.965
1961 	22.914
1971 	27.305
1975 	27.308
1980 	28.135
	
Jahr 	Einwohner
1985 	28.888
1990 	30.508
1995 	32.093
2000 	33.412
2005 	34.196
	
Jahr 	Einwohner
2010 	34.944
2015 	34.918
2016 	34.935
2017 	35.267
Politik
Ratswahl 2021[16]
Wahlbeteiligung: 57,49 % (2016: 57,09 %)
 %
50
40
30
20
10
0
41,90 %
21,26 %
12,58 %
14,42 %
4,42 %
2,94 %
CDU
SPD
UWG
Grüne
FDP
AfD
Gewinne und Verluste
im Vergleich zu 2016
 %p
   8
   6
   4
   2
   0
  -2
  -4
−2,68 %p
−2,90 %p
−2,87 %p
+6,02 %p
−0,10 %p
+2,94 %p
CDU
SPD
UWG
Grüne
FDP
AfD

Meppen hat den Status einer selbständigen Gemeinde und ist seit 1977 die Kreisstadt des damals flächenmäßig größten deutschen Landkreises, des Landkreises Emsland.
Rat

Der Rat der Stadt Meppen hat 38 gewählte Mitglieder. Hinzu kommt der direkt gewählte hauptamtliche Bürgermeister. Ihm gehören seit der Kommunalwahl am 12. September 2021 Ratsfrauen und Ratsherren von fünf Parteien und einer Wählergemeinschaft an.
Partei/Liste 	Sitze 	Veränderung
CDU 	16 	− 1
SPD 	8 	− 1
UWG 	5 	− 1
Grüne 	6 	+ 3
FDP 	2 	± 0
AfD 	1 	+ 1
Bürgermeister

Hauptamtlicher Bürgermeister der Stadt Meppen ist seit 2014 Helmut Knurbein (parteilos). Bei der letzten Bürgermeisterwahl 2021 wurde Knurbein mit 79,21 Prozent der Stimmen im ersten Wahlgang gegen Marius Nürenberg (Die Partei) wiedergewählt. Die Wahlbeteiligung lag bei 57,5 Prozent.[17]

Hauptamtliche Bürgermeister:

    2001–2006: Heinz Jansen (CDU)
    2006–2014: Jan Erik Bohling (CDU)
    seit 2014: Helmut Knurbein (parteilos)

Bis 2001 bestand eine zweigleisige Verwaltungsspitze in der Stadt mit einem ehrenamtlichen Bürgermeister und einem Stadtdirektor:

Ehrenamtliche Bürgermeister:

    1929–1933 Heinrich Lesker (Zentrum)[18]
    1933–1944 Max Bontemps (kommissarisch)
    1934–1945 Hans Kraneburg (NSDAP)[11]
    1946: Hermann Kerckhoff (CDU)
    1946–1947: Arnold Blanke
    1948–1956: Wilhelm Sagemüller (CDU)
    1956–1967: Arnold Blanke
    1975–1988: Hans Plate
    1988–1994: Wilhelm Mevenkamp
    1994–1996: Karin Stief-Kreihe (SPD)
    1996–2001: Heinz Jansen (CDU)

Stadtdirektoren:

    1946–1964: Hans Kraneburg
    1964–1989: Hans Simon
    1989–2001: Franz Quatmann[19]

Wappen
Meppens Wappen

Meppen kam im 13. Jahrhundert zum Hochstift Münster. Das Meppener Wappen ist aus dem ursprünglichen Münsteraner Wappen abgeleitet. Dieses ursprüngliche Wappen ist ein gold-rot-goldenes Balkenwappen, das in seiner Originalform heute noch von der Stadt Werne und dem Bistum Münster geführt wird. Im Gegensatz zu diesem ist dem Meppener Wappen zusätzlich ein rotes Kreuz auf dem Mittelbalken zugefügt worden.
Städtepartnerschaften

Wappen Ostrolekas Ostrołęka (Polen), seit September 1994
Kultur und Sehenswürdigkeiten
Siehe auch: Liste der Baudenkmale in Meppen
Theater

Zwischen September und April bietet die Theatergemeinde Meppen ein umfangreiches Programm an. Die Aufführungen finden in dem von Eberhard Kulenkampff entworfenen und 1959 fertiggestellten Theater- und Konzertsaal der Stadt Meppen statt, welcher auch dem Windthorst-Gymnasium als Aula dient. Geboten werden dabei Sprechtheater mit Tourneeproduktionen und Musikveranstaltungen unterschiedlicher Genres.

Von Mai bis September bietet die Emsländische Freilichtbühne Meppen den Besuchern jeweils ein Familienmusical und ein Abendstück, meist aus dem Bereich Musical. Die über 30.000 Besucher, die jährlich in den Esterfelder Forst in die Naturbühne kommen, dürfen große Ausstattungsstücke mit bis zu hundert Beteiligten aus dem Bereich Musiktheater erwarten.
Museen

    Stadtmuseum Meppen an der Koppelschleuse
    Arenberg’sche Rentei in der Obergerichtsstraße, erbaut von August Reinking, ehemaliges Stadtmuseum, das durch den Heimatverein Meppen betreut wurde
    Ausstellungszentrum für die Archäologie des Emslandes im Kunstzentrum an der Koppelschleuse[20]

    Theater Meppen
    Theater Meppen
    Kunstzentrum an der Koppelschleuse
    Kunstzentrum an der Koppelschleuse
    Pause einer Aufführung auf der Emsländischen Freilichtbühne
    Pause einer Aufführung auf der Emsländischen Freilichtbühne

Shantychor

Mit regelmäßigen Veranstaltungen in der Region und deutschlandweit ist der in Meppen ansässige Shantychor Geeste e. V. unter der Leitung von Peter Ludewig aktiv.[21]
Bauwerke

    Um 1461/62 wurde die Propsteikirche St. Vitus als dreischiffige spätgotische Hallenkirche errichtet. Während es im Umkreis nur hölzerne Kirchenbauten gab, stand an dieser Stelle schon im 9. Jahrhundert ein einfacher steinerner Vorgängerbau. Dieser wurde im 11. Jahrhundert erweitert, unter anderem entstand so der Kern des heutigen Turms. Beim Ausbau im 13. Jahrhundert entstand unter anderem das Braut- und das Nordportal der Kirche.
    Die „Residenz“, heutiger Sitz der Verwaltung und des Rektorates des Windhorstgymnasiums, wurde zwischen 1726 und 1729 erbaut. Später wurde die Gymnasialkirche (1743–46) unter Pater Superior Karl Immendorf an die Residenz angebaut.

Rathaus Meppen

    Das Rathaus, heute Wahrzeichen der Stadt, wurde 1408 aus Findlingen gebaut. 1601 bis 1605 wurde es erheblich erweitert und um ein in Backstein ausgeführtes Geschoss erhöht. Um die Grundfläche für die oberen Stockwerke zu vergrößern, wurde dem Bau eine offene Bogenhalle vorgelegt. Der von halbkreisförmigen Aufsätzen versehene Stufengiebel lehnt sich stark an münsteraner Vorbilder an („Rothenburg 44“ von 1583 und Krameramtshaus von 1589). Zu Beginn des 19. Jahrhunderts scheint das Gebäude recht baufällig gewesen zu sein, da der arenbergische Baudirektor Josef Niehaus von der Stadt um ein Gutachten zu seiner Erneuerung gebeten wurde. Er empfahl unter anderem, den maroden Turm abzubrechen und die Zierrate des Giebels abzunehmen, jedoch kam es dazu zunächst nicht. 1885 wurden die Aufsätze schließlich abgenommen und die Giebelspitze mit einem schlichten Dreiecksgiebel versehen. Außerdem musste die Haube des seitlichen, erst 1611 hinzugefügten Treppenturmes wegen Baufälligkeit abgetragen werden. 1909 wurde beschlossen, Turm und Giebel in der noch heute vorhandenen Form zu rekonstruieren. Im Inneren befindet sich ein 1605 bezeichneter Sandsteinkamin.
    Das Zeughaus wurde im Jahr 1752 auf dem ehemaligen Standort der abgetragenen Paulsburg, einem 1374 erbauten Drostensitz, im Auftrag von Kurfürst Clemens August errichtet. Es sollte den in der Festung Meppen diensttuenden Soldaten als Lagerraum für Waffen, Munition, Uniformen und Kriegsgerät dienen. Im 19. Jahrhundert wurde das Bauwerk zwischenzeitlich gewerblich und heute als Wohnhaus genutzt. Es ist nach einigen baulichen Veränderungen bis heute erhalten geblieben.
    Die Geschichte der „Herrenmühle“, einer Wassermühle an der Nordradde gelegen, geht bis ins 16. Jahrhundert zurück. Sie wird heute für kulturelle Veranstaltungen genutzt.
    Wohnbauten. Im Gegensatz zu dem nur wenige Kilometer entfernten Lingen weist die Innenstadt von Meppen kaum noch historische Bausubstanz auf. Das Straßenbild wird heute vor allem von verklinkerten Neubauten und einzelnen Backsteinbauten des 19. Jahrhunderts geprägt. Von überregionaler Bedeutung ist die „Arenbergische Rentei“ in der Obergerichtsstraße. Der zweigeschossige klassizistische Bau mit Pilastergliederung und Mansarddach wurde 1805 von August Reinking für den Großkaufmann Ferdinand Frye und seiner Ehefrau Josefine Mulert als Wohnhaus errichtet. Ab 1835 als Rentei genutzt, dient er heute als Stadtmuseum. Vier Jahre später entstand nach den Plänen desselben Architekten das so genannte Heyl’sche Haus in der Emsstraße. Bauherr war der herzoglich-arenbergische Kammerrat Anton Heyl. Während das eigentliche Wohnhaus 1977 zugunsten eines Bankgebäudes abgebrochen wurde, konnte der anschließende Saalbau mit seiner bemerkenswerten Ausstattung erhalten und restauriert werden. Neben dem maßstabsprengenden Bankhaus wirkt er allerdings recht verloren. Das 1816 vom Arzt Nikolaus Vagedes erbaute Stadthaus unweit des Rathauses beherbergt seit 1936 die Stadtverwaltung. Zu den wenigen erhaltenen Fachwerkbauten gehören die eingeschossigen Traufenhäuser „Kuhstraße 24“ und „Im Sack 12“. Erstgenanntes stammt im Kern noch aus dem 16. Jahrhundert und ist damit eines der ältesten Wohngebäude der Stadt. Es wurde mehrfach erweitert und verlängert. „Im Sack 12“ entstand hingegen erst 1797 und verfügt noch über ein Dielentor. Heute sind hier die Büros der Seniorenzeitung und der Senioren Freiwilligen-Agentur untergebracht.
    Das „Meppener Högerhaus“, 1936–1937 erbautes, ehemaliges Verwaltungsgebäude des Landkreises Meppen, wurde vom Architekten Fritz Höger entworfen. Heute befindet sich in dem zweiflügeligen, massiven Ziegelbau mit Walmdach an der Bahnhofstraße eine Polizeidienststelle. Die Eingangstreppe an der Süd-West-Front wird von einem Bogengang dominiert.
    Die „Koppelschleuse“ zwischen 1826 und 1830 gebaut, ist in ihrem ursprünglichen Zustand als Teil des ehemaligen Ems-Hase-Kanals erhalten geblieben.
    Die „Höltingmühle“, eine Holländerwindmühle, wurde vermutlich 1639 in der Nähe von Bockhorn im Landkreis Friesland erbaut. Die Mühle wurde durch den Hölting-Bürgerschützenverein gekauft und aus Anlass des 600-jährigen Stadtjubiläums in den Jahren 1959/60 auf der Landzunge zwischen dem Dortmund-Ems-Kanal und der Hase wieder errichtet. Im Inneren der Mühle befindet sich heute ein Café, das während der Sommermonate an Wochenenden geöffnet hat. In der Mühle finden auch standesamtliche Trauungen statt.
    Auf dem 131 Meter hohen Kühlturm des (inzwischen stillgelegten) Gaskraftwerkes Meppen-Hüntel ist die laut Guinness-Buch der Rekorde „größte Weltkarte der Welt“ aufgemalt. Gestaltet wurde diese Bemalung vom Schweizer Künstler Christoph Rihs.

    Hochaltar der Propsteikirche St. Vitus
    Hochaltar der Propsteikirche St. Vitus
    Gymnasialkirche und Residenz
    Gymnasialkirche und Residenz
    Rathaus Meppen (SW-Ansicht)
    Rathaus Meppen (SW-Ansicht)
    Stadtverwaltung am Markt
    Stadtverwaltung am Markt
    Arenbergische Rentei (Stadtmuseum)
    Arenbergische Rentei (Stadtmuseum)
    Högerhaus
    Högerhaus
    Höltingmühle an der Hasemündung
    Höltingmühle an der Hasemündung
    Herrenmühle an der Nordradde
    Herrenmühle an der Nordradde
    Stadtwall (ehemalige Kontreescarpe)
    Stadtwall (ehemalige Kontreescarpe)
    Gaskraftwerk Hüntel mit Weltkarte
    Gaskraftwerk Hüntel mit Weltkarte

Parks

Die ehemalige Kontreeskarpe der Festung Meppen ist erhalten geblieben und bildet heute eine von alten Bäumen gesäumte, „Stadtwall“ genannte Promenade um die Altstadt. Zwischen dieser und dem Dortmund-Ems-Kanal befindet sich die Schülerwiese, ehemals eine Anlage für den Schulsport. Heute wird die Schülerwiese regelmäßig für Veranstaltungen genutzt.
Naturdenkmäler
„Borkener Paradies“

Im Ortsteil Borken befindet sich das Naturschutzgebiet „Borkener Paradies“, eine historische Huteweide.
Sport
Sportvereine
Emslandstadion im Mai 2017

    SV Meppen: Die Herrenmannschaft des SV Meppen war von der Saison 1987/88 bis 1997/98 in der 2. Fußball-Bundesliga vertreten, damals war sie eine Art Symbol für einen besonders abgelegenen, kleinen und provinziellen Standort des deutschen Profifußballs. Heute dagegen gibt es noch wesentlich kleinere Städte mit Profifußball. In der Saison 2023/24 spielt die Mannschaft in der 3. Fußball-Liga.

Die Frauenmannschaft des SV Meppen spielte seit der Saison 2020/21 in der Frauen-Bundesliga, im Sommer 2023 stieg das Team in die 2. Frauen-Bundesliga ab.

    Mitgliederstärkster Sportverein ist der SV Union Meppen, dessen Volleyballabteilung 1994 die deutsche Meisterschaft in der E-Jugend erringen konnte. Die erste Fußballmannschaft der Frauen qualifizierte sich 2014, 2015 und 2016 für den DFB-Pokal der Frauen.
    DLRG OG Meppen e. V.
    Bridge-Treff Meppen
    Turnverein Meppen
    Leichtathletik-Verein Meppen
    Schwimm-Club Meppen
    Behindertensportgemeinschaft Meppen
    Boxring Meppen
    Karateverein Meppen
    Ju-Jutsu-Kampfsportverein Meppen
    Squash-Club Meppen
    Tennis-Club Meppen
    Wassersportverein Meppen
    Kanuclub Meppen
    Schachklub Meppen

Sportanlagen

    Leichtathletikstadion Helter Damm
    Hänsch-Arena
    Waldstadion Esterfeld
    Freisportanlage Versener Straße
    Skateanlage
    Frei- und Hallenbad Meppen
    Badesee am Schlagbrückener Weg
    Bogenschießplatz
    Tennisanlage am Stadtforst
    Tennisanlage am Schullendamm
    mehrere kleinere und größere Sporthallen

Inklusion

2021 bewarb sich die Stadt als Host Town für die Gestaltung eines viertägigen Programms für eine internationale Delegation der Special Olympics World Summer Games 2023 in Berlin. 2022 wurde sie als Gastgeberin für Special Olympics St. Lucia ausgewählt.[22] Damit wurde sie Teil des größten kommunalen Inklusionsprojekts in der Geschichte der Bundesrepublik mit mehr als 200 Host Towns.[23]
Regelmäßige kulturelle Veranstaltungen
Weihnachtsmarkt mit überdachter Eislaufbahn

    Die Kreuztracht, eine Karfreitagsprozession, seit dem Jahr 1647[24]
    Mittelaltermarkt, Anfang Mai
    Rock unter Linden, Festival als Abschlussfestival der Meppener Gymnasien
    Sommerkirmes
    Meppener Jazz- und Bluesnacht, am ersten Freitag im August
    Stadtfest, am ersten Septemberwochenende
    Herbstkirmes im Oktober
    Weihnachtsmarkt
    Freilichtbühne Meppen
    Meppener Musicalnacht
    Kleinstadtfest (Jugendkulturfestival)

Wirtschaft und Infrastruktur
Wirtschaft

Als städtischer Mittelpunkt war Meppen Verwaltungs- und Handelsstadt mit Ausstrahlung auf die Umgebung. Zu den Behörden traten im 19. Jahrhundert auch eine seinerzeit wichtige Eisenhütte, die bis heute besteht[25], um zunächst das Raseneisenerz[26] in der Umgebung verarbeiten zu können. Hinzu kam der Schießplatz der Firma Krupp sowie Eisenbahn- und Wasserbaubehörden.
Fußgängerzone Bahnhofstraße – Zustand vor Erneuerung und Errichtung der Einkaufspassage MEP
Fußgängerzone Bahnhofstraße – Zustand nach Errichtung der Einkaufspassage MEP, 2018
Diamant des Einkaufszentrums MEP, vom Dortmund-Ems-Kanal aus fotografiert, 2013

Am größten ist heute der Dienstleistungssektor. Hier sind Einzelhandel, Verwaltung und Gesundheitswesen, zunehmend auch Informationstechnologie und Tourismus von Bedeutung. Das ortsansässige Logistikunternehmen Lanfer Logistik ist deutschlandweit aktiv und zählt zu den größten Tanklogistik-Dienstleistern Deutschlands. Im produzierenden Gewerbe sind zu nennen Betriebe des Elektro- und Maschinenbaus (z. B. Hedelius Maschinenfabrik), der Holz-, Erdöl- und chemischen Industrie sowie der Kunststoffverarbeitung und das Handwerk. In der Peripherie liegen landwirtschaftliche Betriebe.
Beschäftigte

Die Anzahl der sozialversicherungspflichtig Beschäftigten in Meppen ist von 1980 bis 2012 um 77,5 Prozent von 9085 auf 16.124 gestiegen. Der Tabelle ist zu entnehmen, dass diese Entwicklung im Wesentlichen gleichgerichtet verlaufen ist mit derjenigen im Landkreis Emsland (Anstieg um 73,9 Prozent). In Niedersachsen ist die Beschäftigtenzahl in dieser Zeit lediglich um 19,2 Prozent gestiegen:
Sozialversicherungspflichtig Beschäftigte[27] 	1980 	1985 	1990 	1995 	2000 	2005 	2010 	2012
Anzahl 	9085 	9228 	10.717 	12.302 	13.416 	13.362 	15.159 	16.124
Index Stadt Meppen 	100,0 	101,6 	118,0 	135,4 	147,7 	147,1 	166,9 	177,5
Index Landkreis Emsland 	100,0 	99,4 	114,3 	130,0 	138,1 	137,2 	161,6 	173,9
Index Land Niedersachsen 	100,0 	94,8 	104,8 	109,9 	111,7 	105,7 	112,6 	119,2

In der Beschäftigungsstruktur nach Wirtschaftsbereichen dominiert der Dienstleistungssektor. Hier sind über die Hälfte der Beschäftigten tätig. Die Tabelle mit den prozentualen Anteilen der sozialversicherungspflichtig Beschäftigten zeigt zum Vergleich auch die entsprechenden Werte für den Landkreis Emsland und für das Bundesland Niedersachsen (Stand: 30. Juni 2012):
Wirtschaftsbereich[28] 	Stadt Meppen 	Landkreis Emsland 	Land Niedersachsen
Land-, Forst und Fischereiwirtschaft 	1,1 	1,5 	1,3
produzierendes Gewerbe 	23,9 	43,2 	31,0
Handel, Verkehr und Lagerei, Gastgewerbe 	23,8 	20,8 	23,1
sonstige Dienstleistungen 	51,2 	34,4 	44,6
  davon: Erbringung von Unternehmensdienstleistungen 	13,7 	12,5 	17,5
  davon: öffentliche und private Dienstleistungen 	37,4 	21,9 	27,1

Daten zur Arbeitslosigkeit werden für die Stadt Meppen selbst nicht erhoben. Der Bereich der Geschäftsstelle Meppen der Agentur für Arbeit Nordhorn umfasst mit Meppen und den umliegenden Gemeinden Twist, Haren (Ems), Dohren, Haselünne, Herzlake, Geeste, Lähden im Wesentlichen das Gebiet des Altkreises Meppen. Hier lag die Arbeitslosenquote im Juni 2013 bei 2,6 Prozent. Sie lag damit um 4 Prozentpunkte unter dem Bundesdurchschnitt.[29]
Verkehr
Ems in Meppen, mit alter Hubbrücke vor 2007
Hasehubbrücke 2022
Siehe auch: Verkehr im Landkreis Emsland
Straße

Meppen kann über die Bundesautobahn A 31, Anschlussstellen Meppen und Twist, sowie die Bundesstraßen B 70 und B 402, einem Teilstück der Europastraße E 233, erreicht werden.
Schienenverkehr

Der Bahnhof Meppen[30] liegt an der 1855 eröffneten Eisenbahnlinie Münster–Emden (Emslandstrecke). In Meppen halten die zweistündlich verkehrenden Intercitys der Linie 35 Koblenz–Norddeich Mole. Außerdem verkehrt stündlich der Emsland-Express RE 15 von Münster nach Emden, welcher seit Dezember 2015 von der Westfalenbahn betrieben wird.[31]
Linie 	Verlauf 	Takt
RE 15 	Emsland-Express:
(Emden Außenhafen –) (nur bei Schiffsverkehr) Emden Hbf – Leer (Ostfriesl) – Papenburg (Ems) – Aschendorf – Dörpen – Lathen – Haren (Ems) – Meppen – Geeste – Lingen (Ems) – Leschede – Salzbergen – Rheine – (Rheine-Mesum –)* Emsdetten – (Reckenfeld –)* Greven (← (Münster Zentrum Nord –)* Münster (Westf) Hbf
* nur einzelne Züge
Stand: Fahrplanwechsel Dezember 2023 	60 min
IC 34 	Norddeich – Emden – Meppen – Lingen (Ems) – Münster (Westf) – Hamm – Unna – Siegen – Wetzlar – Frankfurt am Main 	Ein Zugpaar
IC 35 	Norddeich – Emden – Meppen – Lingen (Ems) – Münster (Westf) – Recklinghausen – Oberhausen – Duisburg – Düsseldorf – Köln – Koblenz (Fr und Sa je ein Zug von Koblenz aus über Mannheim – Karlsruhe – Offenburg nach Konstanz) 	120 min

Neben der von der DB Fernverkehr bzw. Westfalenbahn befahrenen Verbindung gibt es die Strecke der 1894 eröffneten Meppen-Haselünner Eisenbahn (MHE) von Meppen über Haselünne und Herzlake nach Essen (Oldenburg). Heute verkehren hier lediglich Güterzüge und eine Museumsbahn. Der Fahrbetrieb der letzteren wird dabei vom Verein „Eisenbahnfreunde Hasetal e. V.“ organisiert.[32] In den 1920er Jahren gab es Planungen eines grenzüberschreitenden Eisenbahnverkehrs und einen Anschluss an die Bahnstrecke Stadskanaal–Ter Apel Rijksgrens herzustellen. Jedoch verhinderte die Inflation die Verwirklichung des Vorhabens.[33]

Bis Sommer 2015 wurde der Bahnhof modernisiert und barrierefrei umgestaltet.[34]

    Emsländische Eisenbahn
    Emsländische Eisenbahn
    Bahnhof Meppen
    Bahnhof Meppen
    Bahnhof Vormeppen
    Bahnhof Vormeppen
    Lokomotive des Vereins „Eisenbahnfreunde Hasetal e. V.“
    Lokomotive des Vereins „Eisenbahnfreunde Hasetal e. V.“
    Bahnhof Bokeloh der MHE
    Bahnhof Bokeloh der MHE

Busse

Im Stadtverkehr werden von Montag bis Samstag Verbindungen meist im Stundentakt, teilweise auch in kürzeren Intervallen angeboten. Darüber hinaus gibt es regelmäßige Regionalbusverbindungen, unter anderem nach Nordhorn, Sögel, Haselünne, Herzlake und Twist. Zudem gab es grenzüberschreitend eine Linie in die niederländische Großstadt Emmen, welche zum Jahresende 2022 aufgehoben wurde.[35][36] Am Bahnhof Emmen bestand Anschluss an das Eisenbahnnetz der Nederlandse Spoorwegen. Der örtliche Verkehrsverbund für den Busverkehr heißt Busverkehr Emsland-Mitte/Nord. Zentrale Haltestellen sind der Busbahnhof, der Bahnhof und der Windthorstplatz.
Fahrrad

In Meppen wird, wie auch sonst im Emsland und den zu den Niederlanden benachbarten Gebieten, viel Fahrrad gefahren. Genauere Daten liegen nicht vor. Im Gegensatz zu Lingen, Leer oder der Grafschaft Bentheim gibt es in Meppen bisher keine konzeptionellen Ansätze zur Förderung des Radverkehrs.

Durch das Stadtgebiet führen mehrere Radfernwege: Die Dortmund-Ems-Kanal-Route ist ein rund 350 Kilometer langer und nahezu steigungsfreier Radfernweg, der das Ruhrgebiet mit der Nordseeküste verbindet. Der Emsradweg beginnt an der Ems-Quelle in der Ortschaft Schloß Holte-Stukenbrock am Rande des Teutoburger Waldes und folgt dem Fluss über eine Strecke von 375 Kilometern. Die Emsland-Route, ein 300 Kilometer langer Rundkurs zwischen Rheine und Papenburg, kreuzt oder nutzt mehrfach die gleiche Streckenführung wie die Dortmund-Ems-Kanal-Route. Die Hase-Ems-Tour führt entlang der Hase rund 265 Kilometer durch Niedersachsen und Nordrhein-Westfalen über die Mündung der Hase in die Ems bei Meppen bis nach Rheine. Entlang dem Abschnitt zwischen Bersenbrück und Meppen ist in jeder Stadt bzw. Gemeinde ein Kunstwerk aufgestellt. In Meppen steht die Sandsteinskulptur Begegnung von Jutta Klose. Die Kunstwerke werden durch die rund 100 Kilometer lange Hasetaler Kunstroute miteinander verbunden, die mit dem Fahrrad abgefahren werden kann.
Schiffsverkehr
Alter Hafen Meppen – Zustand vor Stilllegung und Abriss

Die Ems ist ab Meppen flussabwärts schiffbar und Teil des Dortmund-Ems-Kanals, flussaufwärts wird sie heute nur noch im Freizeitverkehr befahren. Bereits seit 1829 umfährt der Güterverkehr die zahlreichen Mäander der Ems zwischen Lingen und Meppen auf dem Ems-Hase-Kanal, der seit 1899 überwiegend in den Dortmund-Ems-Kanal einbezogen ist.

Etwa einen halben Kilometer nördlich der Stadtgrenze, auf dem Gebiet der Stadt Haren (Ems) wurde 2007 der interkommunale Eurohafen Emsland eröffnet.[37] Diesen rechtsemsischen Stichhafen werden nach dem Ausbau des Dortmund-Ems-Kanals zur Binnenwasserstraße der Klasse V auch Großmotorgüterschiffe anfahren können.[38] Bis 2008 befand sich ein Emshafen in Innenstadtnähe etwa 300 Meter nördlich der Hasemündung. Dieser kleine Parallelhafen am östlichen Flussufer war für Europaschiffe ausgelegt und diente überwiegend dem Schüttgutumschlag.[39]
Medien
Printmedien

    Meppener Tagespost, gehört zum Verlag der Neuen Osnabrücker Zeitung (Kopfblatt), erscheint werktags
    Emsland-Kurier, gehört zum Verlag der Osnabrücker Nachrichten, erscheint mittwochs und sonntags
    Der Meppener, erscheint monatlich

Onlinemedien

    Was los in Meppen?[40]

Hörfunk und Fernsehen

    Ems-Vechte-Welle, ein werbefreies Bürgerradio für das Emsland und die Grafschaft Bentheim
    Krankenhausradio und TV „Studio Ludmilla“ im Krankenhaus Ludmillenstift
    Kirchenfunk der St.-Vitus-Kirche
    Ems-TV, ehemals Emsland-eins, regionaler Internet-Fernsehsender für das Emsland[41]

Gesundheit
Altbau Ludmillenstift

Das Krankenhaus Ludmillenstift Meppen übernimmt als Krankenhaus der Schwerpunktversorgung die Leistungen der stationären medizinischen Bevölkerungsversorgung. Es bietet mit seinen 420 Planbetten jährlich etwa 17.000 stationären sowie etwa 65.000 ambulanten Patienten medizinische Hilfe in 17 Fach- und Belegabteilungen. In Meppen sind zwei Rettungswagen, ein Notfalltransportwagen, zwei Krankentransportwagen und ein Notarzteinsatzfahrzeug des Deutschen Roten Kreuzes stationiert.
Öffentliche Einrichtungen

Meppen ist Sitz der Kreisverwaltung.

Die Wehrtechnische Dienststelle 91 für Waffen und Munition der Bundeswehr, früher Kruppscher Schießplatz, wurde 1877 gegründet. Sie betreibt den Fliegerhorst Meppen.
Bildung
Gymnasien

    Gymnasium Marianum, privates Gymnasium in Trägerschaft des Bistums Osnabrück
    Windthorst-Gymnasium
    Berufliches Gymnasium Wirtschaft, Technik, Sozialpädagogik und Gesundheitspflege

Oberschule

    Kardinal-von-Galen-Schule Meppen

Haupt- und Realschulen

    Anne-Frank-Schule
    Johannesschule

Grundschulen

    Sechs Grundschulen in den zentralen Stadtteilen sowie sieben in den eingemeindeten Ortsteilen Apeldorn, Bokeloh, Groß Fullen, Hemsen, Rühle, Teglingen und Versen

Förderschulen und Tagesbildungsstätte

    Pestalozzischule, Förderschule mit dem Schwerpunkt Lernen
    Helen-Keller-Schule, Förderschule mit dem Schwerpunkt körperliche und motorische Entwicklung
    Jakob-Muth-Schule, Tagesbildungsstätte für Kinder und Jugendliche mit Förderbedarf im Bereich der geistigen Entwicklung

Berufsbildende Schulen

    Berufsbildende Schulen Meppen – Landwirtschaftliche und Hauswirtschaftliche Fachrichtungen
    Berufsbildende Schulen Meppen – Gewerbliche und Kaufmännische Fachrichtungen
    Marienhaus-Schule: Berufsfach-, Fachschulen und Fachoberschulen der Missionsschwestern Mariens
    Schulungszentrum am Krankenhaus Ludmillenstift Meppen: Aus-, Fort- und Weiterbildung für Gesundheitsberufe

Weitere Schulen

    Musikschule des Emslandes[42]
    Kunstschule im Meppener Kunstkreis
    Volkshochschule Meppen
    Deutsche Angestellten-Akademie

Kirchen

Die Einwohner sind überwiegend katholisch.

    katholische Gemeinden
        Propsteikirche St. Vitus, Altstadt
        St. Paulus, Neustadt
        St. Maria zum Frieden, Esterfeld
        St. Franz Xaver, Rühle
        St. Vinzentius, Fullen/Versen
        St. Vitus, Bokeloh
        St. Antonius, Apeldorn
        Kirche der Unbefleckten Empfängnis Mariens, Hemsen
        St. Joseph, Schwefingen
        St. Antonius, Teglingen

    Propsteikirche St. Vitus (Meppen-Altstadt)
    Propsteikirche St. Vitus (Meppen-Altstadt)
    St. Antonius von Padua (Apeldorn)
    St. Antonius von Padua (Apeldorn)
    St. Vitus (Bokeloh)
    St. Vitus (Bokeloh)
    St. Marien (Hemsen)
    St. Marien (Hemsen)
    St. Franz Xaver (Rühle)
    St. Franz Xaver (Rühle)
    Gustav-Adolf-Kirche
    Gustav-Adolf-Kirche


    evangelische Gemeinden
        evangelisch-lutherische Gustav-Adolf-Kirchengemeinde, Neustadt
        evangelisch-lutherische Bethlehem-Kirchengemeinde, Esterfeld
        evangelisch-reformierte Kirchengemeinde, Schönighsdorf
    Freikirchen
        Evangelisch-Freikirchliche Gemeinde, Baptisten

Andere Glaubensgemeinschaften

    Neuapostolische Kirche
    Zeugen Jehovas

Persönlichkeiten
Windthorst-Denkmal Gymnasialkirche Meppen (2022)
Ehrenbürger

    1888: Ludwig Windthorst (1812–1891), Abgeordneter von Meppen im Reichstag und Mitgründer der Deutschen Zentrumspartei
    1913: Wilhelm Anton Riedemann (1832–1920), Pionier der Tankschifffahrt und Mitgründer der Deutsch-Amerikanischen Petroleum-Gesellschaft (DAPG, heute ExxonMobil)
    1919: Engelbert-Maria von Arenberg (1872–1949), neunter Herzog des Hauses Arenberg und Enkel von Herzog Prosper-Ludwig von Arenberg (1785–1861), dem ehemaligen Landesherrn im Herzogtum Arenberg-Meppen
    1950: Wilhelm Berning (1877–1955), von 1914 bis 1955 Bischof von Osnabrück
    1955: Wilhelm Sagemüller (1880–1962), von 1948 bis 1956 Bürgermeister der Stadt Meppen, Aberkennung der Ehrenbürgerschaft durch die Stadt Meppen am 18. September 2014 u. a. wegen der Beteiligung beim Bau der Emslandlager 1933
    1967: Arnold Blanke (1887–1972)[43]

In Meppen geborene Personen

    Johannes Schiphower (1463–nach 1521), Theologe und Historiker
    Theodor von Rheden (1492–1556), Bischof von Lübeck
    Dietrich von Velen (1591–1657), Drost des Emslandes und Gründer von Papenburg
    Dietrich Anton von Velen (1643–1700), Dompropst in Münster
    Levin Schücking (1814–1883), Schriftsteller
    Ferdinand Schöningh (1815–1883), Verleger
    Bernhard von Lepel (1818–1885), preußischer Offizier, Schriftsteller und lebenslanger Freund Theodor Fontanes
    Eduard Schöningh (1823–1900), Pionier der Hochmoorkultivierung, Marineartillerieoffizier und Bürgermeister von Meppen
    Augustus Maria Toebbe (1829–1884), Bischof von Covington, Kentucky, USA
    Wilhelm Anton Riedemann (1832–1920), Pionier der Tankschifffahrt und Mitbegründer der DAPG
    Johannes von Euch (1834–1922), Bischof, apostolischer Vikar von Dänemark (1892–1922)
    Adolf Bödiker (1835–1893), Reichstags- und Landtagsabgeordneter (Zentrum)
    Tonio Bödiker (1843–1907), preußischer Staatsmann und Oberregierungsrat
    Max Sternberg (1856–1930), politisch engagierter Arzt
    Theodor Reismann-Grone (1863–1949), Verleger und Politiker
    Karl Brandi (1868–1946), Historiker
    Maria Heilmann (1887–1969), Lehrerin, Heimatforscherin, Historikerin und Kunsthistorikerin
    August Löning (1889–1966), Politiker
    Walter Többens (1909–1954), Unternehmer
    Franz Bösken (1909–1976), Organologe
    Hermann Friese (1911–1996), Politiker (CDU), Mitglied des Deutschen Bundestages
    Rhabanus Maurus Haacke (1912–1993), Benediktiner und Kirchenhistoriker
    Gerd Zacher (1929–2014), Komponist, Organist und Musikschriftsteller
    Hans Hunfeld (* 1936), Professor für die Didaktik der Englischen Sprache und Literatur
    Alwin Schockemöhle (* 1937), Springreiter
    Wendelin Köster SJ (* 1939), Rektor des Jesuitenkollegs Sankt Georgen
    Hermann Lause (1939–2005), Film- und Theaterschauspieler
    Günter Balders (* 1942), baptistischer Theologe und emeritierter Professor für Kirchengeschichte
    Reinhold Schaffrath (* 1946), Schauspieler, Sänger, Theaterwissenschaftler und Regisseur
    Bernt Jansen (* 1949), Tischtennisspieler
    Hermann Korte (1949–2020), Germanist und Literaturwissenschaftler
    Dieter Kley (* 1950), Bundesrichter a. D.
    Helmut Gels (* 1952), Bürgermeister von Vechta
    Richard Wiese (* 1953), Linguist und Hochschullehrer
    Carolin Philipps (* 1954), Jugendbuchautorin
    Helmut Hoping (* 1956), katholischer Theologe und Professor
    Renate Volbert (* 1957), Psychologin und rechtspsychologische Gutachterin
    Andreas Slominski (* 1959), Künstler
    Markus Löning (* 1960), Politiker
    Christa Frieda Vogel (* 1960), Fotokünstlerin
    Andreas Müller (* 1961), Jugendrichter
    Peter Wenig (* 1961), Journalist
    Alwin Otten (* 1963), zweifacher Ruderweltmeister im Leichtgewicht
    Ludger Abeln (* 1964), Unternehmenssprecher und früherer Fernsehmoderator des NDR
    Vera Brieske (* 1967), Archäologin für Frühgeschichte
    Axel Büring (* 1967), Volleyballtrainer
    Daniel Giese (* 1969/70), neonazistischer Sänger
    Bernd Schlömer (* 1971), Politiker (Piratenpartei; FDP)
    Tobias Böckermann (* 1973), Journalist und Sachbuchautor
    Christian Hüser (* 1973), Kinderliedermacher, Autor
    Holger Wehlage (* 1976), Fußballspieler
    Kerstin de Witt (* 1976), Blockflötistin
    Thomas Bode (* 1977), Rechtswissenschaftler und Hochschullehrer
    Carsten Schlangen (* 1980), Leichtathlet, deutscher Meister 2006/07/09/10, Olympiateilnehmer 2008 und EM-Silbermedaillengewinner 2010
    Thomas Bröker (* 1985), Profifußballspieler
    Jana-Franziska Poll (* 1988), Volleyball-Nationalspielerin
    Maciej Szewczyk (* 1994), polnisch-deutscher Fußballspieler
    Thorben Deters (* 1995), Fußballspieler
    Ted Tattermusch (* 2001), Fußballspieler
    Noah Kruth (* 2003), Fußballtorhüter

Persönlichkeiten, die vor Ort gewirkt haben

    Beringer Altmann (1939–2010), Maler und Grafiker
    Gottfried Wilhelm Bueren (1801–1859), Liederdichter
    Matthias Deymann (1799–1871), Jurist und Politiker
    Johannes Bernhard Diepenbrock (1796–1884), Theologe und Historiker
    Gerhard Henschel (* 1962), Schriftsteller und Übersetzer
    Dodo Freiherr zu Innhausen und Knyphausen (1583–1636), Feldherr im Dreißigjährigen Krieg. Er kam am Beginn der Schlacht bei Haselünne ums Leben. Seine Leiche wurde von Meppen am 4. März 1636 per Schiff die Ems hinab nach Emden überführt und am 3. Mai 1636 in der Jennelter Kirche beigesetzt, wo der kupferne Prunksarg noch heute zu besichtigen ist
    Isaac Lardin von Limbach († 1627), protestantischer Obrist im Dreißigjährigen Krieg, war 1621 bis 1623 Kommandant der Festung Meppen
    Hermann Michel (1935–2015), Spieler-Trainer beim SV Meppen sowie bis 1991 Sportlehrer am Gymnasium Marianum
    Maria Mönch-Tegeder (1903–1980), Dichterin
    Werner Müller (1946–2019), Manager und Politiker und ehemaliger Bundeswirtschaftsminister; Abitur am Windthorst-Gymnasium
    Christian Neidhart (* 1968), Fußballtrainer des SV Meppen zum Zeitpunkt des Aufstiegs in die 3. Liga
    Otto Pankok (1893–1966), Maler und Bildhauer; 1964 Aufenthalt in Meppen, während der NS-Zeit zeitweilig im heutigen Ortsteil Bokeloh lebend
    Theo Paul (* 1953), Generalvikar des Bistums Osnabrück
    Gottlieb Planck (1824–1910), Richter und Politiker; wirkte in den Jahren 1863 bis 1867 als Richter am Obergericht Meppen
    Christoph Rihs (* 1957), Künstler
    Josef Stecker (1916–2008), Jurist und Politiker
    Deniz Undav (* 1996), Fußballspieler
    Arthur Wieferich (1884–1954), Mathematiker

Trivia
Eintrittskarte für das Spiel des SV Meppen gegen den FC Barcelona am 3. August 1982

In Meppen ist auch Luise Koschinsky beheimatet, die vom Kabarettisten Hans Werner Olm dargestellt wird. Die Dreharbeiten für ihre Episoden fanden bisher jedoch nicht in Meppen statt.

Der FC Barcelona war am 3. August 1982 beim SV Meppen zu Gast. Hierbei handelte es sich um das erste Klubspiel von Diego Maradona auf europäischem Boden.[44]
Literatur

    Martin Zeiller: Meppen. In: Matthäus Merian (Hrsg.): Topographia Westphaliae (= Topographia Germaniae. Band 8). 1. Auflage. Matthaeus Merian, Frankfurt am Main 1647, S. 45–46 (Volltext [Wikisource]).
    Hermann Abels: Die Ortsnamen des Emslandes, in ihrer sprachlichen und kulturgeschichtlichen Bedeutung. Ferdinand Schöningh Verlag, Paderborn 1929.
    Johannes Bernhard Diepenbrock: Geschichte des vormaligen münsterschen Amtes Meppen oder des jetzigen hannoverschen Herzogthums Arenberg-Meppen. Münster 1838.
    Ernst Förstemann, Hermann Jellinghaus (Hrsg.): Altdeutsches Namenbuch. Band II, 1 und 2: Ortsnamen. Bonn 1913/1916 (Nachdruck: Bd. II, 2, Hildesheim 1967/1983, ISBN 3-487-01733-4).
    Alexander Geppert: Meppen. Abriß einer Stadtgeschichte. Stadt Meppen, Meppen 1951.
    Hans-Jürgen Häßler (Hrsg.): Ur- und Frühgeschichte in Niedersachsen. Theiss, Stuttgart 1991, ISBN 3-8062-0495-0.
    Heinrich Heeren und Dieter Stockmann: Meppen in alten Ansichten, Band 1. Zaltbommel, 1982.
    Heinrich Heeren: Meppen in alten Ansichten, Band 2. Zaltbommel, 1992.
    Michael Herrmann (Hrsg.): Meppen im Spiegel historischer Quellen. Meppen 2003, ISBN 3-9808550-1-5.
    Carl Knapstein (Hrsg.): Meppen in alter und neuer Zeit 834–1984. Stadt Meppen, Meppen 1983.
    Hans Simon: Meppen 1946–2001 – die Zeit der Stadtdirektoren. Ein Beitrag zur Meppener Stadtentwicklung. Stadt Meppen, Meppen 2007, ISBN 978-3-9808550-3-7.
    Stadt Meppen (Hrsg.): Geschichte der Stadt Meppen. Stadt Meppen, Meppen 2006, ISBN 978-3-9808550-2-0.
    Gerhard Steenken: Die Meppener Eisenhütte – Die Geschichte eines bedeutenden Industriebetriebes von 1859 bis heute. In: Studiengesellschaft für Emsländische Regionalgeschichte (Hrsg.): Emsländische Geschichte. Band 19, Haselünne 2012, ISBN 978-3-9814041-4-2, S. 218–300.
    Anton Timpe: Neues und Altes im Emsland. Osnabrück 1933.
    Hermann Wenker: Meppen und seine Bürger in alter Zeit. 3. Auflage. Gels, Meppen 1978.

Weblinks
Commons: Meppen – Sammlung von Bildern, Videos und Audiodateien
Wikivoyage: Meppen – Reiseführer

    Offizielle Website der Stadt Meppen
    Literatur über Meppen in der Niedersächsischen Bibliographie

Einzelnachweise

Landesamt für Statistik Niedersachsen, LSN-Online Regionaldatenbank, Tabelle A100001G: Fortschreibung des Bevölkerungsstandes, Stand 31. Dezember 2022 (Hilfe dazu).
Hans Heinrich Seedorf: 1.1.1 Allgemeine Landschaftsgliederung. In: Der Landkreis Emsland. Geographie, Geschichte, Gegenwart. Eine Kreisbeschreibung. Meppen 2002, Karte der Naturräume mit Legende, S. 22–23.
Niederschlagsdaten nach Deutschem Wetterdienst, Normalperiode 1961–1990
Hermann-Josef Mammes: Einkaufs-Ufo im Emsland gelandet. Meppener „Diamant“ wird nach 18-monatiger Bauzeit eröffnet – 55 Millionen Euro investiert. In: Meppener Tagespost, Ausgabe vom 15. Mai 2013, S. 7.
Hermann-Josef Mammes: Sorgenkind Bahnhofstraße. Baufällig und marode. In: Meppener Tagespost, Ausgabe vom 7. Januar 2009, S. 15.
Statistisches Bundesamt (Hrsg.): Historisches Gemeindeverzeichnis für die Bundesrepublik Deutschland. Namens-, Grenz- und Schlüsselnummernänderungen bei Gemeinden, Kreisen und Regierungsbezirken vom 27.5.1970 bis 31.12.1982. W. Kohlhammer GmbH, Stuttgart/Mainz 1983, ISBN 3-17-003263-1, S. 257.
Hermann Abels: Zur Abstammung emsländischer Ortsnamen. In: Heimatkalender 1926, Kreis Meppen, Meppen 1926, S. 20.
Alexander Geppert: Meppen. Abriß einer Stadtgeschichte. Stadt Meppen, Meppen 1951, S. 14–15.
Hermann Wenker: Meppen und seine Bürger in alter Zeit. 3. Auflage, Gels, Meppen 1978, S. 9.
Carola Alge: Kleiner Punkt auf der Landkarte sorgt für Staunen. In: Meppener Tagespost vom 24. September 2011, S. 20.
Heinz Kleene: Der Umgang mit dem Nationalsozialismus in einer Kleinstadt. Das Beispiel des ehemaligen Bürgermeisters und späteren Stadtdirektors Dr. Hans Kraneburg aus Meppen. (PDF) In: d-nb.info. Abgerufen am 16. März 2023.
1945 – Einmarsch in den Landkreis Meppen. In: Neue Osnabrücker Zeitung vom 6. April 2015, abgerufen am 20. Oktober 2016.
Gustav Uelschen: Die Bevölkerung in Niedersachsen 1821–1961. Hannover 1966 (für 1821 bis 1961).
Jahrbuch des Emsländischen Heimatbundes. Bd. 20, 1973 (für 1971).
Statistische Erhebung 100 – Bevölkerungsfortschreibung. Landesbetrieb für Statistik und Kommunikationstechnologie Niedersachsen, abgerufen am 26. Mai 2013 (ab 1975).
Stadtratswahl 12.09.2021 – Stadt Meppen. Abgerufen am 27. Januar 2022.
Ergebnis Bürgermeisterwahl 2021. Abgerufen am 24. August 2022.
Christof Haverkamp: Zwei Meppener Bürgermeister und die NS-Zeit. In: noz.de. Neue Osnabrücker Zeitung, 25. November 2015, abgerufen am 16. März 2023.
Hans Simon: Meppen 1946–2001, die Zeit der Stadtdirektoren. Ein Beitrag zur Meppener Stadtentwicklung, hrsg. von der Stadt Meppen. Meppen 2007.
Koppelschleuse. (Memento vom 21. Oktober 2017 im Internet Archive) Meppen-Touismus.
Webseite des Shantychors
Special Olympics: Host Towns. (PDF) Special Olympics, März 2023, abgerufen am 13. Mai 2023.
Host Town Program. Abgerufen am 13. Mai 2023.
Meppener Kreuztracht. Propsteigemeinde St. Vitus.
meppener-eisenhuette.de, abgerufen am 24. Januar 2024.
Geschichte des Meppener Montanwesens
Statistische Erhebung 70A – Beschäftigte und Pendler, ab 1980. Landesbetrieb für Statistik und Kommunikationstechnologie Niedersachsen, abgerufen am 10. Juli 2013.
Statistische Erhebung 70H – Beschäftigte WZ2008(66) ab 2008. Landesbetrieb für Statistik und Kommunikationstechnologie Niedersachsen, abgerufen am 10. Juli 2013.
Arbeitsmarkt in Zahlen: Arbeitsmarktreport Agentur für Arbeit Nordhorn. Bundesagentur für Arbeit, Nürnberg Juni 2013. S. 25.
Stationssteckbrief: Meppen. In: zvbn.de. Abgerufen am 18. Januar 2024.
Lukas Herbers: Westfalenbahn seit Sonntag auf der Emslandstrecke. In: noz.de. 13. Dezember 2015, abgerufen am 18. Januar 2024.
Die Fahrten. Eisenbahnfreunde Hasetal, abgerufen am 18. Januar 2024.
Der Bahnbau Meppen-Ter Apel. Denkschrift der Kreiskommission für den Bahnbau Meppen-Ter Apel mit Stichbahn Fullen-Gross-Hesepe. Selbstverlag der Kreiskommission, Meppen 1920.
Hermann-Josef Mammes: Zehn Millionen Euro für Meppener Bahnhof. In: noz.de. 3. Juli 2015, abgerufen am 18. Januar 2024.
Fahrplan Linie 922 Meppen–Emmen. (PDF; 63 kB) In: levelink.de. Omnibusverkehr Levelink, 2018, archiviert vom Original (nicht mehr online verfügbar) am 21. März 2018; abgerufen am 11. Januar 2024.
Caroline Theinling: Buslinie Meppen–Emmen endet zum Jahreswechsel. In: noz.de. 22. Dezember 2022, abgerufen am 31. März 2023.
Historie. (Memento des Originals vom 4. März 2016 im Internet Archive)  Info: Der Archivlink wurde automatisch eingesetzt und noch nicht geprüft. Bitte prüfe Original- und Archivlink gemäß Anleitung und entferne dann diesen Hinweis. Eurohafen Emsland GmbH, abgerufen am 18. Juli 2013.
Dortmund-Ems-Kanal Nordstrecke – Ausblick. (Memento des Originals vom 4. März 2018 im Internet Archive)  Info: Der Archivlink wurde automatisch eingesetzt und noch nicht geprüft. Bitte prüfe Original- und Archivlink gemäß Anleitung und entferne dann diesen Hinweis. Wasserstraßen-Neubauamt Datteln, abgerufen am 18. Juli 2013.
Holger Keuper: Letztes Frachtschiff gestern entladen. Rückbau des Meppener Emshafens beginnt. In: Meppener Tagespost, Ausgabe vom 31. Mai 2008, S. 17.
Was los in Meppen? Waslos GmbH, abgerufen am 3. Januar 2024.
Wir über uns. EV1.
Musikschule des Emslandes. Abgerufen am 21. Juni 2022.
Ehrenbürger der Stadt Meppen (Memento vom 23. Oktober 2014 im Internet Archive)

    Vor 40 Jahren: Als Maradona mit dem FC Barcelona in Meppen spielte. ndr.de, 3. August 2022, abgerufen am 10. Dezember 2023.

Einklappen
Wappen des Landkreises Emsland
Gemeinden im Landkreis Emsland

Andervenne | Bawinkel | Beesten | Bockhorst | Börger | Breddenberg | Dersum | Dohren | Dörpen | Emsbüren | Esterwegen | Freren | Fresenburg | Geeste | Gersten | Groß Berßen | Handrup | Haren (Ems) | Haselünne | Heede | Herzlake | Hilkenbrook | Hüven | Klein Berßen | Kluse | Lähden | Lahn | Langen | Lathen | Lehe | Lengerich | Lingen (Ems) | Lorup | Lünne | Meppen | Messingen | Neubörger | Neulehe | Niederlangen | Oberlangen | Papenburg | Rastdorf | Renkenberge | Rhede (Ems) | Salzbergen | Schapen | Sögel | Spahnharrenstätte | Spelle | Stavern | Surwold | Sustrum | Thuine | Twist | Vrees | Walchum | Werlte | Werpeloh | Wettrup | Wippingen
Normdaten (Geografikum): GND: 4038685-5 (lobid, OGND) | LCCN: n81125554 | VIAF: 162696538
Kategorien:

    MeppenGemeinde in NiedersachsenOrt im Landkreis EmslandHansestadtEmslandOrt an der EmsKreisstadt in NiedersachsenEhemalige Hauptstadt (Deutschland)Ersterwähnung 834Stadtrechtsverleihung 1360

Navigationsmenü

    Nicht angemeldet
    Diskussionsseite
    Beiträge
    Benutzerkonto erstellen
    Anmelden

    Artikel
    Diskussion

    Lesen
    Bearbeiten
    Quelltext bearbeiten
    Versionsgeschichte

Suche

    Hauptseite
    Themenportale
    Zufälliger Artikel

Mitmachen

    Artikel verbessern
    Neuen Artikel anlegen
    Autorenportal
    Hilfe
    Letzte Änderungen
    Kontakt
    Spenden

Werkzeuge

    Links auf diese Seite
    Änderungen an verlinkten Seiten
    Spezialseiten
    Permanenter Link
    Seiten­­informationen
    Artikel zitieren
    Kurzlink
    QR-Code herunterladen
    Wikidata-Datenobjekt

Drucken/​exportieren

    Als PDF herunterladen
    Druckversion

In anderen Projekten

    Commons
    Wikinews
    Wikivoyage

In anderen Sprachen

    Dansk
    English
    Español
    Français
    Italiano
    Plattdüütsch
    Nederlands
    Русский
    Türkçe

Links bearbeiten

    Diese Seite wurde zuletzt am 5. Februar 2024 um 23:54 Uhr bearbeitet.
    Abrufstatistik · Autoren

    Der Text ist unter der Lizenz „Creative-Commons Namensnennung – Weitergabe unter gleichen Bedingungen“ verfügbar; Informationen zu den Urhebern und zum Lizenzstatus eingebundener Mediendateien (etwa Bilder oder Videos) können im Regelfall durch Anklicken dieser abgerufen werden. Möglicherweise unterliegen die Inhalte jeweils zusätzlichen Bedingungen. Durch die Nutzung dieser Website erklären Sie sich mit den Nutzungsbedingungen und der Datenschutzrichtlinie einverstanden.
    Wikipedia® ist eine eingetragene Marke der Wikimedia Foundation Inc.

    Datenschutz
    Über Wikipedia
    Impressum
    Verhaltenskodex
    Entwickler
    Statistiken
    Stellungnahme zu Cookies
    Mobile Ansicht

    Wikimedia Foundation
    Powered by MediaWiki

"""
print(text)
img: Image = encode_image(Image.open(sys.argv[1]), text)
img.save(sys.argv[3])