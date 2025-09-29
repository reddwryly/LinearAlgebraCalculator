import numpy as np

"""
ideas for expanding this project:
    *ui for maxrix value entry
    *differnt pages for differnt calculators (like the calculator websites!!)
    *have guassian(/jordan) elimination work for infinite solutions (solve parametrically)
"""

def menu():
    #any non-int input should bring you back to menu at any time

    #loop for menu
    print("""\nSystem of Equations using Matrix Calculator *Showing Steps* \n----------------------------------------------------------
1.) Guassian Elimination \n2.) Guasian-Jordan Elimination \n3.) Matrix Multiplication \n4.) Exit\n""")


def get_matrix_from_user():
    #ask for number of equations = (rows) and variables = (columns - 1)
    numRows = input("Enter number of rows/equations: ")
    if numRows.isdigit() == False:
        menu() # if the user enters not a number, then it should return to the menu

    numColumns = input("Enter number of columns/variables: ")
    if numColumns.isdigit() == False:
        menu() # returns to main menu when non-number entered

    # confirms the method to solve matrix 
    solvingMethod = input("Would you like to see this matrix solved using Gaussian Elimination or Guass-Jordan Elimination?" \
    "Enter 'G' or 'GJ': ")
    while (solvingMethod.lower() != "g" and solvingMethod.lower != "gj"):
        solvingMethod = input("Please enter a 'G' or 'GJ' to solve: ")

    #loop with append to array by equation (row)
    #return an array called matrix 

    testMatrix = np.array([[-3,-3,3,-1],
                          [9,5,-1,4],
                          [-9,-21,28,-2]]) #test matrix = (11/60, 11/20, 2/5)
    return testMatrix

testMatrix = np.array([[0,-3,3,-1],
                          [9,0,-1,4],
                          [-9,1,28,-2],
                          [1,0,3,4]])

def decimal_to_fraction():
    pass

def check_for_swap(matrix, rowTotal, pivotRowIndex, pivotColumnIndex):
    # print(matrix[pivotRowIndex])
    column = matrix[:,pivotColumnIndex] #returns column at the given index
    if column[pivotRowIndex] == 0:
        #loop through rest of column to find a value of not zero
        #swap rows to get a non zero pivot
        #if none skip to next column
        for index in range(pivotRowIndex, rowTotal):
            if column[index] != 0:
                #swap rows so piviot index is not zero
                print(f"r{pivotRowIndex+1} <=> r{index+1}")
                matrix[pivotRowIndex] = matrix[index]
               # print(matrix[pivotRowIndex])
                break
            if column[index] == 0 and index == rowTotal-1:
                print(f"no pivot in column {pivotColumnIndex+1}")
                check_for_swap(matrix, rowTotal, pivotRowIndex, pivotColumnIndex+1)
    return matrix

def gaussian_elimination(matrix):
    
    print(matrix)
    #PRINT ALL STEPS TO THE USER
    #only handling unique solutions, tell the user if no solutions (check for contradictions)

    #matrix.shape returns dim(matrix) indexing it as 1 returns the number of columns
    columnTotal = matrix.shape[1] #includes augmented column*
    rowTotal = matrix.shape[0]
 
    #column lastColumn + 1 => find pivot
    #see if rows need swaped => look for 0s in the pivotLocation = lastPivotIndex + 1

    #if 0 found: check second row for 0 in the desired pivot location repeat until pivot found
    #if no pivot found move on to next column with same pivot 

    pivotRowIndex = 0
    pivotColumnIndex = 0

    print(check_for_swap(matrix, rowTotal, pivotRowIndex, pivotColumnIndex)) #check_for_swap returns the matrix

    # for column in range(len(matrix)): #for [0,1,2,3],[4,5,6,7],[8,9,10,11] => 0, 1, 2
    #     for row in range(len(matrix[column])): #for [4,5,6,7] => 0, 1, 2, 3
    #         print(row)
    
    #repeat for all non pivot columns:
    #continue to non pivot row (top to bottom) => pivot * x - nonPivot = 0
    #multiply pivot row by x then add the non pivot row to the pivot row
    #print the row operation new matrix for the user

    for indexC in range(pivotColumnIndex, columnTotal):
        column = matrix[:,indexC] #returns column at the given index
        pivot = column[pivotRowIndex]
        rowMultiplier = (column[pivotRowIndex+1] * -1) / pivot
        for indexR in range(pivotRowIndex+1, rowTotal):
            newRowforAddition = rowMultiplier * column[indexR]
            # matrix[indexR][indexC] = newRowforAddition + column[]

    """
    *need to figure out how to scaler multiply to row 
    *and if i can also add two rows (matrix addition) possibly new function
    """

    #when complete final triangle matrix => back substitution 
    #finalVariable = finalConstant || secondToLastVariable + finalConstant = secondToLastConstat 
    #print a formatted opperation for each step 
    #repeat for all equations 
    pass

gaussian_elimination(testMatrix)

def guassian_jordan_elimination(matrix): # GJE means RREF - all zeroes in non-pivot points
    #
    pass

def matrix_multiplication(matrixA, matrixB):

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
