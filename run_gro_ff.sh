#!/bin/bash

usage() { echo "Usage: $0 -m [min,nvt,npt,prd] -M [*gro] -S [*gro] -F [*top]" \
1>&2; exit 1; }
while getopts ":m:M:S:F:" o; do
    case "${o}" in
        m)
            mod=${OPTARG}
            if [[ !  " min nvt npt prd ana " =~ " $mod " ]]; then  usage ; fi 
            ;;
        M)
            pos_mol=${OPTARG}
            ;;
        S)
            pos_sol=${OPTARG}
            ;;
        F)
            topol=${OPTARG}
            ;;
        *)
            echo -z
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [[ $mod == "" ]]; then
    echo "provide mod ( min nvt npt prd ana)" ; exit
fi
            
tmp_fol=$MTSC/MD/gmx/temps
tag=MOL
if [[ " $mod " =~ " nvt npt prd " ]] && [[ $topol_temp == "" ]]; then
    echo provide topology file ; exit
elif [[ " $mod " =~ " min " ]] && ( [[ $pos_mol != *.gro ]] || [[ $pos_sol != *.gro ]] || [[
$topol != *.top ]] ); then 
    echo provide '*gro' for mol and solv and '*.top' file ; exit
fi

## File names
    job_nam=$(basename $(pwd) ) 
    boxed=BOX_${job_nam}.gro 
    solvated=SOLV_${job_nam}.gro
    minim=MIN_${job_nam}.tpr
    nvt=NVT_${job_nam}.tpr
    npt=NPT_${job_nam}.tpr
    prd=PRD_${job_nam}.tpr

## Clean folder
    if [ ! -d ARCH ]; then
        mkdir ARCH
    fi
    mv *.[eo][1-9]* *job ARCH &>/dev/null


error_mess () {
    nam=$1
    if grep MPI_ABORT ${nam}.out &> /dev/null; then
        echo -e "\033[0;31m STOP ${nam} did not terminate\033[0m" ; 
        grep "Error \|Fatal error:" ${nam}.out -A 10 ;  exit
    fi
}


#gmx='/usr/local/chem/gromacs-2021.4/bin/gmx_mpi'
gmx=gmx
gmx_run () {
    gmx mdrun -deffnm ${1%.*} &> ${1}.run_out
}

topol_temp=TEMP_${topol}
if [[ $mod == min ]]; then
    cp $topol $topol_temp
    ## Make box
        echo ... making box
        gmx editconf -f $pos_mol -o $boxed -c -d 1.5 -bt cubic &> ${boxed}.out
        error_mess ${boxed}
    ## Solvate
        echo ... make solvated box
        gmx solvate -cp $boxed -cs $pos_sol -o $solvated -p $topol_temp &> ${solvated}.out
        error_mess ${solvated}
    ## Minimize
        echo .. minimize
        cp ${tmp_fol}/minim.mdp .
#   Maxwarn due to non canonical naming C vs C1
        $gmx grompp -f minim.mdp -c ${solvated} -p $topol_temp -o ${minim} -maxwarn 1 \
            &> ${minim}.out
        error_mess ${minim}
        gmx_run ${minim} 

    echo -e "Potential \n 0" | $gmx energy -f ${minim%.*}.edr -o potential.xvg &>potential.out
elif [[ $mod == nvt ]]; then
    cp $tmp_fol/nvt.mdp .
    echo .. nvt
    $gmx grompp -f nvt.mdp -c ${minim%.*}.gro -p $topol_temp -r ${minim%.*}.gro -o ${nvt} &> ${nvt}.out
    error_mess ${nvt}
    gmx_run ${nvt}
    echo -e "Temper \n 0" | $gmx energy -f ${nvt%.*}.edr -o temperature.xvg &>temperature.out
elif [[ $mod == npt ]]; then
    cp $tmp_fol/npt.mdp .
    echo .. npt
    $gmx grompp -f npt.mdp -c ${nvt%.*}.gro -p ${topol_temp} -o ${npt} &> ${npt}.out
    error_mess ${npt}
    gmx_run ${npt}
    echo -e "Pressure \n 0" | $gmx energy -f ${npt%.*}.edr -o pressure.xvg &>pressure.out
elif [[ $mod == prd ]]; then
    cp $tmp_fol/prd.mdp .
    echo .. production
    $gmx grompp -f prd.mdp -c ${npt%.*}.gro -t ${npt%.*}.cpt -p ${topol_temp} -o ${prd} \
    &> ${prd}.out 
    error_mess ${prd}
    gmx mdrun -deffnm ${prd%.*} &> ${prd}.run_out  & 

    PROC=$!
    N=( $(grep nsteps prd.mdp) ) ; N=${N[2]}
    for i in {0..100000}; do
    if kill -0 "$PROC" &>/dev/null; then
        out=( $(grep " Step " -A1 PRD*log | tail -n1) ) ; out=${out[0]}
            part=$( bc <<< "scale=2; 0${out} / 0${N} * 100" )
        echo -ne "${out} of ${N} -> ${part} %\r" ; sleep 10
    else
        echo "JOB Terminated"; break
    fi
    done
    #wait

elif [[ $mod == ana ]]; then
    echo -e "$tag\n$tag\n$tag" | $gmx trjconv -s ${prd%.*}.tpr -f ${prd%.*}.xtc -o ${prd%.*}_mol.xtc \
    -center -fit rot+trans &> ${prd%.*}_mol.xtc.out
    echo -e "$tag\nsystem" | $gmx trjconv -s ${prd%.*}.tpr -f ${prd%.*}.xtc -o ${prd%.*}_sys.xtc -pbc mol -center \
    &> ${prd%.*}_sys.xtc.out
    sed "/cycl/d" ${prd%.*}.gro > ${prd%.*}_mol.gro
    len=$(cat ${prd%.*}_mol.gro | wc -l) ; len=$( echo " ${len} - 3 " | bc )
    echo len $len
    sed -i "2 c\ $len" ${prd%.*}_mol.gro
else
    echo provide valid modes min,nvt,npt,prd ; exit
fi


mv \#* *out *log *pdb *trr ARCH &>/dev/null
