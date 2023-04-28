#/bin/bash

for i in `ls`
do
	if [ $i==*.com* ]
	then
		j=${i%_[${2}]*}
		k=$j${i#$j}
		k=${k%.com}.chk
		cp `ls ${1%/}/$j*chk*` ./$k
		echo "Copied ${k}" 
	fi
done
