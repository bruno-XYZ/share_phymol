#!/usr/bin/python3

import sys, os, fnmatch
sys.path.insert(0, sys.path[0]+'/../0-2_modules') # relative path to script location
import mod_geometry as geo, mod_io as io, mod_log as log
import numpy as np
from numpy import subtract as sub
import itertools
import argparse
import re

parser= argparse.ArgumentParser(description='Calculates dihedrals for given script')
parser.add_argument(
    'dihedfile',metavar='dihedral_file', type=str, 
    help="""File with the saved Label numbers of the dihedral angles to be determined.
    Consider the ordering you determined for your calculations in the begining.""")
parser.add_argument(
    '-gaus', action='store_true',
    help="""run calculation with gaussian, bodyfile with option -bodyfile necessary""")
parser.add_argument(
    '-trdipm', action='store_true',
    help="""run follow-up calculation on states with highest DP-moments, bodyfile with option -bodyfile necessary""")
parser.add_argument(
    '-bodyfile',metavar='bodyfile', type=str,\
    help='File containing the structure of an input file',default="")
parser.add_argument(
    '-angtol', metavar='angle_tollerance', type=str, 
    help="""absolute value of difference between to angles to be indetified as the same
    in degree, default value is 1.0""", default=2.0)
parser.add_argument(
    '-engtol', metavar='energy_tollerance', type=str, 
    help="""threshold value for energy difference in Hartree to lowest minimum for runnning 
    follow-up calculations. Default value is 0.005""", default=0.005)
parser.add_argument(
    '-namelfile', metavar='nameoflistfile', type=str,
    help="""Choose name of the listfile, by default it will be name like the first logfile
    trundcated after the first occurence of underscore and a number. Then \"_ang.txt\" is
    appended as ending""",default='default')
parser.add_argument(
    '-dend', metavar='directory_ending', type=str,
    help="""Choose the ending of the directory. The name of the directorie(s) will be the
    log file truncated by the extension and the first occurence of the wilcard \"_[0-9]\".
    By default \"_HL\" is appended or \"_\{your option\}\".
    With both default or chosen value if the folder allready exists \"_\{i\}\" will be
    appenden with i a number not occured yet.""", default="")
parser.add_argument(
    '-oform', metavar='output_format', type=str, choices=["LIST","CSV"],
    help="""Choose either \"CSV\" for comma separated value format to be readable as table or
    \"LIST\" for getting a .txt file. Default is \"LIST\".""", default="LIST")
parser.add_argument(
    '-full', action='store_true', 
    help="""Take option if all values should be put out to calculate. I.e. when not sure if
    structures are the same, though angles are the same""")
args        =parser.parse_args()
dihedfile   =args.dihedfile
ofile       =args.namelfile
gaus        =args.gaus
trdipm      =args.trdipm
bfile       =args.bodyfile
ang_tol     =args.angtol
eng_tol     =args.angtol
dend        =args.dend
oform       =args.oform
full        =args.full


if dend!="":
    dend="_"+dend
if gaus and trdipm:
    quit("""Choose either -gaus or -trdipm (or none), otherwise two different headerfiles would
    have to be provided and running both at the same time does not seem to make to much sense
    either. Contact the author if you think differently.""")

#Get logfiles in present working directory 
dihed_ar =log.read_diheds(dihedfile)
logfiles= [file for file in os.listdir()]
logfiles= fnmatch.filter(logfiles, '*.log*')

if len(logfiles)==0:
    quit("No logfiles could be read in this folder")

# Check if body file provided when option -gaus is chosen
if gaus and not os.path.exists(bfile):
    quit("""Quit do to wrong inpit:\n\
    option -gaus requires an existing bodyfile provided by option -bodyfile""")
# generate filename for list file if not chosen manually
if ofile=="default":
    ofile=logfiles[0].split(".")[0]
    ending=re.split("_[\-0-9]*",ofile)[-1]
    if ending!="":
        ending="_"+ending
    ofile=re.split("_[\-0-9]",ofile)[0]+"_ang"
    ofile_uni=ofile+"_uni"+ending
    if oform=="LIST":
        ofile+=".txt"
        ofile_uni+=".txt"
    if oform=="CSV":
        ofile+=".csv"
        ofile_uni+=".txt"


