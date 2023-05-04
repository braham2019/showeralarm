# Shower alarm

My first ever project based on Micropython code. I wanted to tackle two simple household issues in my bathroom:

- Make sure the (teenage) inhabitants don't shower longer than necessary (save water & energy).
- Boost the Renson ventilation to extract moisture/steam quicker.

## How did I do this

The first issues is easy: install a bathroom timer that buzzes when time is up. 
The second one is do-able as the Renson ventilation has a local API that can be addressed to boost the ventilation to max.

## Hardware needed
- Adafruit Magtag (https://www.adafruit.com/product/4800)
- Lithium Ion Polymer Battery - 3.7v 2500mAh (https://www.adafruit.com/product/328)

## Software components (Micropython) used:
- MagTag
- Adafruit requests

## Additional info
- Only variables I use are the location of the API (http) and the shower timer
- Upon boot, it shows Start button & battery info, then waits (until Start pressed) 
- It goes into sleep mode to wake with Timer button showing on the screen
- It lasts at least 4 weeks on the battery (average usage 3 showers a day)
- The buzzer is an awful sound ;-)
- Every hour it wakes itself up & goes back to sleep to update battery info.
- The background is created by using a shower and battery picture in SVG format and putting it on a BMP using The GIMP.
- The font (Milky Coffee) was downloaded from Dafont (https://www.dafont.com/milky-coffee.font)

## To do
- Show battery info in percentage rather than voltage (nice to have, not a must have)

## View of the screen
![image](https://user-images.githubusercontent.com/56874881/236297336-9778e942-afdc-46d6-ad88-7fa116d62baf.png)

![image](https://user-images.githubusercontent.com/56874881/236297417-facdfeac-4e7f-47f5-8b5e-36660251a6e0.png)
