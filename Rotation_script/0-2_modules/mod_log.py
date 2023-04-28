comtag="!!"
import itertools
import numpy as np
import re
from pathlib import Path
import os

def read_diheds(dihedfile):
    diheds=[]
    dih=[]
    with open(dihedfile,"r") as rd:
        for line in rd:
            if line.startswith(comtag):
                pass
            else:
                line=line.split(comtag)[0]
                if len(line.split())>1:
                    quit(f"""the dihedfile has more than one entry in {line}, 
                    give format \"a,b,c,d\"
                    for the atom labels for one dihedral in every line (\"\!\!\" makes comments)""")
                elif len(line.split()[0].strip())==0:
                    pass
                else:
                    dih=line.split(",")
                    for i in range(len(dih)):
                        dih[i]=dih[i].strip()
                    diheds.append(dih)
    if len(diheds)>0:
        return diheds
    else:
        quit("""no valid dihedral given to read (consider format \"a,b,c,d\" with a,b,c,d are
        labels)""")
def checkInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def number(str):
    try:
        int(str)
        return int(str)
    except ValueError:
        try:
            float(str)
            return float(str)
        except ValueError:
            quit("Error, string instead of number read")

def read_coords_log(ifile):
    area_sw=False ; start_sw=False ; ter_sw=False
    tmp_ar=[]
    array=[]
    idstring=" Center     Atomic      Atomic             Coordinates (Angstroms)"
    scfstring=" SCF Done"
    ter_str=" Normal termination of Gaussian"
    scfcount=0
    energy=0.0

    with open(ifile,"r") as rd:
        for line in rd:
            if line.startswith(idstring):
                area_sw=True
                start_sw=False
                tmp_ar=[]
            elif area_sw:
                if checkInt(line.split()[0]):
                    start_sw=True
                    tmp_ar.append(line.split())
                elif start_sw:
                    area_sw=False
            elif line.startswith(scfstring):
                energy=float(line.split()[4])
                scfcount+=1
            elif line.startswith(ter_str):
                ter_sw=True
        if len(tmp_ar)==0:
            print(f"file {ifile} has no coordinates, skipping this file")
            return "",""
        for i,j in itertools.product( range(len(tmp_ar)),range(len(tmp_ar[0])) ):
            tmp_ar[i][j]=number(tmp_ar[i][j])
        for i in range(len(tmp_ar)):
            array.append([  tmp_ar[i][0],np.array([tmp_ar[i][x] for x in [3,4,5] ])  ] )
        
    if not ter_sw:
        print("!"*os.get_terminal_size().columns+
        f"{ifile}: did NOT terminated normally please check!\n"
        +"!"*os.get_terminal_size().columns)

    return array,energy

def wr_csv(fileop, thelist):
    for i in range(len(thelist)):
        fileop.write(thelist[i])  
        if i < len(thelist)-1:
            fileop.write(" , ")

def wr_list(fileop, thelist,leng=10):
    for i in range(len(thelist)):
        fileop.write(f"{thelist[i]:>{leng}}")

def write_logheader(results,ofile,oform):
    with open(ofile, 'w') as wr:
        hd_ar=[]
        ang_in=results[0][0]
        ang_out=results[0][1]
        First=True
        for j in ang_in,ang_out:
            hd_ar=[]
            for i in range(len(j)):
                io="o"
                if First:
                    io="i"
                hd_ar.append(io+"_ang_"+str(i+1))
            if oform=="LIST":
                wr_list(wr,hd_ar)
                if First:
                    wr.write("\n")
                First=False
            elif oform=="CSV":
                wr_csv(wr,hd_ar)
     
        if oform=="LIST":
            wr_list(wr,["Tot.Eng.","Rel.Eng."],15)
        elif oform=="CSV":
            
            wr_csv(wr,["Tot.Eng.","Rel.Eng."])
        wr.write("\n")


def write_loglist(results,ofile,oform):
    open(ofile, 'w').close()    # empty previous file to work in append mode
    write_logheader(results,ofile,oform)
    for res in results:
        ang_in=res[0].copy()
        ang_out=res[1].copy()
        energy=res[2]
        del_eng=energy-results[-1][2]
        with open(ofile,"a") as wr:
            # write input angles 
            # maybe also allow with invalid filenames (supress this error)
            if len(ang_in)>0:
                for i in range(len(ang_in)):
                    ang_in[i]=f"{float(ang_in[i]):.2f}"
                if oform=="LIST":
                    wr.write("!")
                    wr_list(wr,ang_in)
                    wr.write("\n")
                elif oform=="CSV":
                    wr_csv(wr,ang_in)
            else:
                wr.write(f"! filename does not contain angles seperated by \"_\" \n")


            # write resulting angles
            for j in range(len(ang_out)):
                if ang_out[j]<-180.:
                    ang_out[j]+=360.
                elif ang_out[j]>180.:
                    ang_out[j]-=360.
                ang_out[j]=f"{ang_out[j]:.2f}"
            if oform=="LIST":
                wr.write(" ") # to compensate ! in line before
                wr_list(wr,ang_out)
            elif oform=="CSV":
                wr.write(" , ")
                wr_csv(wr,ang_out)
            # write energy
            energy=f"{energy:.6f}" ; del_eng=f"{del_eng:.6f}"
            if oform=="LIST":
                wr_list(wr,[energy,del_eng],15)
                wr.write("\n")
            elif oform=="CSV":
                wr.write(" , ")
                wr_csv(wr,[energy,del_eng])
                wr.write("\n")

