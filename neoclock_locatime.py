import board
import neopixel
import pytz
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime as dt

# Set up the main clock face - a ring of 60 LEDs
clockface            = neopixel.NeoPixel(board.D12, 60)
clockface.auto_write = False

# Determine where we're using for sunrise/sunset calculations
city = LocationInfo("London", "England", "Europe/London")
tz   = pytz.timezone(city.timezone)

add = lambda x,y: min(x+y,255)

while True:
    # Turn all the LEDs to dim blue
    clockface.fill((0, 0, 16))

    # Read the current time and date
    curtime = dt.now()

    # Calculate the sunrise and sunset times
    suninfo = sun(city.observer, dt.now(), tzinfo = tz)

    sunrise = suninfo["sunrise"]
    sunset  = suninfo["sunset"]

    # Convert sunrise and sunset to LED numbers
    daystart = int(((sunrise.hour * 60) + sunrise.minute) / 24)
    dayend   = int(((sunset.hour  * 60) + sunset.minute)  / 24)

    # Set the "day" LEDs to dim yellow
    for led in range(daystart, dayend):
        clockface[led] = (4, 4, 0)

    # Get the current time
    curtime = dt.now()

    # M and S are already in LED number format (0-59), but hours need to be converted
    s = curtime.second
    m = curtime.minute
    h = int((curtime.hour * 60.0 + m) / 12)

    # Make sure the hours are in range, including 1 after 1 one before (=59 after)
    h1 =  h     % 60
    h2 = (h+1)  % 60 
    h3 = (h+59) % 60

    # Add the hands on top of the day/night colours = be careful of byte-overflow!
    clockface[h1] = tuple(map(add, clockface[h1], (128,0,0)))
    clockface[h2] = tuple(map(add, clockface[h2], (32,0,0)))
    clockface[h3] = tuple(map(add, clockface[h3], (32,0,0)))

    clockface[m]  = tuple(map(add, clockface[m], (0,128,0)))
    clockface[s]  = tuple(map(add, clockface[s], (0,0,255)))

    # Update the display
    clockface.write()
    