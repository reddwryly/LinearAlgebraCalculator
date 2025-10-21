import numpy as np
np.set_printoptions(precision=10, suppress=False)

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

testMatrix1 = np.array([[0,-3,3,-1],
                          [9,0,-1,4],
                          [2,1,28,-2],
                          [1,0,3,4]], dtype=float) #swap first pivot no rows skiped

testMatrix2 = np.array([[9,2,-1,4],
                        [0,0,3,-1],
                          [2,0,28,-2]], dtype=float) #swap second pivot underdetermined

testMatrix3 = np.array([[0,-3,3],
                          [9,0,-1],
                          [2,1,28],
                          [1,0,3]], dtype=float) #overdetermined

testMatrix4 = np.array([[1,2,3,9],
                          [2,3,1,8],
                          [3,1,2,10],], dtype=float) #from chatgpt

testMatrix5 = np.array([[5,2,1,-5,0],
                          [2,3,-2,3,0],
                          [-14,-10,6,4,0]], dtype=float) #infinite solution

def check_for_swap(matrix, rowTotal, columnTotal, pivotRowIndex, pivotColumnIndex):
    # print(matrix[pivotRowIndex])
    column = matrix[:,pivotColumnIndex] #returns column at the given index
    if column[pivotRowIndex] == 0:
        #loop through rest of column to find a value of not zero
        #swap rows to get a non zero pivot
        #if none skip to next column
        pivotOfOne = None
        for index in range(pivotRowIndex, rowTotal): 
            if column[index] == 1: #checks if it can switch to a pivot of 1 first
                pivotOfOne = index
        if pivotOfOne == None:
            for index in range(pivotRowIndex, rowTotal):
                if column[index] != 0:
                    #swap rows so piviot index is not zero
                    print(f"r{pivotRowIndex+1} <=> r{index+1}")
                    matrix[[pivotRowIndex, index]] = matrix[[index, pivotRowIndex]]
                    print(matrix)
                # print(matrix[pivotRowIndex])
                    break
                if column[index] == 0 and index == rowTotal-1 and pivotColumnIndex+1 < columnTotal:
                    print(f"no pivot in column {pivotColumnIndex+1}")
                    check_for_swap(matrix, rowTotal, pivotRowIndex, pivotColumnIndex+1)
        else:
            print(f"r{pivotRowIndex+1} <=> r{pivotOfOne+1}")
            matrix[[pivotRowIndex, pivotOfOne]] = matrix[[pivotOfOne, pivotRowIndex]]
            print(matrix)
    return matrix

