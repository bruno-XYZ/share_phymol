#!/usr/bin/python3

import numpy as np, sys, argparse, os
sys.path.insert(0, '../0-2_modules')
import mod_geometry as geo, mod_io as io
# rotation module used from
# https://www.adamsmith.haus/python/answers/how-to-rotate-a-3d-vector-about-an-axis-in-python

parser = argparse.ArgumentParser(
description="""Script to displace molecule for defined operations.
At the moment the turning the molecule around dihedrals and freezing of atoms is possible.""")
parser.add_argument(
    "coorfile",   type=str, 
    help="""File with the coordinates. At the moment only pdb supported.""")
parser.add_argument(
    "operationsfile",   type=str,   
    help="file with labels and operations")
parser.add_argument(
    "-ofilestem",  type=str,   
    help="Name of the outputfile to be produced",default="default")
parser.add_argument(
    "-oformat",    type=str,   
    help="Current supported outputformats are \".xyz\", \".pdb\", and \".com\"."
    "These can be respectively called as \"XYZ\" or \"PDB\" or \"COM\"."
    "\".com\" is the default and requires the option \"-hfile\" for the body" 
    "of the \".com\"-file", default="COM")
parser.add_argument(
    "-bfile",    type=str,   
    help="""Provides the \"body\" of an i.e. Gaussian input-file. 
    Check provided example and manual for further info""", default="")

args= parser.parse_args()
ifile   =args.coorfile    
ostem   =args.ofilestem  
opfile  =args.operationsfile  
opt     =args.oformat     
hfile   =args.bfile
if opt=="COM" and hfile=="":
    quit("Give header file when you choose COM (default) as option, run with -hfor help")

#get extension and determine format to be read
ext=ifile.split(".")[-1]
oform="blank"
if ext=="xyz":
    oform="XYZ"
elif ext=="pdb":
    oform="PDB"
else:
    quit("""The input file does not end with the extension \".xyz\" or \".pdb\". This is
    necessary to get the file format. Please change the extension""")

# Read Coords
coor    =io.read_coor(ifile, oform)
jobs    =io.read_jobs(opfile)

# make directory and get stem of filename
dir_name, ending,stem    = io.dir_make(ifile,"_"+opt.lower(),ostem)
stem=dir_name+"/"+stem

# loop over the individual jobs read in io.read_jobs
for job in jobs:
    tmp_coor=coor.copy()    # Always start with new 
    excluded=[]
    filename=stem+job[0]+"."+opt.lower()
    for operation in job[1]:
        tmp_coor,excluded=geo.run_operation(tmp_coor,operation,excluded)
    io.generate_job_file(filename, hfile, opt, ifile, tmp_coor, excluded)

