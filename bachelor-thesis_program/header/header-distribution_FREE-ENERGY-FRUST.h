double AtoEinv (struct params paramscur, int J );
double engval (struct params paramscur, double einv);
double func_E_frust ( struct params paramscur, int J);


double AtoEinv (struct params paramscur, int J )
{
	// not define for 1!!
	double 	einv_up = 1-TOL, einv_lw=0;
	double 	heinv, aim, deviance, sqrthelp;
	int 	cnt=0;
	double einvcur;
	
	aim	=(J*paramscur.anot)/(4*M_PI*pow(paramscur.beta,2));
	
	while (cnt<MAXN ){
	// h monotonuously increasing
	
		einvcur			= einv_lw + (einv_up-einv_lw)/2;
		sqrthelp		= sqrt(1-pow(einvcur,2));
		heinv 			= 1 + (asin(sqrthelp))/(einvcur*sqrthelp);
		deviance 		= aim - heinv/2;
		//printf("%lf, \t %lf \n", einvcur, heinv);
	
		if (deviance<0)
		{
			einv_lw = einvcur;
		}
		else
		{
			einv_up = einvcur;
		}
		cnt++;
		
	}
	
	//printf("J: %d, aim: %lf, einv: %lf \n", J, aim, einv_up);
	
		//printf("J: %d \t aim : %lf \t einvup: %lf \n", J, aim, einv_up);
	return einv_up;
}

double func_E_frust ( struct params paramscur, int J){

	double ratio = ((double)paramscur.numsphere)/((double)J);
	//printf("ratio: %d %lf \n", J, ratio);
	double gfru;
	double einv,einv2;
	double engsph=engval(paramscur, 0.999999);
		
	if(ratio<=1)
	//formula for ellipsoid
	{
		// save einv
		einv	= AtoEinv(paramscur, J);
		paramscur.EARR[J-1] = einv;
		
		gfru	=	engval(paramscur, einv);
	}
	else
	//formula by surface tension
	{
		//paramscur.EARR[J-1] = 0.9999;
		//gfru	=	(paramscur.numsphere-J)*paramscur.surftens/J + engsph;
		einv	= AtoEinv(paramscur, paramscur.numsphere);
		einv2	= AtoEinv(paramscur, 2*paramscur.numsphere-J);
		if(J==paramscur.numsphere)
		{
		    gfru    =engsph;
		}
		else
		{
		    gfru    = 2*engsph- 
		            engval(paramscur,einv2);
		}
	}
		
		//printf("grfru: %lf \n", gfru);
		return gfru;
}

double engval (struct params paramscur, double einv)
{
	
		double pin_0 = paramscur.pin_0;
		double pex_0 = paramscur.pex_0;
		double lam   = paramscur.lam;
		double xi    = paramscur.xi;
		
	double gfrutrans, h;
		double sqrth = sqrt(1- pow(einv, 2));
			//printf("sqrth: \t %lf\n", sqrth);
		double test=asin(sqrth);
			//printf("test: \t %lf\t", test);
			//printf("einv: \t %lf\t", einv);
		
		h=1/(einv + test/(sqrth))*2/3	;
			//printf("g: %lf", g);
			//printf("g: \t %lf\t", g);
		// formula for gfru
		gfrutrans	=	pow((h - pin_0),2) 
			+ xi * pow( ( h * (2 + einv + (1 + 2*einv )* lam + einv* pow(lam,2)) - pex_0) , 2);
		gfrutrans	*=	paramscur.ki/2;
			//printf("f: \t %lf\n", f);
	//printf("gfrutrans %lf \n", gfrutrans);
	return gfrutrans;
}

