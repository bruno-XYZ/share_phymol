#!/usr/bin/python3

#import argparse
import os,fnmatch,re
from collections import OrderedDict

#par=argparse.ArgumentParser(description='extract transition dipole moments from files')

logfiles= [file for file in os.listdir()]
logfiles= fnmatch.filter(logfiles, '[!.]*.log*')
ofile=logfiles[0]
ofile_h=ofile.split(".log")
ofile_h=ofile_h[0].split("_")
for i in range(len(ofile_h)):
    if re.match('[\-0-9]',ofile_h[i]):
        ofile_h[i]=""
ofile=""
for a in ofile_h:
    if a!="":
        ofile+=a+"_"
monum_fi=ofile+"monum.txt"
ofile+="analysis.txt"

tdipm_str   =" Ground to excited state transition electric dipole moments"
dipm_str    =" Dipole moment (field-independent basis, Debye):"
norm_str    =" Normal termination of Gaussian"
trs_sta_str =" Excitation energies and oscillator strengths:"
trs_sub_str =" Excited State"
ter_str     =" SavETr:"

rd_fl=False ; cnt=-1 ; lf_rd=[]; warn_ls=[] 
for lf in logfiles:
    trdipm="default"
    dipm="default"
    normal=False ; rd_trs=False; sec_sw=False; cnt_trs=-420 ; tr_ls=[] ; dip_read=False
    tmp=[]; tr_dir=[] 

    with open(lf,"r") as rd:
        for line in rd:

            #trdipm
            if line.startswith(tdipm_str):
                cnt=2
            if not cnt:
                trdipm=line.split()[4]
            cnt-=1

            #dipm
            if line.startswith(dipm_str):
                dip_read=True
            else:
                if dip_read:
                    dipm=line.split()[-1]
                    dipm=dipm.split("=")[-1]
                    dip_read=False

            # read transition data
            if line.startswith(trs_sta_str):
                rd_trs=True; sec_sw=False ; tr_ls=[]
            if rd_trs:
                if line.startswith(trs_sub_str):
                    tmp=line.split()
                    tr_ls.append([ [],[] ])
                    tr_ls[-1][0]= [ tmp[4],tmp[8].split("=")[-1] ]
                    sec_sw=False
                if len(line.split())==4:
                    tmp=line.split()
                    if tmp[1]=="->":
                        tr_ls[-1][1].append( [tmp[0],tmp[2],tmp[3]] )
            #if line.strip()=="":
                #    sec_sw=True
                #elif sec_sw and not line.startswith(trs_sub_str):
                #   rd_trs=False
                if line.startswith(ter_str):
                    rd_trs=False
            elif line.startswith(norm_str):
                normal=True

            cnt_trs-=1

        if not normal:
            warn="!"*os.get_terminal_size().columns
            print(f"{warn}\n{lf} did not terminate normal\n{warn}")
            warn_ls.append(lf)
        elif trdipm=="default":
            print(f"Not possible to read TDIPM from {lf}")
        else:
            print(f"{lf} read SUCCESSFULL")
            lf_rd.append([float(dipm),tr_ls,lf])

# sort to have the highest tipm on first place and then sort entries
lf_rd_sort=sorted(lf_rd,key=lambda x:x[0], reverse=True)

for i in lf_rd:
    print(i[0],i[-1])

monum_ls=[]
for i in range(len(lf_rd_sort[0][1])):
    item=lf_rd_sort[0][1][i]
    for j in range(len(item)):
        item_sub=item[j]
        if j>=1:
            item_sub.sort(key=lambda x: abs(float(x[2])) , reverse=True)
            monum_ls.append(item_sub[0][0]); monum_ls.append(item_sub[0][1])
monum_ls_un=list(OrderedDict.fromkeys(monum_ls))
monum_ls_un.sort(key=lambda x:int(x))

o_ls=[]
if len(lf_rd_sort)==0:
    quit("No file in this folder could be read, no output reduced")
for i in range(len(lf_rd_sort[0][1])):
    o_str={
        "st"    : [],
        "delE"  : [],
        "osc"   : [],
        "tra"   : []
    }
    leng=10
    ar=lf_rd_sort[0][1][i]
    o_str["st"]     =[f"S0->S{i+1}",leng]
    o_str["delE"]   =[ar[0][0],leng]
    o_str["osc"]    =[ar[0][1],leng]
    for j in range(len(ar[1])):
        ar2=ar[1][j]
        hstr=[f"{ar2[0]}->{ar2[1]} :  {ar2[2]:>{leng}}",25]
        o_str["tra"].append(hstr)
    o_ls.append(o_str)
    
with open(monum_fi, "w") as wr:
    for i in monum_ls_un:
        wr.write(i+" ")


#for i in range(len(o_ls)):
#    for j in range(len(o_ls[i])):
#        if ol_ls[i][j][0]==list:
#            for l in range(len(ols[i][j])):
#                if a[i][j]
#                ifa[i][j][0]=
#        else:
#            if a[i][j]<=len(ol_ls[i][j][0])-2:
#                a[i][j]=len(ol_ls[i][j][0])+2

open(ofile,"w")

def write(ofile,line):
    with open(ofile,"a") as wr:
        wr.write(line)

# Write file
wr_ls=[]     
for o in o_ls:
    line=""
    hel_ar=[ [o["st"]] , [o["delE"],o["osc"]] , [o["tra"]] ]
    space=" "
    cnt=0 ; con_fl=True
    header=""; h_fl=True
    h_names=["Transition","TDIPM","Osc","Orbitals"] ; i=0 ; header=""
    while con_fl:
        if h_fl:
            header+=" | "
        con_fl=False
        linemin=" +-"
        line+=" | "
        i=0
        for ar in hel_ar:
            for hel in ar:
                if type(hel[0])==list:
                    if cnt<len(hel):
                        line+=f"{hel[cnt][0]:>{hel[cnt][1]}}"
                        linemin+="-"*hel[cnt][1]
                        if h_fl:
                            header+=f"{h_names[i]:^{hel[cnt][1]}}"
                        if cnt<len(hel)-1:
                            con_fl=True
                    else:
                        line+=f"{space:>{hel[0][1]}}" 
                        linemin+="-"*hel[0][1]
                        if h_fl:
                            header+=f"{h_names[i]:^{hel[0][1]}}"
                elif cnt<1:
                    line+=f"{hel[0]:>{hel[1]}}"
                    linemin+="-"*hel[1]
                    if h_fl:
                        header+=f"{h_names[i]:^{hel[1]}}"
                else:
                    line+=f"{space:>{hel[1]}}"
                    linemin+="-"*hel[1]
                i+=1
            if h_fl:
                header+=" |"
            line+=" |"
            linemin+="-+"
        h_fl=False
        if con_fl:
            line+="\n"
        cnt+=1
         
    wr_ls.append(line+"\n"+linemin+"\n")


write(ofile,f"Max dip_m file: {lf_rd_sort[0][2]}\n")
wr_ls.insert(0,header+"\n")
lens=[ len(l) for l in linemin.split("+") if len(l)>2]
if len(warn_ls):
    write(ofile, "!"*os.get_terminal_size().columns+"\n")
    for i in warn_ls:
        write(ofile,f"file {i} did not terminate normal\n")
    write(ofile, "!"*os.get_terminal_size().columns+"\n")
write(ofile,linemin+"\n") 
for wr in wr_ls:
    write(ofile,wr)
#write(ofile,linemin)   #os.get_terminal_size().columns*"-")
