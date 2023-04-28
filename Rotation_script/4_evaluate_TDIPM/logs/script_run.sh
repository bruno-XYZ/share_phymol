for i in `ls -d C*/`; do 
    cd $i
        ../../script_evaluate_latex_out.py ${i%/}
    cd ..
done

