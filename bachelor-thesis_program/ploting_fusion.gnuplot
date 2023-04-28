set macros
set datafile separator ','
set encoding utf8


set terminal pngcairo size 2000,1000 enhanced font "CMU Bright,50"
set tics font "CMU Bright,60"
set key font "CMU Bright,60"
set label font "CMU Bright,60"

lwidth = 7.5

pack( r, g, b ) = 2**16*r + 2**8*g + b
set style line 1 	linecolor rgb 		pack(240, 	0, 		0) lw lwidth
set style line 2 	linecolor rgb  		pack(240, 	80, 	0) lw lwidth
set style line 3 	linecolor rgb 		pack(240, 	160,	0 ) lw lwidth
set style line 4 	linecolor rgb 		pack(240, 	240, 	0) lw lwidth
set style line 5	linecolor rgb 		pack(160, 	240, 	80) lw lwidth
set style line 6 	linecolor rgb 		pack(80, 	240, 	160) lw lwidth
set style line 7 	linecolor rgb 		pack(0, 	240, 	240) lw lwidth
set style line 8 	linecolor rgb 		pack(0, 	160, 	240) lw lwidth
set style line 9 	linecolor rgb 		pack(0, 	80, 	240) lw lwidth
set style line 10 	linecolor rgb 		pack(0, 	0, 		240) lw lwidth
set style line 11	linecolor rgb 		pack(80, 	0, 		240) lw lwidth
set style line 12	linecolor rgb 		pack(160, 	0, 		240) lw lwidth
set style line 13 	linecolor rgb 		pack(240, 	0, 		240) lw lwidth
set style line 14 	linecolor rgb 		pack(0, 	0, 	160) lw 2




#set lmargin at screen -0.01
set size 1.13,1.07
#set bmargin at screen 0.2
set term pngcairo

	chi="`head -3 	"plot_size-distribution/X-plot_size-distribution_eagg0-ki0__xi0__help.csv" | tail -1 `"
	
	pin="`head -4 	"plot_size-distribution/X-plot_size-distribution_eagg0-ki0__xi0__help.csv" | tail -1 `"
	pex="`head -5 	"plot_size-distribution/X-plot_size-distribution_eagg0-ki0__xi0__help.csv" | tail -1 `"
	lam="`head -6 	"plot_size-distribution/X-plot_size-distribution_eagg0-ki0__xi0__help.csv" | tail -1 `"
	
	#plot '<tail -n+7  "size-distribution_energy.csv"' using 1:2  w lines ls 1 #smooth bezier

		
#set xlabel "aggregationnumber" offset 0,0.6   font cmu
set xtics offset 0,0.2
set ytics offset 0.2,0
set y2tics # offset -0.2,0
#set ylabel "mole fraction" offset 0.6,0 font cmu
#set y2label "aspect ratio" offset -0.6,0 font cmu rotate by 270
#unset ytics

set key height 0 #outside
set key spacing 1 left
set key left

	line = 0.2
	step= "`head -1 	"values.csv"`"
	


set xtics nomirror (1) 20
#set x2tics
set y2tics 0.5 nomirror 
#set format y "%1.2f" 
set format y2 "%1.1f" 
set ytics  nomirror 
set autoscale xfix
set autoscale x2fix
set autoscale y2fix
set y2tics border in offset -5,0

set xrange[1:139]
#set x2range[0:120]
set yrange[0:13]
set y2range[0.75:2.05]

     
#set zrange [0:1000]
	
	kilw 	= "`head -3 "values.csv" | tail -1 `";
	kiup 	= "`head -6 "values.csv" | tail -1 `";
	gagglw	= "`head -2 "values.csv" | tail -1 `";
	gaggup	= "`head -5 "values.csv" | tail -1 `";
	xilw	= "`head -4 "values.csv" | tail -1 `";
	xiup	= "`head -7 "values.csv" | tail -1 `";
	
	do for[m=0:step]{
	  			if(m==0){
	  			xix(m)=0.0
	  			}
	  			else{
	  			xix(m)=xilw + (2.0**m/2.0**step)*(xiup-xilw)
	  			}
	 }
	 
	  	set arrow from 80,4.5 to 80,0 lc rgb 'grey' lw lwidth nohead
	  	set arrow from 106,7.24 to 110,7.86 lc rgb 'red' lw lwidth/2 nohead
	  	set arrow from 106,7.86 to 110,7.24 lc rgb 'red' lw lwidth/2 nohead
	  	
	  	set arrow from 108,7 to 108,8.1 lc rgb 'red' lw lwidth/2 nohead
	  	set arrow from 105,7.55 to 111,7.55 lc rgb 'red' lw lwidth/2 nohead
	  	
do for[i=1:step]{
do for[j=1:step]{

	ki		= (kilw + j*(kiup-kilw)/step)*2.311
	gagg	= (gagglw + i*(gaggup-gagglw)/step)*2.311
	
	
	titlefile = sprintf("k_i = %.0f, g^{agg} = %.2g", ki, gagg)
	
	#set title titlefile font "CMU Bright,50" offset 0,-0.8
		
  		set output sprintf("plots_size-distribution_png/plot_size-distribution_eagg%d-ki%d__xi.png", i, j)
  	
  		
		do for [m=1:step]{
		
	  		file(m) = sprintf("plot_size-distribution/plot_size-distribution_eagg%d-ki%d__xi%d.csv", i, j ,m)
	  		#set style line 14 	linecolor rgb 		pack(0, 	0, 	160) lw 2
	  	}	
	  	
	  	#set object 1 circle at 60,0.06 size scr 0.03 fc rgb "red"
		plot 'einv-scale.csv' using 2:1 axes x1y2 title "aspect ratio"  w l dt 4 lw 2	,\
		for [v =0:step]	 file(v)  using 1:3 ls 1+2*(v) w	lines title sprintf("ξ=%.2f", 	xix(v))
		
     
}
}

unset yrange	
set xrange [1:150]
set ytics font "CMU Bright,50"
set yrange [2.5:900]
unset y2tics
set format y "%1.0f"
#unset yrange	
set logscale y


	set key top right spacing 1 width 1.65 horizontal

do for[i=0:step]{
do for[j=0:step]{
	
	ki=kilw + j*(kiup-kilw)/step
	gagg=gagglw + i*(gaggup-gagglw)/step
	
	
	#set title titlefile
		
  	do for[z=0:step]{
  		set output sprintf("plots_energy_png/plot_energy_eagg%d-ki%d__xi.png", i, j)
  	
  		
		do for [m=0:step]{
	  		file(m) = sprintf("plot_energy/plot_energy_eagg%d-ki%d__xi%d.csv", i, j ,m)
  		xix(m)=xilw + (2.0**m/2.0**step)*(xiup-xilw)
 
	  	}
	  	
	ki		=(kilw + j*(kiup-kilw)/step)*2.311
	gagg	=(gagglw + i*(gaggup-gagglw)/step)*2.311
	
	titlefile = sprintf("k_i = %.0f, g^{agg} = %.2g", ki, gagg)
	
		plot for [v =0:step]	file(v) using 1:3  ls 1+2*(v) w	lines title sprintf("ξ=%.2f", 	xix(v))	
	}
}
}	