Evl=[]; Evl=log.read_HL(logfiles)

results=[]
for lfi in logfiles:
    coor,energy     =log.read_coords_log(lfi)
    if coor=="":
        pass # answer printed in function
    else:
        angs=[]
        for ats in dihed_ar:
            d=[coor[int(i)][1] for i in ats]
            ang_tmp=geo.get_dihedral(  sub(d[0],d[1])  ,  sub(d[3],d[2])  , sub(d[2],d[1])  )
            angs.append(geo.rad_to_grad(ang_tmp))

        ang_in=lfi.split(".")[0]
        ang_in=ang_in.split("_")
        ang_in=[ float(x) for x in ang_in if log.checkInt(x) ]
        Eval=[]
        Eval=log.read_HL([lfi])
        results.append([ang_in, angs, energy,Eval,lfi])
# results array contains the information with original angle, current angle and energy as array for
# every file

if len(results)==0:
    quit("no valid file read, quit")
res_sor    =sorted(results, key=lambda x: x[2], reverse=True)

# Get names
res_dir_name,res_ending,res_stem=io.dir_make(logfiles[0],dend+"_results")
ofile=res_dir_name+"/"+ofile
ofile_uni=res_dir_name+"/"+ofile_uni

log.write_logheader(res_sor,ofile,oform) ; log.write_loglist(res_sor,ofile,oform)

uni_res_sor=[] ; uni_res_sor=log.unif(res_sor,ang_tol)

log.write_logheader(uni_res_sor,ofile_uni,oform) ; log.write_loglist(uni_res_sor,ofile_uni,oform)

Evl_sor=[]; Evl_sor=[ res_sor[i][3] for i in range(len(res_sor))]
Evl_sor_dip    =sorted(Evl_sor, key=lambda x: x[-1], reverse=True)
Evl_uni=[]; Evl_uni=[ uni_res_sor[i][3] for i in range(len(uni_res_sor)) ]
Evl_uni_dip    =sorted(Evl_uni, key=lambda x: x[-1], reverse=True)

uni_sw=False; add=""
for Evls in [Evl_sor_dip,Evl_uni_dip]:
    for val in Evls:
        if val[0]!="fail":
            val[5]=val[4]-Evl_sor[-1][4]
    if uni_sw:
        add="_uni"
    HLfile=io.file_make(res_dir_name+"/"+res_stem,"_HL-analysis"+add,".txt")
    log.res_write(Evls,HLfile)
    uni_sw=True

if gaus: # maybe also pass possible formats
    dir_name,ending,stem=io.dir_make(uni_res_sor[0][-1],dend)
    if full:
        vals=res_sor
    else:
        vals=uni_res_sor
    for i in range(len(vals)):
        # does file lie in energy threshold compared to lowest energy value
        if abs(vals[-i-1][2]-vals[-1][2])<=eng_tol:
            # give any appendix to files?
            #num=i # enumerate files and write to bash script?
            log.make_com(vals[-i-1][-1],bfile,dir_name,ending) # i[3] is name of logfile

if trdipm:
    trdipm_tol=0.75
    dir_name,ending,stem=io.dir_make(uni_res_sor[0][-1],dend+"_TD")
    if full:
        vals=Evl_sor_dip
    else:
        vals=Evl_uni_dip
    high_dp=-420; first_sw=False; on_sw=False
    for i in range(len(vals)):
        if vals[i][0]!="fail" and not first_sw:
            high_dp=vals[i][-1]
            first_sw=True
            on_sw=True
        if abs(vals[i][-1]/high_dp)>=trdipm_tol and on_sw:
            # give any appendix to files?
            #num=i # enumerate files and write to bash script?
            jobname=io.file_make(uni_res_sor[i][-1],ending,".com",dir_name)
            io.generate_job_file(jobname = jobname , hfile = bfile, opt = "COM") # i[3] is name of logfile

