#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

//TOL
const double TOL = 1.0E-5;
const int MAXN = 0.2E3;

struct params{
	double cnot;
	double ctot;
	double* DARR;
	double* FARR;
	double* EARR;
	double borders[6];
	double anot;
	double surftens;
	double beta;
	double lam;
	double pex_0;
	double pin_0;
	double xi;
	double ki;
	double E_agg;
	double potagg;
	double RT;
	double einv;
	int arraysize;
	int numsphere;
};


#include "header/header-distribution_IO.h"
#include "header/header-distribution_FREE-ENERGY-FRUST.h"
#include "header/header-distribution_SERIES.h"


int main ( )
{
	struct params paramscur;
	
//concentrations
	
	/// MAXIMUM 3
	paramscur.ctot = 0.5;
	paramscur.cnot = 1;
	
//System parameters
	// scale down every length volume and area unit to beta!
	
	// with unit
	paramscur.beta  = 1;
	
	paramscur.numsphere=80;
	//dummy value
	paramscur.anot 		= ((4)*pow(paramscur.beta,2)*M_PI)/paramscur.numsphere;
	paramscur.surftens	=	1;
	// calulate energies in RT
	paramscur.ki 		= 	1.0		;
	paramscur.E_agg		= 	-5.0		;	
	paramscur.potagg	= 	1.0		;
	paramscur.RT		= 	1.0		;
	
	//without unit
	paramscur.lam		= 	0.75	;
	paramscur.pex_0 	= 	1.75	;
	paramscur.pin_0 	= 	0.25	;
	paramscur.xi  		= 	1.0		;
	
	int steps =4;
	double help1[6]=			{ 	-0,  		0, 		0,   	// lower: E_agg, ki, xi
									-14,		14, 	4, 		
									};	
		for (int i=0; i<6; i++){
			paramscur.borders[i]=help1[i];
		}
	printvalues(paramscur,steps);
	//array to save 
	paramscur.DARR = (double*) calloc (MAXN,sizeof(double));
	paramscur.FARR = (double*) calloc (MAXN,sizeof(double));
	paramscur.EARR = (double*) calloc (MAXN,sizeof(double));
	
	paramscur.arraysize = MAXN;
	
	//
	double xtot = paramscur.ctot/paramscur.cnot;
	
// work
	int numarr[3];
	int uv;
	for (int i=0; i < steps + 1 ; i++) {
		uv=0;
		paramscur.E_agg=paramscur.borders[uv]+
		i*(paramscur.borders[uv+3]-paramscur.borders[uv])/steps;
	for (int j=0; j < steps + 1 ; j++) {
		uv=1;
		paramscur.ki=paramscur.borders[uv]+
		j*(paramscur.borders[uv+3]-paramscur.borders[uv])/steps;
	for (int k=0; k < steps + 1; k++) {
		uv=2;
		if(k>0){
			paramscur.xi=paramscur.borders[uv]+
			((pow(2.0,k))/(pow(2.0,steps)))*(paramscur.borders[uv+3]-paramscur.borders[uv]);
		}
		else{
			paramscur.xi=paramscur.borders[uv];
		}
		
			numarr[0] = i;
			numarr[1] = j;
			numarr[2] = k;
			//printf("params %lf, \t %lf \t %lf\n", paramscur.E_agg, paramscur.ki, paramscur.xi);
			
			algorithm(paramscur, xtot);
			
			write_to_file (paramscur, paramscur.DARR, paramscur.EARR, "plot_size-distribution",
			paramscur.arraysize, numarr);
			write_to_file (paramscur, paramscur.FARR, paramscur.EARR,"plot_energy",
			paramscur.arraysize, numarr);

        int tot_steps,n_step;
	    tot_steps = (steps)*(steps+1)*(steps+1) + (steps)*(steps+1) + (steps+1) ;	
        n_step=i*(steps+1)*(steps+1) + j*(steps+1) + k +1 ;
        if (tot_steps>=10) {
            if (n_step%5==0){
                printf("plot %d of %d \n", n_step, tot_steps);
            }
        }
        else {
            printf("plot %d of %d \n", n_step, tot_steps);
        }
	}
	}
	}
	
	free(paramscur.DARR);
	free(paramscur.FARR);
}