def print_same(Loc_same,eng_beg,eng_end,first):
    deng=eng_beg-eng_end
    deng2=deng*2625.5
    if first:
        print("-"*os.get_terminal_size().columns)
    print(f"Same entries: {str(Loc_same[-1]):>3}-{str(Loc_same[0]+1):<3}\t|\t"
                f"Max. Eng_diff in H / kJ/mol: {deng:+.1E} / {deng2:+.1E}")


def unif(res_sor,tol):
    if len(res_sor)==0:
        quit("There are no entries in your sorted list")

    Ls_del=[] ; Loc_same=[] ; fl_indv=True ; first=True
    for i in range(1,len(res_sor)): # only entered if len(res_sor)>0
        same=True
        for j in range(len(res_sor[i][1])):
            ang1=float(res_sor[i][1][j])
            ang2=float(res_sor[i-1][1][j])
            if abs(ang1-ang2)>=tol:
                same=False
        if same:    
            fl_indv=False
            eng_end=res_sor[i][2]
            Loc_same.append(i)
        else:
            fl_indv=True
            eng_beg=res_sor[i][2]
            if Loc_same:
                print_same(Loc_same, eng_beg, eng_end,first)
                first=False
                Ls_del+=Loc_same
                Loc_same=[]
    if Loc_same:
        print_same(Loc_same, eng_beg, eng_end,first)
        Ls_del+=Loc_same

    ls_ret=[]
    for i in range(len(res_sor)):
        if i not in Ls_del:
            ls_ret.append(res_sor[i])

    return ls_ret


def make_dir(logfile,dend):

    dir_stem=logfile.split("/")[-1]
    dir_stem=dir_stem.split(".")[0]
    dir_stem=re.split("_[\-0-9]",dir_stem)[0]

    if dend=="default":
        ending="_HL"
    else:
        ending="_"+dend

    if os.path.isdir(dir_stem+ending):
        for i in range(1,100):
            num_ending=ending+"_"+str(i)
            if not os.path.isdir(dir_stem+num_ending):
                ending=num_ending
                dir_flag=True
                break
            dir_flag=False
    else:
        dir_flag=True

    if dir_flag:
        os.makedirs(dir_stem+ending)
    else:
        quit(f"""It was not possibe to make the dir with name {dir_name} or {dir_name}_[0-99]""")
    return dir_stem+ending,ending


def res_write(Evl,ofile):
    with open(ofile,"w") as wr:
        wr.write("Energy values in Hartree, Dipoles moment in debye\n")
        leng=10
        col_l=12
        mline=""
        sep=" | "
        header_lin=""

        entries=["Homo","Lumo","Del_HL(H)","Del_HL(eV)","Abs. Energy","Del_En","DipM"]
        for i in range(len(entries)):
            header_lin+=f"{entries[i]:^{col_l}}"
            mline+=col_l*"-"
            if i in [3,5]:
                header_lin+=sep
                mline+="-+-"
        wr.write(mline+"\n")
        wr.write(header_lin+"\n")
        wr.write(mline+"\n")
        
        fail_ls=[]; fcnt=1
        for l in Evl:
            if l[0]=="fail":
                fail_ls.append(f"Logfile of {l[1]} failed to read\n")
                f_num=f"*{fcnt}"
                wr.write(f_num + (col_l*4-len(f_num))*" " + sep + col_l*2*" "+ sep + "\n")
                fcnt+=1
            else:
                dig=[5,5,5,4, # HL eng
                    4,6,
                    5]
                tmp=[f"{l[i]:.{dig[i]}f}" for i in range(len(l))]
                for i in range(len(tmp)):
                    wr.write(f"{tmp[i]:>{col_l-2}}  ")
                    if i in [3,5]:
                        wr.write(" | ")
                wr.write("\n")
        wr.write(mline+"\n")
        for i in range(len(fail_ls)):
            wr.write(5*" "+f"*{i+1} {fail_ls[i]}\n")

#################

def read_HL(logfiles):
    HinEV=27.2114
    occstr= " Alpha  occ."
    virstr= " Alpha virt."
    scfstr= " SCF Done"
    dipstr= " Dipole moment"

    sec_fl=False
    occ_fl=False
    dct_fl=False
    Evl=[]
    for lfile in logfiles:
        with open(lfile, "r") as rd:
            for line in rd:
                if line.startswith(occstr):
                    t_homo=line.split()[4]
                    occ_fl=True
                elif line.startswith(virstr):
                    t_lumo=line.split()[4]
                    if occ_fl:
                        if sec_fl:
                            homo=float(t_homo) ; lumo=float(t_lumo)
                        sec_fl=True
                    occ_fl=False

                if line.startswith(dipstr):
                    dip_ct=1
                    dct_fl=True
                elif dct_fl:
                    dip_ct+=-1
                    if dip_ct==0:
                        dipm=float(line.split()[-1])
                        dct_fl=False

                if line.startswith(scfstr):
                    eng=float(line.split()[4])
        leng=40
        try:
            Evl.append([homo,lumo,lumo-homo,(lumo-homo)*HinEV,eng,-420.,dipm])
            string="SUCCESFULL"
        except:
            Evl.append(["fail",lfile,1.E+20])
            string="FAILED"

        if len(lfile)>leng-2:
            leng=len(lfile)+2
        print(f"{lfile:<{leng}}| Homo-Lumo data read {string}")

    if len(Evl)!=1:
        return Evl
    else:
        return Evl[0]
