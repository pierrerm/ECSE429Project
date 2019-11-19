/* Copyright 2015 Chandra Shekhar (chandraiitk AT yahoo DOT co DOT in).
Homepage: https://sites.google.com/site/chandraacads
* * */


/* This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
* * */


/* This program computes inverse of a square matrix, based on LUP decomposition.
*
* Tested with GCC-4.8.3 on 64 bit Linux (Fedora-20).
*
* Compilation:     "gcc -O2 Matrix_inverse_LUP.c -o Mat_inv_LUP.exe -lm -Wall"
* Execution:     "./Mat_inv_LUP.exe"
* * */

# include <stdio.h>
# include <float.h>
# include <math.h>
# include <stdlib.h>


/* This function performs LUP decomposition of the to-be-inverted matrix 'A'. It is
* defined after the function 'main()'.
* * */
static int LUPdecompose(int size, double A[size][size], int P[size]);

/* This function calculates inverse of the matrix A. It accepts the LUP decomposed
* matrix through 'LU' and the corresponding pivot through 'P'. The inverse is
* returned through 'LU' itself. The spaces 'B', 'X', and 'Y' are used temporary,
* merely to facilitate the computation. This function is defined after the function
* 'LUPdecompose()'.
* * */
static int LUPinverse(int size, int P[size], double LU[size][size],\
    double B[size][size], double X[size], double Y[size]);

    int main(int argc, const char* argv[] )
    {
         fflush( stdout );
        int matrixSize = (int) sqrt(argc);
        printf("matrix is of size %d\n", matrixSize);

        double A[matrixSize][matrixSize], A1[matrixSize][matrixSize], I[matrixSize][matrixSize];
        int P[matrixSize];
        double B[matrixSize][matrixSize], X[matrixSize], Y[matrixSize]; //Temporary spaces.

        int count = 1;

        for (int i = 0 ; i < matrixSize ; i++){
            for (int j = 0 ; j < matrixSize ; j++){
                A[i][j] = A1[i][j] = atof(argv[count]);
                count++;
            }
        }

        if(LUPinverse(matrixSize, P, A, B, X, Y) < 0) return -1;
        printf("\n\nMatrix inversion successful.\nInverse of A:\n");
        fflush( stdout );
        for(int j = 0; j < matrixSize; j++)
        {
          for(int i = 0; i < matrixSize; i++) printf("%f ", (float)A[i][j]);
        }

        return 0;
    }



    /* This function decomposes the matrix 'A' into L, U, and P. If successful,
    * the L and the U are stored in 'A', and information about the pivot in 'P'.
    * The diagonal elements of 'L' are all 1, and therefore they are not stored. */
    static int LUPdecompose(int size, double A[size][size], int P[size])
    {
        int i, j, k, kd = 0, T;
        double p, t;

        /* Finding the pivot of the LUP decomposition. */
        for(i=1; i<size; i++) P[i] = i; //Initializing.

        for(k=1; k<size-1; k++)
        {
            p = 0;
            for(i=k; i<size; i++)
            {
                t = A[i][k];
                if(t < 0) t *= -1; //Abosolute value of 't'.
                if(t > p)
                {
                    p = t;
                    kd = i;
                }
            }

            if(p == 0)
            {
                printf("\nLUPdecompose(): ERROR: A singular matrix is supplied.\n"\
                "\tRefusing to proceed any further.\n");
                return -1;
            }

            /* Exchanging the rows according to the pivot determined above. */
            T = P[kd];
            P[kd] = P[k];
            P[k] = T;
            for(i=1; i<size; i++)
            {
                t = A[kd][i];
                A[kd][i] = A[k][i];
                A[k][i] = t;
            }

            for(i=k+1; i<size; i++) //Performing substraction to decompose A as LU.
            {
                A[i][k] = A[i][k]/A[k][k];
                for(j=k+1; j<size; j++) A[i][j] -= A[i][k]*A[k][j];
            }
        } //Now, 'A' contains the L (without the diagonal elements, which are all 1)
        //and the U.

        return 0;
    }



    /* This function calculates the inverse of the LUP decomposed matrix 'LU' and pivoting
    * information stored in 'P'. The inverse is returned through the matrix 'LU' itselt.
    * 'B', X', and 'Y' are used as temporary spaces. */
    static int LUPinverse(int size, int P[size], double LU[size][size],\
        double B[size][size], double X[size], double Y[size])
        {
            int i, j, n, m;
            double t;

            //Initializing X and Y.
            for(n=1; n<size; n++) X[n] = Y[n] = 0;

            /* Solving LUX = Pe, in order to calculate the inverse of 'A'. Here, 'e' is a column
            * vector of the identity matrix of size 'size-1'. Solving for all 'e'. */
            for(i=1; i<size; i++)
            {
                //Storing elements of the i-th column of the identity matrix in i-th row of 'B'.
                for(j = 1; j<size; j++) B[i][j] = 0;
                B[i][i] = 1;

                //Solving Ly = Pb.
                for(n=1; n<size; n++)
                {
                    t = 0;
                    for(m=1; m<=n-1; m++) t += LU[n][m]*Y[m];
                    Y[n] = B[i][P[n]]-t;
                }

                //Solving Ux = y.
                for(n=size-1; n>=1; n--)
                {
                    t = 0;
                    for(m = n+1; m < size; m++) t += LU[n][m]*X[m];
                    X[n] = (Y[n]-t)/LU[n][n];
                }//Now, X contains the solution.

                for(j = 1; j<size; j++) B[i][j] = X[j]; //Copying 'X' into the same row of 'B'.
            } //Now, 'B' the transpose of the inverse of 'A'.

            /* Copying transpose of 'B' into 'LU', which would the inverse of 'A'. */
            for(i=1; i<size; i++) for(j=1; j<size; j++) LU[i][j] = B[j][i];

            return 0;
        }
