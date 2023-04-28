#!/bin/bash

gcc -Wall code-size_var_M1.c -o program-size_var_M4 -lm
	
if [ $? -eq 0 ]; then
	./program-size_var_M4
	gnuplot ploting_fusion.gnuplot
	
    cd TEX 
	gcc -Wall tex-generator.c -o program-tex -lm -w

	if [ $? -eq 0 ]; then
		./program-tex
		xelatex standalone-size.tex
		xelatex standalone-eng.tex	
		echo success
	else
		echo stoped tex
	fi
    cd -

	echo success
	
else
    echo stoped complete
fi



