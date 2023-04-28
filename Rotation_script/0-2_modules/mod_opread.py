def eline(line_num,er_str="blank"):
    print(f"Error in line {line_num}:")
    if er_str=="blank":
        quit()
    else:
        quit(er_str)

# check if the line is written in the right format and save the line
def fgroup(line,line_num):
    tmp_ran,tmp_int=[],[]
    tmp_ran=line.split(",")
    for i in tmp_ran:
        tmp_int=i.split("-")
        if len(tmp_int)!=2:
            eline(line_num, "Format of the first line after \"!!\" line is a-b[,c-d,...]")
        else:
            try:
                int(tmp_int[0])
                int(tmp_int[1])
            except:
                eline(line_num, 
                "Error in line {line_num}: give integers in format a-b[,c-d,...]")
    return line

# check if line is written in the right format and with possible options, return the operation
# mode and atom indices for dihedral anlge
def foperation(line,line_num):
    tmp_ar=line.split()
    mode=tmp_ar[0]
    if mode=="ROT":
        if len(tmp_ar)!=2:
            quit(f"""Error in line {line_num} option \"ROT\" requires format
            \"ROT a,b,c,d\" """)
        else:
            harr    =tmp_ar[1].split(",")
            if len(harr)!=4:
                eline(line_num)
                quit("Give four values in format \"a,b,c,d\" for dihedral")
            try:
                [int(i) for i in harr]
            except:
                quit(f"Error in line {line_num}:\nGive integers in format \"a,b,c,d\" ")
            tmp_ar=[tmp_ar[0], line.split()[1]]#[int(i) for i in harr] ]
    elif mode=="FIX":
        if len(tmp_ar)!=1:
            eline(line_num)
            quit("option \"FIX\" does not require additional arguments")
        tmp_ar=["blank"]
    return tmp_ar,mode

# save values given in array and return
def fvalues(line,mode,line_num):
    pmflag=False
    tmp_ar=[]
    tmp_ar=line.split()
    if "pm" in tmp_ar:
        pmflag=True
        if len(tmp_ar)!=2:
            eline(line_num)
            quit("You gave \"pm\" but no values, just dont give any values then!")
        tmp_ar=tmp_ar[1].split(",")
    else:
        if len(tmp_ar)!=1:
            eline(line_num)
            quit("Give format \"[pm] val1[,val2,...]\"")
        tmp_ar=tmp_ar[0].split(",")

    tmp_ar=[int(i) for i in tmp_ar if i!="pm"]
    if pmflag:
        tmp_ar+= [ -i for i in tmp_ar]
    return tmp_ar


def write_operation(val_ar,prim_ar,fix_ar,ofile):
    with open(ofile,"a") as wr:
        wr.write("!!")
        for i in range(len(val_ar)):
            wr.write("  "+str(prim_ar[i][2][val_ar[i]]))
        wr.write("\n")
        for i in range(len(prim_ar)):
            j=prim_ar[i]
            if len(j[0])<12:
                length=12
            else:
                length=len(j[0])+3
            wr.write(4*" "+f"{j[1][0]:<8}"+f"{j[0]:<{length}}"+f"{j[1][1]:<16}"+
            f"{str(j[2][val_ar[i]]):>8}" +"\n")
        # Write fix
        wr.write(4*" "+f"{'FIX':<8}")#+f"{i:<16}"+"\n")
        for i in range(len(fix_ar)):
            wr.write(f"{fix_ar[i]}")
            if i<len(fix_ar)-1:
                wr.write(",")
        wr.write("\n")
                
# implict function, makes a step and determines next value, then calls itself again to
# determine the value after (for permutation)
def fimplicit(val_ar,prim_ar,fix_ar,step,ofile):
    step+=1
    for j in range(len(prim_ar[step-1][2])):
        val_ar[step-1]=j
        if step< len(prim_ar):
            val_ar=fimplicit(val_ar,prim_ar,fix_ar,step,ofile)
        else:
            write_operation(val_ar,prim_ar,fix_ar,ofile)
    return val_ar

