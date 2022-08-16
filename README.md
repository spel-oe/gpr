# gpr
open source ground penetation radar, 

## princible
<pre>
<!-- language: lang-none -->  
               ┌──────────┐    ┌─────────┐    ┌─────────┐  
    ┌──────────┤   VNA    │.s2p│ tdr.py  │.DZT│ viewer: │   
    ▼      ┌──►│(NanoVNA) |───►│         ├───►│ GPRPy   │   
  ────   ────  │          │    │         │    │         │   
  Ant1  Ant2   └──────────┘    └─────────┘    └─────────┘   
 
</pre>
## hardware interfaces
based on RaspberryPi 3 or 4

USB 		NanoVNA

GPIO 08 	SDA (I2C)  => Display (displays measurement number)  
GPIO 09 	SCL (I2C)  => Display (displays measurement number)  
GPIO 26		switch to 3.3V, external pull down => activates measurement   
GPIO 17		buzzer  => indicating active measurement  

## usage
- start worker.py on startup, see config section in worker.py
  - config in worker.py, enable/disable modules
  - set path for patched nanovna-saver, adjust freuqency range
  - if rpi is disabled, start worker.py to start measurement, crtl+c for ending, no automatic postprocessing

## Requirements
- patched nanovna-saver with parameter interface for headless operation 
	https://github.com/spel-oe/nanovna-saver  
- i2c activated on raspberry  
- pip3 install: 
  - numpy 
  - scikit-rf  
- imagemagick for preview image  
     for pdf conversion support: `sudo sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml`

For file transfer:  
- dnsmasq for AP  (dhcp server)
- hostapd for AP  (wifi access point)
- http server - if http is enabled in worker.py, file listing is provided on port 8080

Viewing the data  
- GPRPy (optional )  
	https://nsgeophysics.github.io/GPRPy/  
	https://github.com/NSGeophysics/GPRPy  
- if gprpy is installed and enabled in worker, a preview image is provided in out/images

	       	
## wifi_ap
simple accesspoint using dns-catch all as captive portal for easy data access



## files and directories:
- **documentation/** hardware documentation and example files
- **out/** contains processed input files (.DZT), webserver points here
- **out/images** contains preview images if enabled in worker.py
- **wifi_ap/** example config files for wifi access point 
- **worker/** contains the raw touchstone files one folder each measurement, with ascending number
- **beep.py** lib: triggers beep as metronom during measurements
- **display.py** lib: controls the oled display with font file and oled lib
- **FreeSans.ttf** lib: font for oled display
- **gprpy_img.py** generates preview png-image out of .DZT file (standalone -h for help)
- **lib_oled96.py** lib: for small i2c oled display
- **LibreVNA_Class.py** lib for LibreVNA
- **librevna.py** saves s2p files from librevna _experimental_ (standalone -h for help)
- **README.md** this file
- **tdr.py** converts touchstone (.s2p) files to gpr .DZT file (standalone -h for help)
- **worker.py** script that orchestrates everything
- ****
- ****
- ****
- ****


## TODO
- maybe apply file based calibration for s2p files before tdr.py
- librevna haeadless operation
- example files and pictures



# Hardware 
## Antenna 
Antenna design based on https://www.mdpi.com/1424-8220/19/5/1045/pdf?version=1551428447  
see documentation/antenna (KiCad 6)  

## overall setup

- antennas
  - sma cables, short as possible
- shielding boxes, including absorptive material
- vna, e.g. nanovna v2
- pc, e.g. debian based, RaspberryPi 3, 4 or equivalent, pinout see above
  - oled display (i2c) 0,96'' 128x64 pixel
  - beep, buzzer just supply voltage for beep
  - switch, switching measurement on/off  
- usb power pack > 30Wh


