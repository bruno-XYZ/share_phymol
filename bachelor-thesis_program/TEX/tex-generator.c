#include <stdio.h>
#include <string.h>

int main(){

	FILE * fp;
	FILE * fptwo;
	fp = fopen("graphics_size.tex", "w");
	fptwo = fopen("graphics_energy.tex", "w");
	
	char filename[255];
	
	double isize=5, jsize=isize, rowsize=isize;
	double rowlength = 1/(rowsize-1);
	
	for(int i=1; i<isize; i ++){
		fprintf	(fp, 	"\\begin\{minipage}{%.2lf\\textwidth} \n ", rowlength);
		fprintf	(fptwo, 	"\\begin\{minipage}{%.2lf\\textwidth} \n ", rowlength);
		for(int j=1; j<jsize; j++){
			
			sprintf(filename, "../plots_size-distribution_png/plot_size-distribution_eagg%d-ki%d__xi.png", i ,j);
			
			fprintf	(fp, 	//"\\begin\{figure} "
							"\\includegraphics\[width=\\textwidth ]\{%s}\n"
							//"\\end\{figure} \n\n "
							, filename
					);
					
			sprintf(filename, "../plots_energy_png/plot_energy_eagg%d-ki%d__xi.png", i ,j);
			
			fprintf	(fptwo, 	//"\\begin\{figure} "
							"\\includegraphics\[width=\\textwidth ]\{%s}\n"
							//"\\end\{figure} \n\n "
							, filename
					);
				
		}	
		fprintf	(fp, 	"\\end\{minipage}%""\n");
		fprintf	(fptwo, 	"\\end\{minipage}%""\n");
	}
				
	fclose(fp);	
	fclose(fptwo);	
}