def gaussian_elimination(matrix):
    
    print(matrix)
    #PRINT ALL STEPS TO THE USER
    #only handling unique solutions, tell the user if no solutions (check for contradictions)

    #matrix.shape returns dim(matrix) indexing it as 1 returns the number of columns
    columnTotal = matrix.shape[1] #includes augmented column*
    rowTotal = matrix.shape[0]

    #returns list of variable names X1, X2, ..., Xn n = totalColumns-1
    variables = []
    for columnIndex in range(1, columnTotal):
        variables += [f"X{columnIndex}"]
    print(variables)
        
    #column lastColumn + 1 => find pivot
    #see if rows need swaped => look for 0s in the pivotLocation = lastPivotIndex + 1

    #if 0 found: check second row for 0 in the desired pivot location repeat until pivot found
    #if no pivot found move on to next column with same pivot 

    pivotRowIndex = 0
    pivotColumnIndex = 0

    check_for_swap(matrix, rowTotal, columnTotal, pivotRowIndex, pivotColumnIndex) #returns new matrix

    #repeat for all non pivot columns:
    #continue to non pivot row (top to bottom) => pivot * x - nonPivot = 0
    #multiply pivot row by x then add the non pivot row to the pivot row
    #print the row operation and new matrix for the user

    for indexC in range(pivotColumnIndex, columnTotal):
        column = matrix[:,indexC] #returns column at the given index
        pivot = column[pivotRowIndex] 
        # print(pivot) #correct
        for indexR in range(pivotRowIndex+1, rowTotal):
            # print("column[indexR] = ",column[indexR])
            if column[indexR] != 0:
                rowMultiplier = column[indexR] / (pivot * -1)
            else:
                rowMultiplier = 0
            # print("rowMultiplier =", rowMultiplier) 
            for c in range(columnTotal):
                element = matrix[indexR][c]
                # print("element = ",element)
                # print("added element  =", (matrix[pivotRowIndex][c] * rowMultiplier))
                element += (matrix[pivotRowIndex][c] * rowMultiplier)
                # print("new element = ", element)
                matrix[indexR][c] = element
            if rowMultiplier != 0:
                print(f"{rowMultiplier} * r{pivotRowIndex+1} + r{indexR+1}") if rowMultiplier != 1 else print(f"r{pivotRowIndex+1} + r{indexR+1}")
                print(matrix)
        pivotRowIndex += 1
        pivotColumnIndex += 1
        if pivotRowIndex == rowTotal-1:
            break
        if pivotColumnIndex == columnTotal-1:
            break
        matrix = check_for_swap(matrix, rowTotal, columnTotal, pivotRowIndex, pivotColumnIndex)

    #when complete final triangle matrix => back substitution 
    #finalVariable = finalConstant || secondToLastVariable + finalConstant = secondToLastConstat 
    #print a formatted opperation for each step 
    #repeat for all equations 

    printList = []
    equationList = []
    equation = ""
    infiniteSolution = False
    for rowIndex in range(rowTotal-1,-1,-1): 
        # print(rowIndex)
        augment = matrix[rowIndex][columnTotal-1]
        print()
        for columnIndex in range(columnTotal-2, -1,-1):
            # print(matrix[rowIndex][columnIndex])
            var = matrix[rowIndex][columnIndex]
            printList += [f"{var}*{variables[columnIndex]}"]
        for i in range(len(printList)):
            if(i == 0):
                equation += f"{printList[i]} "
            elif(i == len(printList)-1): 
                equation += f" + {printList[i]} = {augment}"
            else:
                equation += f" + {printList[i]}"
        equationList += [equation]
        print(equation)
        equation = ""
        printList = []
        
        #check for no solution
        rowMinusAug = np.delete(matrix[rowIndex], -1)  
        if np.sum(rowMinusAug) == 0 and augment != 0:
            print(f"Contradiction found: {augment} not equal to 0 \nThere are no solutions.")
            return 0
        
        #check for infinite solution
        nonZeroRowMinusAug = rowMinusAug[rowMinusAug != 0]
        if len(nonZeroRowMinusAug) > 1 and rowIndex == rowTotal-1:
            print(f"There is a nonPivot row, there are infinite Solutions.")
            infiniteSolution = True
            break

        """
        does not work properly ^^ 
        """
        
        #alegbra logic: (sum of each element*previously found variable) / element of looking for variable
        """
        test matrix 4
            0x1 + 0x2 + 18*x3 = 33 -> 18*x3 = 33 -> x3 = 33/18 ~ 1.8333

            0x1 + -1x2 + -5x3 = -10 -> -1x2 + -5(33/18) = -10 -> x2 = (-10 - -5(33/18)) / -1 -> x2 = 5/6 ~ 0.83333

            1x1 + 2x2 + 3x3 = 9 -> 1x1 + 2(5/6) + 3(33/18) = 9 -> x1 = (9 - (2(5/8) + 3(33/18))) / 1 -> x1 = 11/6 ~ 1.8333

            Ax1 + Bx2 + Cx3 = D -> xn = D - (xn-1 * xn-1coefficent + ... + xn-m * xn-mcoefficent) / nCoefficent, n-m = smallest included x
                *loop through variable/column index and take the sum

        """

    results = [] 
    resultsIndex = 0 
    rIndex = rowTotal-1
    cIndex = columnTotal-2
    sum = 0
    aug = matrix[:,-1] 
    augIndex = len(aug)-1
    
    if infiniteSolution == False:
        while (augIndex >= 0):
            print(augIndex, rIndex, cIndex)
            row = matrix[rIndex] 
            nonZeroRow = row[row != 0]
            print("nzr:", nonZeroRow)
            print(row)
            if results:
                condition = len(nonZeroRow)
                increment = 1
                sum = 0
                while(condition > 2): #crazy times idk if this loop is nessisary but its wrong
                    print("sum: ",row[cIndex+increment], "*", results[-increment], " = ",sum)
                    sum += (row[cIndex+increment]) * results[-increment] 
                    condition -= 1 
                    increment += 1
            print("sum = ", sum)
            print(f"result: {aug[augIndex]} - {sum} / {row[cIndex]} = {(aug[augIndex] - sum) / row[cIndex]}")
            results += [(aug[augIndex] - sum) / row[cIndex]]
            print(f"result = {results[resultsIndex]}")
            resultsIndex += 1
            rIndex -= 1
            cIndex -= 1
            augIndex -= 1

    while (infiniteSolution):
        pass

    results.reverse()

    for i in results:
        print(i, end=" ")

# gaussian_elimination(testMatrix1)
# gaussian_elimination(testMatrix2)
# gaussian_elimination(testMatrix3)
# gaussian_elimination(testMatrix4)
gaussian_elimination(testMatrix5)


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
