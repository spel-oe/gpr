# gpr

## princible
<pre>
<!-- language: lang-none -->  
               ┌──────────┐    ┌─────────┐    ┌─────────┐  
    ┌──────────┤NanoVNA-  │.s2p│ tdr.py  │.DZT│ viewer: │   
    ▼      ┌──►│(saver)   ├───►│         ├───►│ GPRPy   │   
  ────   ────  │          │    │         │    │         │   
  Ant1  Ant2   └──────────┘    └─────────┘    └─────────┘   
 
</pre>
## interfaces

USB 		NanoVNA

GPIO 08 	SDA (I2C)  
GPIO 09 	SCL (I2C)          
GPIO 26		switch, external pull down  
GPIO 17		buzzer  

## usage
start worker.py on startup

## Requirements

- patched nanovna-saver with parameter interface

	https://github.com/spel-oe/nanovna-saver

- i2c activated at raspberry
   
- pip3 install scikit-rf

- dnsmasq for AP

- hostapd for AP

- GPRPy (optional for viewing the data)  
	https://nsgeophysics.github.io/GPRPy/  
	https://github.com/NSGeophysics/GPRPy  
	       	
## wifi_ap
simple accesspoint using dns-catch all as captive portal for easy data access

