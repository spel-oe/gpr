import os
import time
import subprocess
import threading


http= True #enables http server
gprpy= True #enable default DZT => PDF => png
rpi= True #enable if running on rPi with oled display, beep, switch
#rpi= False #enable if running on rPi with oled display, beep, switch
if rpi:
    import RPi.GPIO as GPIO
    import display
    import beep

if http:
    from functools import partial
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from pathlib import Path
#if gprpy:
#    import gprpy.gprpy as gp

PIN_run = 26 
global run_state_old 
global run_error 
run_error = False
run_state_old = False
run_state = False
run_id = 0;
path_out = "./out/"
path_vna = "python3 /home/pi/nanovna-saver/nanovna-saver.py" #check if cd needed
path_worker = "./worker/"

#
# => start dispaly worker
# => get & set old id
#
# main detect switch
#
#
# ON
# set new id
# => start nanovna
# => set display worker
# => start beep
#
# OFF
# => stop nanovna
# => set display worker
# => stop beep
# => tdr.py
# 


def gpio_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_run, GPIO.IN)

def gpio_status():
    global run_state_old
    if (run_state_old == False and GPIO.input(PIN_run) == True): #ON
        run_state_old = True
        return 2
    elif (run_state_old == True and not GPIO.input(PIN_run)): #OFF
        run_state_old = False
        return 1
    else: #old state
        return 0
def get_measurement_id():
    #list out, order by name get highest => number, numbber
    elem = os.listdir(path_worker)
    s = len(elem)
    elem_num= []
    if (s > 0):
        for i in elem:
            if not i.isnumeric():
                elem.remove(i)
            else:
                elem_num.append(int(i))
        elem_num.sort()
        if not len(elem_num):
            return 0
        return elem_num[-1]
    else:
        return 0
def vna_output(proc):
    global run_state_old
    global run_error
    while True:    
        line = proc.stdout.readline()
        print('got line: {0}'.format(line.decode('utf-8')), end='') 
        if (b'not connected' in line) or (b'IndexError:' in line):
            print ("problem stop!")
            run_error = True
        if (b'running' in line):
            noise.start()
        if run_state_old == False :
            break
            return
        time.sleep(0.1)
        
def start_http():
    print("serving from out...")
    handler = partial(SimpleHTTPRequestHandler, directory="./out/")
    httpd = HTTPServer(('0.0.0.0', 8080), handler)
    httpd.serve_forever()

if rpi: #see above
    gpio_init()
    #display
    iface = display.display()
    iface.number = run_id
    iface.stop()
    #beep
    noise = beep.beep()
    thread_beep = threading.Thread(target = noise.worker) 
    thread_beep.start()  

run_id = get_measurement_id()
t = 0 #variable for therad
proc = 0 #variable for sub process


if http:

    thread_http = threading.Thread(target = start_http) 
    thread_http.start()  

if not rpi:
    status = 2
started = False
while True:
    if rpi:
        status = gpio_status()
    if (status == 0 and run_error == True):
        #status = 1
        print("error___state")
        #noise.error()
    if (status == 2 and started == False): #start measurement
        #start 
        started = True
        run_error = False
        print('start\n')
        run_id+=1
        if rpi:
            iface.number = run_id
            iface.start()
        # beep 
        #noise.start()
        print( path_worker + str(run_id), path_out)

        proc = subprocess.Popen(['python3', '/home/pi/nanovna-saver/nanovna-saver.py','-f','100000000','-t','1000000000', '-o', path_worker+ str(run_id),'-i'],
        #proc = subprocess.Popen(['python3', 'librevna.py','-f','100000000','-t','1000000000', '-o', path_worker+ str(run_id),'-i'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        t = threading.Thread(target=vna_output, args=(proc,))
        t.start()


    elif(status == 1 and started == True): #finished measurement
        #stop
        started = False
        print('stop_state\n')
        #kill nanovna
        # stop beep
        noise.stop()
        proc.terminate()
        t.join()
        #run_error = True 
        if (not run_error) :
            print("python3 tdr.py -i "+ str(path_worker) + str(run_id) + " -o " + str(path_out) + str(run_id))
            os.system("python3 tdr.py -i "+ str(path_worker) + str(run_id) + " -o " + str(path_out) + str(run_id))
            a = 0
        if gprpy:
            
            os.system("python3 gprpy_img.py -i "+ str(path_out)+str(run_id)+".DZT" + str(path_out)+"images/"+str(run_id)+".png")
            #process_gprpy(str(path_out)+str(run_id)+".DZT",str(path_out)+"images/"+str(run_id)+".png")
        iface.stop()
    if rpi:
        iface.work()
    #if ( run_state_old == True):
        #noise.beep()
    time.sleep(0.1)
