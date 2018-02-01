import tingbot
from tingbot import *
import websocket
import json

coverURL = 'https://d3njx7zf7layds.cloudfront.net/BookCoverImages/%s.jpg'
checkedIn = 0
checkedOut = 0


checkout=''
checkin=''

# Set screen brightness
screen.brightness = 75


# Incoming message from server
def on_message(ws, message):
    # Parse JSON message
    j = json.loads(message)

    # Increment counters
    t = j['message']
    if t == 'checkin':
        global checkedIn
        checkedIn += 1
        global checkin
        checkin=j

    if t == 'checkout':
        global checkedOut
        checkedOut += 1
        global checkout
        checkout=j

    # Fill screen
    screen.fill(color='white')
    
    screen.rectangle(xy=(0, 0), size=(screen.width, 128), color=(51, 52, 52))

    # Draw title frame
    screen.rectangle(xy=(0, 0), size=(screen.width, 25), color=(53, 126, 212))

    # Draw title
    screen.text('Estonian Libraries Live', xy=(10,2), align='topleft', font_size=18, color='white')
    
    

    # Draw checkout
    draw_checkout(checkout)
    
    # Draw checkin
    draw_checkin(checkin)

    # Draw counters
    screen.text('Checked out: %s     Checked in: %s' % (checkedOut, checkedIn), xy=(10, 240), align='bottomleft', color='red', font_size=11)

    screen.update()

def draw_checkout(co):
    
    
    y = 32
    
    # Draw image frame
    screen.rectangle(xy=(9, y - 1), size=(70, 90), color=(30, 30, 30), align='topleft')

    # Draw book cover image from cloud or show default image
    url = coverURL % (co['isbn'])
    try:
        screen.image(url, xy=(10, y), scale='shrinkToFit', align='topleft', max_width=68, max_height=88, raise_error=True)
    except:
        screen.image('nocover.png', xy=(10, y), scale='fit', align='topleft', max_width=68, max_height=88)
    
    # Draw library name
    screen.text(co['library'], color='white', xy=(90, y), font_size=14, max_lines=1, max_width=screen.width-95, align='topleft', font='Roboto-Light.ttf')

    # Draw book title
    screen.text(co['title'], color='white', xy=(90, y + 18), font_size=16, max_lines=1, max_width=screen.width-95, align='topleft')

    # Draw book author
    screen.text(co['author'], color=(250, 250, 250), xy=(90, y + 36), font_size=12, max_lines=1, max_width=200, align='topleft', font='Roboto-Light.ttf')
                
    # Draw gender icon
    screen.image('%s.png' % (co['sex']), xy=(90, y + 50), align='topleft', max_width=40, max_height=40, scale='fill')
    
    # Draw patrons age
    screen.text(co['age'], xy=(140, y + 60), align='topleft', font_size=18, font='Roboto-Light.ttf', color='white')
    

def draw_checkin(ci):
    
    y = 132
    
     # Draw image frame
    screen.rectangle(xy=(9, y - 1), size=(70, 90), color=(30, 30, 30), align='topleft')

    # Draw book cover image from cloud or show default image
    url = coverURL % (ci['isbn'])
    try:
        screen.image(url, xy=(10, y), scale='shrinkToFit', align='topleft', max_width=68, max_height=88, raise_error=True)
    except:
        screen.image('nocover.png', xy=(10, y), scale='fit', align='topleft', max_width=68, max_height=88)

   # Draw library name
    screen.text(ci['library'], color='black', xy=(90, y), font_size=14, max_lines=1, max_width=screen.width-95, align='topleft', font='Roboto-Light.ttf')

    # Draw book title
    screen.text(ci['title'], color='black', xy=(90, y + 18), font_size=16, max_lines=1, max_width=screen.width-95, align='topleft')

    # Draw book author
    screen.text(ci['author'], color='black', xy=(90, y + 36), font_size=12, max_lines=1, max_width=200, align='topleft', font='Roboto-Light.ttf')
                
    # Draw gender icon
    screen.image('%s.png' % (ci['sex']), xy=(90, y + 50), align='topleft', max_width=40, max_height=40, scale='fill')
    
    # Draw patrons age
    screen.text(ci['age'], xy=(140, y + 60), align='topleft', font_size=18, font='Roboto-Light.ttf')


# Websocket error
def on_error(ws, error):
    print 'socker error'
    
# Websocket closed
def on_close(ws):
    print 'socket closed'
    
# Start listening
def start():
    ws.run_forever()


# Create websocket
websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://live.webriks.ee/lcs/default.ashx",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Start app    
tingbot.run(start)
