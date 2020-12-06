# gpr

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

## wifi_ap
simple accesspoint using dns-catch all as captive portal for easy data access

