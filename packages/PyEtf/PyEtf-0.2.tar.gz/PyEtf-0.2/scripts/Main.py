#!python
from time import sleep
from portfolio import Portfolio
from datetime import datetime


print('Starting the program:')
OK = False
while True:
    time = datetime.now()
    if time.weekday() not in [5, 6] and (time.hour >= 18 or time.hour <= 8):
        if OK is False:
            p = Portfolio()
            print(f'Portfolio aggiornato ! --> {time.strftime("%A %d %B %Y - %H:%M")}')
            print(p.data.tail(1))
            print("----------------------------------------------------------------------------")
            OK = True
    else:
        OK = False
    print(f'{time.strftime("%A %d %B %Y - %H:%M")} Sleeping...')
    sleep(600)
