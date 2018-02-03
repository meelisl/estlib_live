import tingbot
from tingbot import *
import websocket
import json
import requests
from time import sleep
import threading


coverURL = 'https://d3njx7zf7layds.cloudfront.net/BookCoverImages/%s.jpg'
checkedIn = 0
checkedOut = 0
visitors = 0
checkout=''
checkin=''

# Set screen brightness
screen.brightness = 75


def sendPong():
    try:
        ws.send('PONG')
        t = threading.Timer(60, sendPong).start()
    except:
        print 'error sending pong'

# Incoming message from server
def on_message(ws, message):
    
    # Parse JSON message
    j = json.loads(message)

    # Increment counter and set checkin message
    t = j['message']
    if t == 'checkin':
        global checkedIn
        checkedIn += 1
        
        global checkin
        checkin=j

    # Increment counter and set checkout message
    if t == 'checkout':
        global checkedOut
        checkedOut += 1
        
        global checkout
        checkout=j
        
    # Get visitor count
    if t == 'visitor':
        global visitors
        visitors =int(j['visitors'])

    # Fill screen
    screen.fill(color='white')
    
    # Draw dark rectangle
    screen.rectangle(xy=(0, 0), size=(screen.width, 128), color=(51, 52, 52))

    # Draw title rectangle
    screen.rectangle(xy=(0, 0), size=(screen.width, 25), color=(53, 126, 212))

    # Draw title text
    screen.text('Estonian Libraries Live', xy=(10,2), align='topleft', font_size=18, color='white')
    
    # Draw checkout, if set
    if len(checkout)>0:
        draw_checkout(checkout)
    
    # Draw checkin, if set
    if len(checkin)>0:
        draw_checkin(checkin)

    # Draw counters
    screen.text('Checked out: %s     Checked in: %s     Visitors: %s' % (checkedOut, checkedIn, visitors), xy=(10, 240), align='bottomleft', color='black', font_size=11, font='fonts/Roboto-Light.ttf')

    # Update screen
    screen.update()

# Draws checkout
def draw_checkout(co):
    
    # Inital value for top
    y = 32
    
    # Draw image frame
    screen.rectangle(xy=(9, y - 1), size=(70, 90), color=(30, 30, 30), align='topleft')

    # Draw book cover image from cloud or show default image
    url = coverURL % (co['isbn'])
    try:
        screen.image(url, xy=(10, y), scale='shrinkToFit', align='topleft', max_width=68, max_height=88, raise_error=True)
    except:
        screen.image('assets/nocover.png', xy=(10, y), scale='fit', align='topleft', max_width=68, max_height=88)
    
    # Draw library name
    screen.text(co['library'], color='white', xy=(90, y), font_size=14, max_lines=1, max_width=screen.width-95, align='topleft', font='fonts/Roboto-Light.ttf')

    # Draw book title
    screen.text(co['title'], color='white', xy=(90, y + 18), font_size=16, max_lines=1, max_width=screen.width-95, align='topleft')

    # Draw book author
    screen.text(co['author'], color=(250, 250, 250), xy=(90, y + 36), font_size=12, max_lines=1, max_width=200, align='topleft', font='fonts/Roboto-Light.ttf')
                
    # Draw gender icon
    screen.image('assets/%s.png' % (co['sex']), xy=(90, y + 50), align='topleft', max_width=40, max_height=40, scale='fill')
    
    # Draw patrons age
    screen.text(co['age'], xy=(140, y + 60), align='topleft', font_size=18, font='fonts/Roboto-Light.ttf', color='white')
    
# Draw checkin
def draw_checkin(ci):
    
    # Initial value for top
    y = 132
    
     # Draw image frame
    screen.rectangle(xy=(9, y - 1), size=(70, 90), color=(30, 30, 30), align='topleft')

    # Draw book cover image from cloud or show default image
    url = coverURL % (ci['isbn'])
    try:
        screen.image(url, xy=(10, y), scale='shrinkToFit', align='topleft', max_width=68, max_height=88, raise_error=True)
    except:
        screen.image('assets/nocover.png', xy=(10, y), scale='fit', align='topleft', max_width=68, max_height=88)

   # Draw library name
    screen.text(ci['library'], color='black', xy=(90, y), font_size=14, max_lines=1, max_width=screen.width-95, align='topleft', font='fonts/Roboto-Light.ttf')

    # Draw book title
    screen.text(ci['title'], color='black', xy=(90, y + 18), font_size=16, max_lines=1, max_width=screen.width-95, align='topleft')

    # Draw book author
    screen.text(ci['author'], color='black', xy=(90, y + 36), font_size=12, max_lines=1, max_width=200, align='topleft', font='fonts/Roboto-Light.ttf')
                
    # Draw gender icon
    screen.image('assets/%s.png' % (ci['sex']), xy=(90, y + 50), align='topleft', max_width=40, max_height=40, scale='fill')
    
    # Draw patrons age
    screen.text(ci['age'], xy=(140, y + 60), align='topleft', font_size=18, font='fonts/Roboto-Light.ttf')


# Websocket error
def on_error(ws, error):
    print 'socket error'

# Websocket closed
def on_close(ws):
    print 'socket closed'
    
def on_open(ws):
    sendPong()
    
# Get local hour in Estonia from webservice
def areLibrariesOpen():
    
    # Get request
    r = requests.get('http://www.raamatukogud.ee/helper.asp?action=hour')
    
    # If status is ok, get hour value
    if r.status_code==200:
        hour=int(r.text)
        if hour<7 or hour>=19:
            return False
        else:
            return True
    else:
        return True

# Show libraries closed message
def showLibrariesClosed():
    
    # Get request
    r = requests.get('http://www.raamatukogud.ee/helper.asp?action=time')
    
    # If status is ok, get local time text and show message for 5 seconds
    if r.status_code==200:
        localTime=r.text
        screen.fill(color='white')
        screen.text(
            'Hello there!\r\nIt is %s in Estonia and all Libraries are closed!\r\nBest time to run this App is from 06:00AM UTC to 05:00PM UTC!' % (localTime),
            align='center', font_size=20, font='fonts/Roboto-Light.ttf', color='black')
        screen.update()
        sleep(5)
        
        # Show message for 2 seconds
        screen.fill(color='white')
        screen.text('See you soon!', color='black', font_size=30)
        screen.update()
        sleep(2)
        
        # Exit app
        quit()
    
# Start listening
def start():
    
    # Draw splash screen for 3 seconds
    screen.image('assets/splash.png')
    screen.update()
    sleep(3)
    
    # Check, if libraries are open
    if areLibrariesOpen():
        screen.fill(color='white')
        screen.text('Waiting for stream', color='black')
        screen.update()
        
        # Start listening
        ws.run_forever()
    else:
        # Show libraries closed message
        showLibrariesClosed()


# Create websocket
websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://live.webriks.ee/lcs/default.ashx",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.on_open=on_open

# Start app
start()



