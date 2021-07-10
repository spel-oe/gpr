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

GPIO 08 	SDA (I2C)  => Display (displays measurement number)  
GPIO 09 	SCL (I2C)  => Display (displays measurement number)  
GPIO 26		switch to 3.3V, external pull down => activates measurement   
GPIO 17		buzzer  => indicating active measurement  

## usage
start worker.py on startup

## Requirements

- patched nanovna-saver with parameter interface  
	https://github.com/spel-oe/nanovna-saver  
- i2c activated on raspberry  
- pip3 install scikit-rf  

For file transfer:  
- dnsmasq for AP  
- hostapd for AP  
- webserver like apache2 pointing to "out" directory   

Viewing the data  
- GPRPy (optional )  
	https://nsgeophysics.github.io/GPRPy/  
	https://github.com/NSGeophysics/GPRPy  
	       	
## wifi_ap
simple accesspoint using dns-catch all as captive portal for easy data access

