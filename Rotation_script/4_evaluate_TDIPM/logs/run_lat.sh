for i in `ls -d C*/`; do
    cd $i
        cp *.tex *_tex
        cd *_tex
            xelatex *tex 
        cd ..
    cd ..
done
