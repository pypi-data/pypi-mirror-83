#!/usr/bin/env python3

from time import sleep
from portfolio import Portfolio
from datetime import datetime
import argparse

def doRefresh(time, country):
    if country == 'MI' or country == 'L':
        whenRefresh = time.weekday() not in [5, 6] and (time.hour >= 18 or time.hour <= 8)
    elif country == 'NY':
        whenRefresh = time.weekday() not in [5, 6] and (time.hour >= 23 or time.hour <= 14)
    else:
        whenRefresh = True
    return whenRefresh

parser = argparse.ArgumentParser(description='Aggiorna il portafoglio per tenere i dati sempre aggiornati.')
parser.add_argument('-f', '--file', type=str, required=False, default='Info.csv', help='Percorso per il file Info.csv del portafoglio')
args = parser.parse_args()

p = Portfolio(args.file)
country = p.portfolioCountries()
print('Starting the program:')
print('Country: ' + country)

OK = False
while True:
    time = datetime.now()
    if doRefresh(time, country):
        if OK is False:
            p = Portfolio(args.file)
            print(f'Portfolio aggiornato ! --> {time.strftime("%A %d %B %Y - %H:%M")}')
            print(p.data.tail(1))
            print("----------------------------------------------------------------------------")
            if country != 'Mix':
                OK = True
    else:
        OK = False
    print(f'{time.strftime("%A %d %B %Y - %H:%M")} Sleeping...')
    sleep(600)
