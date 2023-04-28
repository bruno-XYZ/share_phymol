#!/usr/bin/python3

import sys
sys.path.insert(0, '../0-2_modules')
import argparse
import mod_opread as oprd
import re
from mod_opread import eline as eline # gives the line of the error occurence

parser = argparse.ArgumentParser(description="""Generate file with operation list from file
with definition of possible operations and values. See manual for further info.""")
parser.add_argument(
    "ifile"   , metavar="inputfile", type=str,   
    help="""inputfile with information about groups and the angles to rotate. The necessary
    formating is described in the manual""")
parser.add_argument(
    "-oname",  metavar="operations_file_name" ,type=str, 
    help="""file name for operations to be written to, the default replaces the extension or
    everything after \"_ang\"[if existant] with the ending \"_op.txt\" """,default='default')
args=parser.parse_args()
ifile=args.ifile
ofile=args.oname

#######################################################################
#----------------------------------------------------------------------

#default name
if ofile=='default':    
    ofile=ifile.split("/")[-1]
    ofile=ofile.split(".")[0]
    ofile=re.split("_ang",ofile)[0]
    ofile+="_op.txt"

# Reading the file, proper operations will be saved in prim_ar and fixations in fix_ar
prim_ar=[] ; fix_ar=[] ; group=[] ; op=[] ; val=[]
write_flag=False ; k=0 ; line_num=1 ; count=-10 ;mode="blank"
with open(ifile,"r") as rd:
    for line in rd:
        # cut comments [!] spaces and linebreaks away
        line    =line.split("!")[0]
        line    =line.strip()
        # empty lines following non-empty lines will lead to saving the value, while empty
        # lines following empty lines are ignored
        # written line switch one write_flag if empty line is encountered and write_flag is
        # switched on then the values are saved and write_flag is switched off
        if line=="":
            count=0
            if write_flag and (group==[] or op==[] or val ==[]):
                    eline(line_num, 
                    "Blank line occured before operation was completly defined")
            elif write_flag:
                if mode=="ROT":
                    prim_ar.append([group,op,val])
                if mode=="FIX":
                    fix_ar.append(group)
            write_flag=False
            group=[] ; op=[] ; val=[]
        # depending on number of lines read since last empty line the line is either saved as
        # the operation group, mode or values
        else:
            write_flag=True
            # to long
            if count>2:
                eline(line_num, 
                "four or more non-empty lines after \"!!\" line (Max three)")
            # group
            elif count==0:
                group   =oprd.fgroup(line,line_num)
            # operation
            elif count==1:
                op,mode =oprd.foperation(line,line_num)
                if mode=="FIX":
                    val=["blank"]
            # values
            elif count==2:
                if mode=="FIX":
                    eline(line_num, 
                    "You gave lines for values but \"FIX\" does not take this,"
                    "leave one line blank!")
                val = oprd.fvalues(line,mode,line_num)
            count+=1
        line_num+=1

    # on end of document read last operation
    if write_flag and (group==[] or op==[] or val ==[]):
        eline(line_num,
        "Blank line occured before operation was completly defined")
    elif write_flag:
        if mode=="FIX":
            fix_ar.append(group)
        elif mode=="ROT":
            prim_ar.append([group,op,val])

step=0
# call an implicit function that permutes through all possible combinations and indicates the
# current value in val_ar
val_ar=[-1 for i in range(len(prim_ar))]
wr=open(ofile,"w")
oprd.fimplicit(val_ar,prim_ar,fix_ar,step,ofile)
    

