#!/usr/bin/python3

import argparse
import os,fnmatch,re
from collections import OrderedDict

par=argparse.ArgumentParser(description='extract transition dipole moments from files')
par.add_argument('stem', metavar='stem', help='stem of files (needed for latex pics)')
args=par.parse_args()

ltx_fl=True
namstr=args.stem

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
ofile+="analysis.tex"

tdipm_str   =" Ground to excited state transition electric dipole moments"
tdpim_str_ter=" Ground to excited state transition velocity dipole moments (Au):"
dipm_str    =" Dipole moment (field-independent basis, Debye):"
norm_str    =" Normal termination of Gaussian"
trs_sta_str =" Excitation energies and oscillator strengths:"
trs_sub_str =" Excited State"
ter_str     =" SavETr:"
#  There are  2185 symmetry adapted basis functions of A   symmetry.

rd_fl=False ; cnt=-1 ; lf_rd=[]; warn_ls=[] 
for lf in logfiles:
    trdipm="default"
    dipm="default"
    normal=False ; rd_trs=False; sec_sw=False; cnt_trs=-420 ; dip_read=False
    tmp=[]; tr_dir=[] ; tdip_rd=False ; LUMO_fl=False ; lumo_cnt=100

    with open(lf,"r") as rd:
       
        for line in rd:
            if LUMO_fl:
                lumo_cnt-=1
                if lumo_cnt<=0:
                    LUMO=line.split()[3]
                    LUMO_fl=False
            if line.startswith(" There are"):
                if re.match(r" There are .* symmetry adapted basis functions of .*",line):
                    LUMO_fl=True
                    lumo_cnt=2

            if line.startswith(tdipm_str):
                tr_ls=[]
                cnt=3
                tdip_rd=True
            if line.startswith(tdpim_str_ter):
                tdip_rd=False
            if tdip_rd:
                cnt-=1
                if cnt<=0:
                    tr_ls.append({
                        "stat"  : [],
                        "delE"  : [],
                        "tdipm" : [],
                        "osc"   : [],
                        "tra"   : []
                    })
                    tr_ls[-cnt]["stat"]=line.split()[0]
                    sub_tr_ls=[]
                    trdipm=line.split()[4]
                    tr_ls[-cnt]["tdipm"]=trdipm

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
                rd_trs=True; sec_sw=False ; cnt_sub=0
            if rd_trs:
                if line.startswith(trs_sub_str):
                    tmp=line.split()
                    tr_ls[cnt_sub]["stat"]   =tmp[2].split(":")[0]
                    tr_ls[cnt_sub]["delE"]   =tmp[4]
                    tr_ls[cnt_sub]["osc"]    =tmp[8].split("=")[-1] 
                    if len(sub_tr_ls)>0:
                        tr_ls[cnt_sub-1]["tra"]=sub_tr_ls
                    sub_tr_ls       =[]
                    sec_sw=False
                    cnt_sub+=1
                if len(line.split())==4:
                    tmp=line.split()
                    if tmp[1]=="->":
                        sub_tr_ls.append([tmp[0],tmp[2],tmp[3]])
                if line.startswith(ter_str):
                    rd_trs=False
                    tr_ls[cnt_sub-1]["tra"]=sub_tr_ls
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
            lf_rd.append([float(dipm),tr_ls,LUMO,lf])


if len(lf_rd)==0:
    quit("No file in this folder could be read, no output reduced")
# sort to have the highest dipm on first place and then sort entries
lf_rd_sort=sorted(lf_rd,key=lambda x:x[0], reverse=True)

for i in range(len(lf_rd_sort)):
    print(lf_rd_sort[i][0],lf_rd_sort[i][-1])

# Get numbers of orbitals occuring in the most dominant transition of the plasmon
# delete duplicates and sort list
monum_ls=[]
for i in range(len(lf_rd_sort[0][1])):
    item=lf_rd_sort[0][1]
    for j in range(len(item)):
        item_sub=item[j]["tra"]
        if j>=0:
            item_sub.sort(key=lambda x: abs(float(x[2])) , reverse=True)
            monum_ls.append(item_sub[0][0]); monum_ls.append(item_sub[0][1])
monum_ls_un=list(OrderedDict.fromkeys(monum_ls))
monum_ls_un.sort(key=lambda x:int(x))
with open(monum_fi, "w") as wr:
    for i in monum_ls_un:
        wr.write(i+" ")

