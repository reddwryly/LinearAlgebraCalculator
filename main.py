import numpy as np

"""
ideas for expanding this project:
    *ui for maxrix value entry
    *differnt pages for differnt calculators (like the calculator websites!!)
    *have guassian(/jordan) elimination work for infinite solutions (solve parametrically)
"""

#start with multiplication to get a better understanding of indexing**

def get_matrix_from_user():
    #ask for number of equations = (rows) and variables = (columns - 1)
    #loop with append to array by equation (row)
    #return an array called matrix 

    testMatrix = np.array([-3,-3,3,-1],
                          [9,5,-1,4],
                          [-9,-21,28,-2]) #test matrix = (11/60, 11/20, 2/5)
    return testMatrix

def gaussian_elimination(matrix=get_matrix_from_user()):

    #PRINT ALL STEPS TO THE USER

    #start with only handling unique solutions, tell the user if no solutions (check for contradictions)

    #column lastColumn + 1 => find pivot
    #see if rows need swaped => look for 0s in the pivotLocation = lastPivotIndex + 1
    #if 0 found: check second row for 0 in the desired pivot location repeat until pivot found
    #if no pivot found move on to next column with same pivot || augmented so ignore final/constant row ||

    #repeat for all non pivot columns:
    #continue to non pivot row (top to bottom) => pivot * x - nonPivot = 0
    #multiply pivot row by x then add the non pivot row to the pivot row
    #print the row operation new matrix for the user 

    #when complete final triangle matrix => back substitution 
    #finalVariable = finalConstant || secondToLastVariable + finalConstant = secondToLastConstat 
    #print a formatted opperation for each step 
    #repeat for all equations
    pass

def guassian_jordan_elimination(matrix=get_matrix_from_user()):
    pass

def matrix_multiplication(matrixA=get_matrix_from_user(), matrixB=get_matrix_from_user()):

    """
        A = 2x3
    | x00 x01 x02 | = xr1
    | x10 x11 x12 | = xr2

        B = 3x3
    | x00 x01 x02 | = xr1
    | x10 x11 x12 | = xr2
    | x20 x21 x22 | = xr3

    A x B

    check dimensions:
        dim(a) = 2x3
        dim(b) = 3x3

        3=3 check

        new dim = 2x3

    result (r):
        r00 = (a00 * b00) + (a01 * b10) + (a02 * b20)
        r01 = (a00 * b01) + (a01 * b11) + (a02 * b21)
        r02 = (a00 * b02) + (a01 * b12) + (a02 * b22)
        r10 = (a10 * b00) + (a11 * b10) + (a12 * b20)
        r11 = (a10 * b01) + (a11 * b11) + (a12 * b21)
        r12 = (a10 * b02) + (a11 * b12) + (a12 * b22)
    
    *print each equation to the user ^
        iterate through the indexes 
        print the two input matrixes as an equation and the result matrix (a * b = r but in matrix form)

    | r00 r01 r02 |
    | r10 r11 r12 |

    """
    pass

def menu():
    #any non int input should bring you back to menu at any time

    #loop for menu
    print("""\nSystem of Equations using Matrix Calculator *Showing Steps* \n----------------------------------------------------------
1.) Guassian Elimination \n2.) Guasian-Jordan Elimination \n3.) Matrix Multiplication \n4.) Exit\n""")

menu()