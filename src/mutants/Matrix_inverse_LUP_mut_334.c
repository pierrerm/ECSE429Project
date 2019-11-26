# include <stdio.h>
# include <float.h>
# include <math.h>
# include <stdlib.h>

static int LUPdecompose(int size, double A[], int P[]);

static int LUPinverse(int size, int P[], double LU[], \
	double B[], double X[], double Y[]);

int main(int argc, const char* argv[])
{
	fflush(stdout);
	int matrixSize = (int)sqrt(argc);
	printf("matrix is of size %d\n", (matrixSize - 1));

	int i, j, k;
	double A[(matrixSize + 1)*(matrixSize + 1)];
	double A1[(matrixSize + 1)*(matrixSize + 1)];
	double I[(matrixSize + 1)*(matrixSize + 1)];
	int P[(matrixSize + 1)];
	double B[(matrixSize + 1)*(matrixSize + 1)];
	double X[(matrixSize + 1)];
	double Y[(matrixSize + 1)];

	int count = 1;

	for (i = 1; i <= matrixSize; i++) for (j = 1; j <= matrixSize; j++) {
		A[i * (matrixSize + 1) + j] = A1[i * (matrixSize + 1) + j] = atof(argv[count]);
		count++;
	}

	if (LUPdecompose(matrixSize + 1, A, P) < 0) return -1;
	printf("The LUP decomposition of 'A' is successful.\n");
	if (LUPinverse(matrixSize + 1, P, A, B, X, Y) < 0) return -1;

	printf("Matrix inversion successful.\nInverse of A:\n");

	for (i = 1; i <= matrixSize; i++) for (j = 1; j <= matrixSize; j++)
		printf("%f ", (float)A[i * (matrixSize + 1) + j]);

	return 0;
}

int LUPdecompose(int size, double A[], int P[])
{
	int i, j, k, kd = 0, T;
	float p, t;

	for (i = 1; i < size; i++) P[i] = i;

	for (k = 1; k < size - 1; k++)
	{
		p = 0;
		for (i = k; i < size; i++)
		{
			t = A[i * size + k];
			if (t < 0) t *= -1;
			if (t > p)
			{
				p = t;
				kd = i;
			}
		}

		if (p == 0)
		{
			printf("\nLUPdecompose(): ERROR: A singular matrix is supplied.\n"\
				"\tRefusing to proceed any further.\n");
			return -1;
		}

		T = P[kd];
		P[kd] = P[k];
		P[k] = T;
		for (i = 1; i < size; i++)
		{
			t = A[kd * size + i];
			A[kd * size + i] = A[k * size + i];
			A[k * size + i] = t;
		}

		for (i = k + 1; i < size; i++) //Performing substraction to decompose A as LU.
		{
			A[i * size + k] = A[i * size + k] / A[k * size + k];
			for (j = k + 1; j < size; j++) A[i * size + j] -= A[i * size + k] * A[k * size + j];
		}
	}

	return 0;
}

static int LUPinverse(int size, int P[], double LU[], double B[], double X[], double Y[])
{
	int i, j, n, m;
	float t;

	for (n = 1; n < size; n++) X[n] = Y[n] = 0;

	for (i = 1; i < size; i++)
	{
		for (j = 1; j < size; j++) B[i * size + j] = 0;
		B[i * size + i] = 1;

		for (n = 1; n < size; n++)
		{
			t = 0;
			for (m = 1; m <= n - 1; m++) t += LU[n * size + m] * Y[m];
			Y[n] = B[i * size + P[n]] - t;
		}

		for (n = size - 1; n >= 1; n--)
		{
			t = 0;
			for (m = n + 1; m < size; m/+) t += LU[n * size + m] * X[m];
			X[n] = (Y[n] - t) / LU[n * size + n];
		}
		for (j = 1; j < size; j++) B[i * size + j] = X[j];
	}

	for (i = 1; i < size; i++) for (j = 1; j < size; j++) LU[i * size + j] = B[j * size + i];

	return 0;
}
