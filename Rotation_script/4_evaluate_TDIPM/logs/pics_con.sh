for i in `ls -d C*/`; do 
    cd $i
        cd *_tex
            #j=$(ls -d *_pics/)
            #cp -r $j ${j%/}_bak
            cd *_pics
                for k in `ls *png`; do 
                    convert -resize 33% -trim -fuzz 1% -transparent white $k $k ; done 
            cd ..
        cd ..
    cd ..
done
