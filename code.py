import board
import time
import wifi
import ssl
import alarm
import adafruit_requests as requests
import socketpool
from adafruit_magtag.magtag import MagTag
from secrets import secrets

# Set up variables and board
URL_BOOST = "http://192.168.0.5/v1/api/boost/2"
TIMER_SEC = 210
BACKGROUND_BMP = "/shower_bg3.bmp"

display = board.DISPLAY
# text_group = displayio.Group()
# colors
RED = 0x880000
GREEN = 0x008800
BLUE = 0x000088
YELLOW = 0x884400
CYAN = 0x0088BB
MAGENTA = 0x9900BB
WHITE = 0x888888

# set up alarms to wake from deep sleep
C_alarm = alarm.pin.PinAlarm(pin=board.BUTTON_C, value=False, pull=True)
alarm.sleep_memory[0] = not alarm.sleep_memory[0]
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3600)

# magtag
magtag = MagTag(
    default_bg=BACKGROUND_BMP,
    rotation=180,
)
# Index 0, Start /old
magtag.add_text(
    text_position=(0, 96),
    text_scale=3,
)
# Index 1, Voltage
magtag.add_text(
    text_font="/fonts/MilkyCoffee-24.bdf",
    text_position=((magtag.graphics.display.width // 2) - 1, 273),
    text_scale=1,
    text_anchor_point=(0.5, 0.5),
)
# Index 2, Timer, Start
magtag.add_text(
    text_font="/fonts/MilkyCoffee-36.bdf",
    text_position=(5, 170),
    text_scale=1,
)
# Index 3, Timer_minutes
magtag.add_text(
    text_position=((magtag.graphics.display.width // 2) - 1, 205),
    text_scale=3,
    text_anchor_point=(0.5, 0.5),
)


def boost_ventilation():
    print("Boosting ventilation...")
    https.put(URL_BOOST, json={"enable": True, "level": 200, "timeout": 900})

def get_boost_status():
    resp = magtag.network.fetch(URL_BOOST)
    json_data = resp.json()
    print(json_data)
    return json_data["enable"]

# main program
try:
    # Upon boot, show Start button & battery info, wait x seconds &
    # then go into sleep mode to wake with Timer button
    # voltage = magtag.peripherals.battery / 4.2 * 100
    voltage = round(magtag.peripherals.battery, 2)
    voltage = str(voltage)
    magtag.set_text("< start", 2, auto_refresh=False)
    magtag.set_text("     {}v".format(voltage), index=1, auto_refresh=True)
    t_end = time.time() + 15
    while time.time() < t_end:
        if magtag.peripherals.button_c_pressed:
            # print("Timer button pressed")
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill(CYAN)
            magtag.peripherals.play_tone(1318, 0.25)
            magtag.peripherals.neopixel_disable = True
            # connect_wifi
            print("Connecting to %s" % secrets["ssid"])
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            print("Connected to %s!" % secrets["ssid"])
            print("IP", wifi.radio.ipv4_address)
            socket = socketpool.SocketPool(wifi.radio)
            https = requests.Session(socket, ssl.create_default_context())
            #
            magtag.set_text("  . . . ", 2, auto_refresh=True)
            # Boosting
            boost_ventilation()
            time.sleep(3)
            # Start timer (seconds)
            t = TIMER_SEC
            while t:
                mins, secs = divmod(t, 60)
                timer = "{:02d}:{:02d} ".format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                t -= 1
            # make some noise when timer finishes
            for i in range(3):
                magtag.peripherals.play_tone(2000, 0.8)
                time.sleep(0.8)
    # Clear screen and display Start button
    magtag.set_text("       ", 2, auto_refresh=False)
    # magtag.set_text("       ", 3, auto_refresh=False)
    magtag.set_text("< timer", 2, auto_refresh=True)

except (ValueError, RuntimeError) as e:
    print("Some error occured, retrying! -", e)

# Wait for button press or refresh after 1 hour (to get battery status)
magtag.peripherals.speaker_disable = True
alarm.exit_and_deep_sleep_until_alarms(time_alarm, C_alarm)
# Write your code here :-)
