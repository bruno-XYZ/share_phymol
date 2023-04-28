from pathlib import Path
import os,re,fnmatch,fnmatch
comtag="!!"

def read_coor(infile,form):
    coor=[]
    if form=="PDB":
        nums=[4,5,6];leng=8
    elif form=="XYZ":
        nums=[1,2,3];leng=4
    else:
        quit("wrong format passed to function read_cor in mod_io")

    with open(infile) as rd:
        for line in rd:
            line_arr=line.split()
            if len(line_arr)==leng:
                a,b,c=line_arr[nums[0]],line_arr[nums[1]], line_arr[nums[2]]
                try:
                    x=float(a);y=float(b);z=float(c)
                    coor.append([x,y,z])
                except:
                    pass
    return coor

def label_fill(thelist): #the list format x,y;z,w
    tmp_ar  =thelist.split(";")
    ret_ar  =[]
    for therange in tmp_ar:
        if len(therange.split("-"))==2:
            bon_down    = therange.split("-")[0]
            bon_up      = therange.split("-")[1]
            ret_ar.extend([ i for i in range(int(bon_down)-1,int(bon_up))])
        else:
            quit(f"""the expression {therange} in the input should contain two elements a,b and 
            look like [...;]a-b[;...]!""")
    return ret_ar

def read_jobs(opfile):
    operations=[]
    jobs=[]
    k=0
    with open(opfile, "r") as rd:
        for line in rd:
            if line.startswith("#") or line=="":
                pass
            elif line.startswith("!"):
                if k>0:
                    jobs.append([jobname,operations])
                    operations=[]
                if len(line.split())==0:
                    jobname="ajn"
                else:
                    jobname=""
                    for i in line.split()[1:]:
                        jobname+=f"_{i}"
                k+=1
            else:
                tmp_ar  =line.split()
                opmod=tmp_ar[0]
                if opmod=="ROT" and len(tmp_ar)==4:
                    opmod='rotate'
                elif opmod=="MIR" and len(tmp_ar)==3:
                    opmod='mirror'
                elif opmod=="FIX" and len(tmp_ar)==2:
                    opmod='exclude'
                else:
                    quit(f"""You gave {opmod} as operation mode, but only ROT, MIR, 
                    and FIX are valid,
                    or you gave not enough argument""")

                tmp_ar[0]=opmod
                tmp_ar[1]   =label_fill(tmp_ar[1])
                if len(tmp_ar)>2:
                    tmp_ar[2]   =[ int(i)-1 for i  in tmp_ar[2].split(",")]
                if len(tmp_ar)==4:
                    tmp_ar[2]=[tmp_ar[2],tmp_ar[3]]
                    tmp_ar.pop()
                operations.append(tmp_ar)
        jobs.append([jobname,operations])
    return jobs
                
def generate_job_file(jobname, hfile, opt, ifile="", coor=[],excluded=[]):
    header_flag=False
    if opt=="PDB":
        printar=[x for x in range(8)]
        mode="w"
    elif opt=="COM":
        printar=[2,3,4,5,6]
        mode="w"
        header_flag=True
    elif opt=="XYZ":
        printar=[2,4,5,6]
        mode="w"
    else:
        print(f"Format problem in job {jobname} set either COM, PDB, or XYZ in script")

    if opt in ["XYZ","PDB"]:
        if not len(coor):
            print(f"No coordinates for {jobname}")
            return 0

    with open(jobname,mode) as wr:
        if header_flag: 
            fstem=Path(jobname).stem
            with open(hfile,"r") as hrd:
                l=0
                for line in hrd:
                    if line.startswith("!"):
                        if l==0:
                            wr.write(f"%chk={fstem}.chk\n")
                        if l==1:
                            wr.write(f"job_{fstem}\n")
                        l+=1
                    else:
                        wr.write(line)
        if len(coor):
            with open(ifile,"r") as rd:
                k=0
                for line in rd:
                    line_arr=line.split()
                    if len(line_arr)==8:
                        for i in range(0,3):
                            line_arr[i+4]="{:.3f}".format(coor[k][i])
                            line_arr[i+4]="{:>8}".format(line_arr[i+4])
                        k+=1
                        line=""
                        line_arr[1]="{:>5}".format(line_arr[1])
                        line_arr[2]="{:>5}".format(line_arr[2])
                        if k in excluded:
                            line_arr[3]=-1
                        else:
                            line_arr[3]=0
                        line_arr[3]="{:>12}".format(line_arr[3])+4*" "
                        line_arr[7]="{:>24}".format(line_arr[7])
                        for i in printar:
                            line+=line_arr[i]
                        line+="\n"
                        wr.write(line)
                    elif opt in ["PDB","XYZ"]:
                        wr.write(line)
        if opt=="COM":
            wr.write("\n")

def read_diheds(dihedfile):
    diheds=[]
    with open(dihedfile,"r") as rd:
        for line in rd:
            line=line.split(comtag)[0]
            if len(line.split())>1:
                quit(f"""the dihedfile has more than one entry in {line}, give format \"a,b,c,d\"
                for the atom labels for one dihedral in every line (\"\!\!\" makes comments)""")
            elif len(line.split())==0:
                pass
            else:
                dihed=line.split(",")
            diheds.append(dihed)
    return(dihed)


def file_make(name,end,ext,dir_name=""):
    if dir_name!="":
        dir_name+="/"
    stem=name.split("/")[-1]
    stem=name.split(".")[0]
    #stem=re.split("_[\-0-9]",stem)[0]

    if os.path.isfile(dir_name+stem+end+ext):
        for i in range(1,100):
            num_ending="_"+str(i)
            if not os.path.isdir(dir_name+stem+end+num_ending+ext):
                end=end+num_ending
                break
    return dir_name+stem+end+ext

def get_stem(ifile,ofile="default"):
    if ofile=="default":
        stem=ifile.split("/")[-1]
        stem=stem.split(".")[0]
        stem=re.split("_[\-0-9]",stem)[0]
    else:
        stem=ofile
    return stem

def dir_make(ifile,dend,ofile="default"):
    
    stem=get_stem(ifile,ofile)

    ending=dend
    if os.path.isdir(stem+dend):
        for i in range(1,100):
            num_ending="_"+str(i)
            if not os.path.isdir(stem+dend+num_ending):
                ending=dend+num_ending
                dir_flag=True
                break
            dir_flag=False
    else:
        dir_flag=True

    if dir_flag:
        os.makedirs(stem+ending)
    else:
        quit(f"""It was not possibe to make the dir with name {dir_name} or {dir_name}_[0-99]""")
    return stem+ending, ending, stem

