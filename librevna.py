#parse arguments: start, stop, out-folder
#start librevna-gui -p --no-gui => own thread
#scpi/gpib => basic settings
#   start qrg, stop qrg, steps
#   ask for data => write to s2p file
import time
import datetime
from datetime import datetime
from os import path, makedirs


import argparse
import sys

import subprocess
import threading
	
import LibreVNA_class

def vna_output(proc):
    global run_error
    while True:    
        line = proc.stdout.readline()
        print('got line: {0}'.format(line.decode('utf-8')), end='') 
        if (b'not connected' in line) or (b'IndexError:' in line):
            print ("problem stop!")
            run_error = True
        time.sleep(0.01)

def make_filename(dataDir):
    dateString = datetime.now().strftime("%Y%m%d")
    timeString = datetime.now().strftime("%H%M%S-%f")
    fileName = dateString+'-'+timeString

    #dataDir = 'LibreVNA'
    if not path.exists(dataDir):
        makedirs(dataDir)
    touchFileName = dataDir + "/" + fileName + ".s2p"
    
    #touchFileName = fileName + ".s2p"
    return touchFileName


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--output", type=str,
                    help="output location (folder)")
    parser.add_argument("-f", "--start", type=int,
                    help="start frequency in Hz")
    parser.add_argument("-t", "--stop", type=int,
                    help="stop frequency in Hz")
    parser.add_argument("-i", "--infinite", action="store_true",
                    help="infinite saving 2port touchstone files, otherwise once")

    args = parser.parse_args()


    output_path = args.output
    frequency_start = args.start 
    frequency_stop = args.stop 
    if args.infinite:
        infinite = True
    else:
        infinite = False


    proc = subprocess.Popen(['../LibreVNA_old/Software/PC_Application/LibreVNA-GUI', '','--no-gui','-p','9091'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    t = threading.Thread(target=vna_output, args=(proc,))
    t.start()
    time.sleep(3)


    vna=LibreVNA_class.LibreVNA_class()
    vna.init()
    time.sleep(5)
    vna.set_start(frequency_start)
    vna.set_stop(frequency_stop)
    vna.set_points(250)
    
    print("run saver now")
    if infinite:
        print("run infinite")
        while True:
            filename=make_filename(output_path)
            vna.save_s2p_long(filename,"lin")
            print(filename)
            time.sleep(0.5)

    else:
        filename=vna.make_filename()
        vna.save_s2p_long("test.s2p","lin")
        print(filename)

        exit()

main()