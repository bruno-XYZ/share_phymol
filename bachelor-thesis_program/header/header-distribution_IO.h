void printvalues (struct params paramscur, int steps);
void write_to_file (struct params paramscur, double array[], double arraytwo[], char filename[], int length, int numarr[]);


void printvalues (struct params paramscur, int steps)
{
	FILE * fp;
	fp = fopen("values.csv","w");
	fprintf(fp, "%d\n", steps);
	for(int i=0; i<6; i++){
		fprintf(fp, "%lf\n", paramscur.borders[i]);
	}
}

void write_to_file (struct params paramscur, double array[],double arraytwo[], char filename[], int length, int numarr[])
{
	FILE* fp;
	char filenamenum[255];
	
	sprintf(filenamenum, "%s/X-%s_eagg%d-ki%d__xi%d__help.csv", filename, filename, numarr[0], numarr[1], numarr[2]);
	fp = fopen( filenamenum, "w");
	
	//fprintf (fp, "Aggregation number \t x_i\n");
	
	
	
	fprintf (fp, "%.3g \n",  paramscur.ki);
	fprintf (fp, "%.3g \n",  paramscur.E_agg);
	fprintf (fp, "%.3g \n",  paramscur.ctot/paramscur.cnot);
	//fprintf (fp, "%.12lf \n",  paramscur.RT);
	
	fprintf (fp, "%.3g \n",  paramscur.pin_0);
	fprintf (fp, "%.3g \n",  paramscur.pex_0);
	fprintf (fp, "%.3g \n",  paramscur.lam);
	fprintf (fp, "%.3g \n",  paramscur.xi);
	
	sprintf(filenamenum, "%s/%s_eagg%d-ki%d__xi%d.csv", filename, filename, numarr[0], numarr[1], numarr[2]);
	
	fp = fopen( filenamenum, "w");
	
	
	for(int i=0; i<length; i++){
	//if(i%10 ==0){
		fprintf (fp, "%4d \t ,%.12lf ,%.12lf \n", i+1, arraytwo[i], array[i]*100 );
	/*}
	else{
		fprintf (fp, "%4d \t , \t ,%.12lf \n", i+1, array[i] );
	}*/
	}
	
	fclose(fp);
	
	FILE* fptwo;
	
	sprintf(filenamenum, "einv-scale.csv");
	fptwo = fopen( filenamenum, "w");
	
	//fprintf (fp, "Aggregation number \t x_i\n");
	
	
	for(int i=0; i<length; i++){
	/*	if(i>=59){
		if(fmod(1/arraytwo[i],0.5) <0.1){*/
			fprintf (fptwo, "%.12lf ,%4d \t ,%4d \t \n", 1/arraytwo[i],i+1,  i+1);
	/*		i+=5;
		}
		}
		
	*/
	}
	fclose(fptwo);	
}
