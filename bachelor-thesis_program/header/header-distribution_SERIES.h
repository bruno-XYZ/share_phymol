
void algorithm (struct params paramscur, double xTot);
double calc_series (struct params paramscur, double xone);

void algorithm (struct params paramscur, double xTot)
{
	double xCalcTot=-420;
	//double factor=-420;
	//double xOne=xTot;
	double xcheck=2;
	int I=0;
	//printf("Start-------------\n");
	//printf("xTot: %lf\n", xTot);
	double x_lw=0, x_up=xTot;
	double x_mid = x_lw + (x_up-x_lw)/2;
	while ( fabs(xcheck)>TOL && I<MAXN)
	{
		xCalcTot	=	calc_series (paramscur, x_mid);
		//printf("xTot: %lf \n", xCalcTot);
		xcheck = xCalcTot-xTot;
		//printf("xcheck %lf\n", xcheck);
		if(xcheck>0){
			x_up=x_mid;
		}
		else{
			x_lw=x_mid;
		}
		x_mid = x_lw + (x_up-x_lw)/2;
		//printf("x_mid : %lf\n", x_mid);
		//	xOne 		*= 	factor ;
		// norm to one!!
		//printf("factor: %lf\n", factor);
		//printf("%lf\n", checkvar);
		I++;
	}
	//renormation
	//printf("xcalctot: %lf\n", xCalcTot);
	for (int J=0; J<MAXN; J++)
	{
		paramscur.DARR[J]*=1/xCalcTot;
	}
}

//same TOL????

double damp_calc (struct params paramscur, int J)
{
    double damp,par=5;
    int ns=paramscur.numsphere;
	damp=(3./(4.-exp(-J+1.)));
	damp*=pow( (1.-exp(par* (J-ns)/ns )) , 4);
	damp/=pow( (1.-exp(par* (1.-ns)/ns )) , 4);
	
	//printf("damp for %d :  %lf \n",J,damp);
	return damp;
}

double calc_series (struct params paramscur, double xone)
{
	//printf("Start\n");
//indexshift
	int J=1;
	double xJ=0, fJ, gFrust, gaggfru, entr, xovl=xone, numagg, damp;
	double xbase=xone;
	//printf("xone %lf\n", xbase);
	paramscur.DARR[0]=xone;
	paramscur.FARR[0]= - log(xbase);
	int check=0;
	double shift	= - func_E_frust(paramscur, 1);
	while ( check==0 && J<MAXN)
	{
		J++;
		gFrust 	= func_E_frust(paramscur, J) ;
		//printf("gFrust: %lf \n", gFrust);
		// otherwise problme with integer -> double	
		numagg		= pow((J-1), paramscur.potagg)/pow(J, paramscur.potagg);
			//printf("numagg: %lf\n", numagg);
		if(J<paramscur.numsphere)
		{
		    damp=damp_calc(paramscur,J);
		}
		else
		{
		    damp=0.0;
		}
		gaggfru		= (1-damp)*paramscur.E_agg*numagg + (1.-damp)*gFrust;

			//printf("%lf\n", gaggfru);
		fJ	= 		gaggfru*J + shift;
		//printf("log: %lf\n", log(pow(xone,J+1)));	
			//printf("fJ: %lf\n", fJ);
		xJ = log(J)-fJ+J*log(xbase);
		xJ = exp (xJ);
			//xcorr = sqrt()
			//printf("xJsqrt %lf, %d \t", xJ, J);
		
		if (xJ>10){
			check=1;
			xovl=11;
			//printf("J: %d\n", J);
		}
		else{
			xovl += xJ;
		}
		
		
		//printf("%lf\n", fFrust);
		entr = 	 log(J) + J*log(xbase);
		//printf("entr: %lf \n", entr);	
		fJ	-= 	entr;
		
		//printf("xJ: %lf \t fJ: %lf \n", xJ ,fJ/J);
		//printf("log: %lf\n", log(pow(xone,J+1)));	
		
			//printf("xJ %lf \t", xJ);
		paramscur.DARR[J-1]=xJ;
		paramscur.FARR[J-1]=fJ;
		
		//printf("xovl %lf\n", xovl);
	}
	//printf("xovl %lf\n", xovl);
	paramscur.arraysize = J;
	return xovl;
}
