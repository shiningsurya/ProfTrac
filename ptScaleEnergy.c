// I want TI
// Where is my TI?
// Taking energy at every scale
#include<stdio.h>
#include<math.h>
#include<gsl/gsl_wavelet.h>


void phi(double * , int , int , double * ); 
void adder(double * , double * , int );
void cycler(double * , int );
void get_scale(double * , int , double * );
void divider(double * , int , int); 
void meanzero(double * , int ); 
void get_energy(double *, int, double *);

int main (int argc, char **argv)
{
		if(argc < 4) {
				printf("Usage: pt <PROFILE_FILE> <NUMBINS> <OUT_FILE>\n");
				exit(0);
		}
		(void)(argc); /* avoid unused parameter warning */
		int n = atoi(argv[2]);
		double * data = malloc ( n * sizeof(double) );
		int j = log2(n); 
		double * red  = malloc ( j * sizeof(double) );
		// FILEIO
		FILE *f;
		int i;
		f = fopen(argv[1],"r");
		// 
		// IO matched to SIGPROC style ASCII prof
		char ch[500];
		int di;
		fscanf(f,"%s\n",ch);
		for (i = 0; i < n; i++) {
				fscanf (f, "  %d %lf\n", &di, &data[i]);
				printf(" Huh %lf\n",data[i]);
		}
		fclose (f);
		for(i = 0; i < j;i++) red[i] = 0.00;
		// PHI call
		/*phi(data, n, j, red);*/
		get_energy(data,j,red);
		// PHI call
		f = fopen(argv[3],"w");
		for (i = 0; i < j; i++) {
				fprintf (f, "%lf\n", red[i]);
		}
		fclose (f);
		free(data);
		free(red);
		return 0;
}

void phi(double * in, int n, int j, double * out) {
		// phi because this is the work function
		// order of wavelet family is 8
		// size is input argument
		gsl_wavelet *wave;
		gsl_wavelet_workspace *wave_work;
		wave = gsl_wavelet_alloc ( gsl_wavelet_daubechies, 8);
		wave_work = gsl_wavelet_workspace_alloc(n);
		//
		double * data = malloc(n * sizeof(double));
		double * acc  = malloc(j * sizeof(double));
		int al;
		/*meanzero(in,n);*/
	    /******
	     * Mean gets to approximation hence, meanzero doesn't matter
	     * **/
		for(al = 0; al < n; al++) { 
				acc[al] = 0.00;
				data[al] = in[al];
				/*printf("In %lf\n", in[al]);*/
		}
		int i = 0;
		for(;i < (n-1);i++) {
				// work loop
				gsl_wavelet_transform_forward(wave, data, 1, n, wave_work);
				get_energy(data,j,acc);
				adder(out,acc,j);
				for(al = 0; al < n; al++) data[al] = in[al];
				cycler(data,n);
		}
		divider(out,j,n);
		/*get_scale(acc,j,out);*/
		/*divider(out,j);*/
		// free
		free(data);
		free(acc);
		gsl_wavelet_free(wave);
		gsl_wavelet_workspace_free(wave_work);
}

void divider(double * a, int n, int j) {
		int i;
		for(i = 0; i < n; i++) a[i] /= j;
}

void meanzero(double * a, int n) {
		int i;
		double t = 0.0;
		for(i = 0; i < n; i++) t += a[i];
		t /= n;
		for(i = 0; i < n; i++) a[i] -= t;
}

void adder(double * a, double * b, int n) {
		// accumulates `b` to `a`
		int i = 0;
		for(;i < n; i++) a[i] += b[i];
}

void cycler(double * in, int n) {
		/***
		 * Cycle to the left once
		 * **/
		double t = in[0];
		int i;
		for(i = 1; i < n; i++) in[i-1] = in[i];
		in[n-1] = t;
}

void  get_scale(double * in, int j, double * out) {
		/****
		 * Given the wavelet transformed list of coefficients
		 * merge the inter-scale coefficients
		 * output in out vector of size J
		 * *************
		 * tested it out. this works
		 * ***/
		int k,j1,j2;
		int wk;
		double t;
		//
		// ignore the approx. coefficient
		// running over J
		k = 1; // this runs over `in`
		for(j1 = 0; j1 < j; j1++) {
				t = 0.0;
				wk = pow(2,j1);
				for(j2 = 0; j2 < wk; j2++) t += in[k + j2];
				k += wk;
				out[j1] = t/wk;
				// This is averaged
		}
}
void get_energy(double * in, int j, double * out) {
		/****
		 * Given the wavelet transformed list of coefficients
		 * compute energy at every scale
		 * output in out vector of size J
		 * *************
		 * tested it out. this works
		 * ***/
		int k,j1,j2;
		int wk;
		double t;
		/*printf("Are you coming here?\n");*/
		//
		// ignore the approx. coefficient
		// running over J
		/*for(k = 0; k < 1024; k++) printf("in %lf\n",in[k]);*/
		k = 1; // this runs over `in`
		for(j1 = 0; j1 < j; j1++) {
				t = 0.0;
				wk = pow(2,j1);
				for(j2 = 0; j2 < wk; j2++)  t += pow(in[k + j2],2);//  printf(" %d %d here %lf\n",k, j2, in[k+j2]); }
				k += wk;
				out[j1] = t;
				/*printf("%d\n",k);*/
				// This is energy 
		}
		
}