# Make array with all the data to be printed
o_ls=[] ; no_exfi_fl=False
LUMO=int(lf_rd_sort[0][2])
for i in range(len(lf_rd_sort[0][1])):
    o_str={
        "st"    : [],
        "delE"  : [],
        "tdipm" : [],
        "osc"   : [],
        "tra"   : [],
        "cont"  : [],
        "char"  : [],
        "ipic"  : [],
        "fpic"  : []
    }
    h_str={
        "st"    : "Transition",
        "delE"  : "$\\Delta E$",
        "tdipm" : "$\\mu_\\mathrm{tra}$",
        "osc"   : "$f$",
        "tra"   : "Main Char.",
        "cont"  : "MC \%",
        "char"  : "Char.",
        "ipic"  : "MC Orb. init.",
        "fpic"  : "MC Orb. fin.",
    }

    if ltx_fl:
        leng=10
        leng2=30
    else:
        leng=10
    ar=lf_rd_sort[0][1][i]
    stat="stat"
    if ltx_fl:
        o_str["st"]     =[f"$S_0 _bs_rightarrow S__cbl_{ar[stat]}_cbr_ $",leng2]
    else:
        o_str["st"]     =[f"S0->S{ar[stat]}", leng]
    o_str["delE"]   =[ar["delE"],leng]
    o_str["osc"]    =[ar["osc"],leng]
    o_str["tdipm"]  =[ar["tdipm"],leng]
    #for j in range(len(ar["tra"])):
    tot_cont=0.
    for i in ar["tra"]:
        tot_cont+=abs(float(i[2]))
    ar2=ar["tra"][0]
    if ltx_fl:
        lower=int(ar2[0])-LUMO; higher=int(ar2[1])-LUMO-1
        if lower==0:
            lower="L"
        else:
            lower=f"L-{-lower}"
        if higher==0:
            higher="H"
        else:
            higher=f"H+{higher}"
        hstr=[f"${lower} _bs_rightarrow {higher}$",leng2]
        hstr_cont=[f"{abs(float(ar2[2]))/tot_cont*100:.0f}\%",leng]
        pic_i=namstr+"_pics/"+namstr+"_mo"+ar2[0]+".png"
        pic_f=namstr+"_pics/"+namstr+"_mo"+ar2[1]+".png"
        ltx_pic_i=[f"_bs_includegraphics[width=0.13_bs_textwidth]_cbl_{pic_i}_cbr_",leng2]
        ltx_pic_f=[f"_bs_includegraphics[width=0.13_bs_textwidth]_cbl_{pic_f}_cbr_",leng2]
    else:
        hstr=[f"LUMO {ar2[0]}->{ar2[1]} :  {ar2[2]:>{leng}}",25]
    o_str["tra"].append(hstr)
    o_str["cont"].append(hstr_cont)
    o_str["ipic"].append(ltx_pic_i)
    o_str["fpic"].append(ltx_pic_f)
    ex_fi=namstr+"_ex_types.txt"
    if os.path.exists(ex_fi):
        with open(ex_fi) as rd:
            for line in rd:
                if line.split()[0]==ar["stat"]:
                    o_str["char"]=[line.split()[1],leng]
    else:
        no_exfi_fl=True
        o_str["char"]=["t.b.det.",leng]
    o_ls.append(o_str)
if no_exfi_fl:
        print(f"""Add a file named {ex_fi} to classify excitations.
        Every excitation is classified by one line in the file \"X DET\" (for every excitation considered)
        where X is the number of the excitation (i.e. 1 for S1 or T1) and DET the
        classification.""")
    

open(ofile,"w")
def write(ofile,line):
    with open(ofile,"a") as wr:
        wr.write(line)

latex_header="""\\documentclass[9pt]{scrartcl}

\\usepackage{graphicx}
\\usepackage[margin=2cm,a4paper]{geometry}
\\begin{document}
\\begin{tabular}{l|lll|lllcc}
"""
latex_footer="""\\end{tabular}
\\end{document}"""
line=""
write(ofile,latex_header)
for entry in h_str:
    out=h_str[entry]
    for i in [ ["_bs_","\\"] , ["_cbl_","{"] , ["_cbr_","}"] ]:
        out.replace(i[0],i[1])
    line+=out
    if entry!=list(h_str.keys())[-1]:
        line+=" & "
write(ofile,line+"\\\\\\hline\n")
for entry in o_ls:
    line=""
    for col in entry:
        el=entry[col]
        if type(el[0])==list:
            out=el[0]
        else:
            out=el
        for i in [ ["_bs_","\\"] , ["_cbl_","{"] , ["_cbr_","}"] ]:
            out[0]=out[0].replace(i[0],i[1])
        line+=f"{out[0]:<{out[1]}}".replace("_bs_","\\")
        if col!=list(entry.keys())[-1]:
            line+=" & " 
    line+="\\\\\\hline\n"
    write(ofile,line)
write(ofile,latex_footer)


quit()
# Write file
full_fl=False
ltx_fl=True
wr_ls=[]     


if full_fl:
    write(ofile,f"Max dip_m file: {lf_rd_sort[0][2]}\n")
wr_ls.insert(0,header+"\n")
lens=[ len(l) for l in linemin.split("+") if len(l)>2]
if len(warn_ls) and full_fl:
    write(ofile, "!"*os.get_terminal_size().columns+"\n")
    for i in warn_ls:
        write(ofile,f"file {i} did not terminate normal\n")
    write(ofile, "!"*os.get_terminal_size().columns+"\n")
write(ofile,linemin+"\n") 
for wr in wr_ls:
    write(ofile,wr)
#write(ofile,linemin)   #os.get_terminal_size().columns*"-")
