#requirements
#  gprpy installed (including "pip3 install .")
#  imagemagick with settings that allow pdf handling, see readme


import os
import argparse
import gprpy.gprpy as gp


def process_gprpy(path_in,path_out):
    mygpr = gp.gprpyProfile()
    print(path_in)
    mygpr.importdata(path_in)
    mygpr.setZeroTime(6e-09)
    mygpr.setVelocity(0.1)
    mygpr.tpowGain(1.0)
    mygpr.tpowGain(0.4)
    #mygpr.cut(15,53)
    #mygpr.truncateY(6)
    mygpr.printProfile('/tmp/gpr_tmp.pdf', color='gray', contrast=2.0, dpi=600)
    #mygpr.printProfile('/tmp/gpr_tmp.pdf', color='gray', contrast=2, yrng=[0,6], xrng=[15.0694,52.9942], dpi=600) 
    print("convert -density 130 /tmp/gpr_tmp.pdf -colorspace RGB "+path_out)
    os.system("convert -density 130 /tmp/gpr_tmp.pdf -colorspace RGB "+path_out)



parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-i", "--input", type=str,
                        help="input location of DZT file")
parser.add_argument("-o", "--output", type=str,
                        help="ouput file name for png image")

args = parser.parse_args()
input = args.input
output = args.output 

process_gprpy(input,output)
