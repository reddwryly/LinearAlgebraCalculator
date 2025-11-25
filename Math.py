import numpy as np
# import re
# from fractions import Fraction
np.set_printoptions(precision=10, suppress=False)

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

testMatrix6 = np.array([[5,2,1,-5, 10, 0],
                          [2,3,-2,3, 13, 0],
                          [-14,-10,6,4, 20,0]], dtype=float) #infinite solution

testMatrix7 = np.array([[1,-1,3],[2,-4,5]]) #inconsistent

def check_for_swap(file, matrix, rowTotal, columnTotal, pivotRowIndex, pivotColumnIndex):
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
                    file.write(f"r{pivotRowIndex+1} <=> r{index+1}\n")
                    matrix[[pivotRowIndex, index]] = matrix[[index, pivotRowIndex]]
                    file.writelines(f"{str(matrix)}\n")
                    break
                if column[index] == 0 and index == rowTotal-1 and pivotColumnIndex+1 < columnTotal:
                    file.write(f"no pivot in column {pivotColumnIndex+1}\n")
                    check_for_swap(file, matrix, rowTotal, pivotRowIndex, pivotColumnIndex+1)
        else:
            file.write(f"r{pivotRowIndex+1} <=> r{pivotOfOne+1}\n")
            matrix[[pivotRowIndex, pivotOfOne]] = matrix[[pivotOfOne, pivotRowIndex]]
            file.writelines(f"{str(matrix)}\n")
    return matrix

def gaussian_elimination(matrix):
    file = open("DisplayGuass.txt", "w")
    #PRINT ALL STEPS TO THE USER
    #only handling unique solutions, tell the user if no solutions (check for contradictions)

    #matrix.shape returns dim(matrix) indexing it as 1 returns the number of columns
    columnTotal = matrix.shape[1] #includes augmented column*
    rowTotal = matrix.shape[0]

    #returns list of variable names X1, X2, ..., Xn n = totalColumns-1
    variables = []
    for columnIndex in range(1, columnTotal):
        variables += [f"X{columnIndex}"]
    file.writelines(f"{str(variables)}\n")
    file.writelines(f"{str(matrix)}\n")
        
    #column lastColumn + 1 => find pivot
    #see if rows need swaped => look for 0s in the pivotLocation = lastPivotIndex + 1

    #if 0 found: check second row for 0 in the desired pivot location repeat until pivot found
    #if no pivot found move on to next column with same pivot 

    pivotRowIndex = 0
    pivotColumnIndex = 0

    check_for_swap(file, matrix, rowTotal, columnTotal, pivotRowIndex, pivotColumnIndex) #returns new matrix

    #repeat for all non pivot columns:
    #continue to non pivot row (top to bottom) => pivot * x - nonPivot = 0
    #multiply pivot row by x then add the non pivot row to the pivot row
    #print the row operation and new matrix for the user

    for indexC in range(pivotColumnIndex, columnTotal):
        column = matrix[:,indexC] #returns column at the given index
        pivot = column[pivotRowIndex] 
        for indexR in range(pivotRowIndex+1, rowTotal):
            if column[indexR] != 0:
                rowMultiplier = column[indexR] / (pivot * -1)
            else:
                rowMultiplier = 0
            for c in range(columnTotal):
                element = matrix[indexR][c]
                element += (matrix[pivotRowIndex][c] * rowMultiplier)
                matrix[indexR][c] = element
            if rowMultiplier != 0:
                file.write(f"{rowMultiplier} * r{pivotRowIndex+1} + r{indexR+1}\n") if rowMultiplier != 1 else print(f"r{pivotRowIndex+1} + r{indexR+1}\n")
                file.writelines(f"{str(matrix)}\n")
        pivotRowIndex += 1
        pivotColumnIndex += 1
        if pivotRowIndex == rowTotal-1:
            break
        if pivotColumnIndex == columnTotal-1:
            break
        matrix = check_for_swap(file, matrix, rowTotal, columnTotal, pivotRowIndex, pivotColumnIndex)

    #when complete final triangle matrix => back substitution 
    #finalVariable = finalConstant || secondToLastVariable + finalConstant = secondToLastConstat 
    #print a formatted opperation for each step 
    #repeat for all equations 

    printList = []
    equationList = []
    equation = ""
    infiniteSolution = False
    for rowIndex in range(rowTotal-1,-1,-1): 
        augment = matrix[rowIndex][columnTotal-1]
        file.write("\n")
        for columnIndex in range(columnTotal-2, -1,-1):
            coef = matrix[rowIndex][columnIndex]
            printList += [f"{coef}*{variables[columnIndex]}"]
        for i in range(len(printList)):
            if(i == 0):
                equation += f"{printList[i]} "
            elif(i == len(printList)-1): 
                equation += f" + {printList[i]} = {augment}"
            else:
                equation += f" + {printList[i]}"
        equationList += [equation]
        file.writelines(f"{equation}\n")
        equation = ""
        printList = []
        
        #check for no solution
        rowMinusAug = np.delete(matrix[rowIndex], -1) 
        rowCheck = rowMinusAug[rowMinusAug == 0] 
        if np.array_equal(rowMinusAug, rowCheck) and augment != 0:
            file.write(f"Contradiction found: {augment} not equal to 0 \nThere are no solutions.\n")
            return 0
        
        #check for infinite solution
        allZeroRowMask = np.all(matrix == 0, axis=1)
        noZeroMatrixMask = ~allZeroRowMask
        new_matrix = matrix[noZeroMatrixMask] #masks remove all zero rows before checking for infinite solution
        if rowTotal < columnTotal-1:
            file.write(f"There is a nonPivot row. The number of equations is less than the number of variables, there are infinite Solutions.\n")
            infiniteSolution = True
            break

        #alegbra logic: (sum of each element*previously found variable) / element of looking for variable
        """
        test matrix 4
            0x1 + 0x2 + 18*x3 = 33 -> 18*x3 = 33 -> x3 = 33/18 ~ 1.8333

            0x1 + -1x2 + -5x3 = -10 -> -1x2 + -5(33/18) = -10 -> x2 = (-10 - -5(33/18)) / -1 -> x2 = 5/6 ~ 0.83333

            1x1 + 2x2 + 3x3 = 9 -> 1x1 + 2(5/6) + 3(33/18) = 9 -> x1 = (9 - (2(5/8) + 3(33/18))) / 1 -> x1 = 11/6 ~ 1.8333

            Ax1 + Bx2 + Cx3 = D -> xn = D - (xn-1 * xn-1coefficent + ... + xn-m * xn-mcoefficent) / nCoefficent, n-m = smallest included x
                *loop through variable/column index and take the sum
        """

    #back substitution
    results = [] 
    resultsIndex = 0 
    rIndex = rowTotal-1
    cIndex = columnTotal-2
    aug = matrix[:,-1] 
    augIndex = len(aug)-1
    
    if not infiniteSolution:
        sum = 0
        while (augIndex >= 0):
            row = matrix[rIndex] 
            nonZeroRow = row[row != 0]
            if results:
                condition = len(nonZeroRow)
                increment = 1
                sum = 0
                while(condition > 2):
                    sum += (row[cIndex+increment]) * results[-increment] 
                    condition -= 1 
                    increment += 1
            file.write("\n")
            
            #prints equations with pluged in value 
            printList = []
            equationList = []
            equation = ""

            """
            expected:
            coef*X3 + 0*X2 + 0*X2 = aug
            .... = resultX3

            coef*resultX3 + coef*X2 + 0*X1 = aug
            .... = resultX2

            coef*resultX3 + coef*resultX2 + coef*X1 = aug
            .... = resultX1

            result part works

            equation plug in only puts the last result not 'all of the above' last results
            """

            for columnIndex in range(columnTotal-2, -1, -1):
                coef = matrix[rIndex][columnIndex]
                resultsIndex = (columnTotal - 2) - columnIndex #has resultsIndex iterating backwards relative to columnIndex
                if resultsIndex < len(results):
                    printList += [f"{coef}*{results[resultsIndex]}"]
                else:
                    printList += [f"{coef}*{variables[columnIndex]}"]

            for i in range(len(printList)):
                if(i == 0):
                    equation += f"{printList[i]} "
                elif(i == len(printList)-1): 
                    equation += f" + {printList[i]} = {aug[augIndex]}"
                else:
                    equation += f" + {printList[i]}"
            equationList += [equation]
            file.write(f"{equation}\n")
            equation = ""
            printList = []

            #prints final algebra equation
            file.write(f"({aug[augIndex]} - {sum}) / {row[cIndex]} = {(aug[augIndex] - sum) / row[cIndex]}\n")
            results += [(aug[augIndex] - sum) / row[cIndex]]
            rIndex -= 1
            cIndex -= 1
            augIndex -= 1

    if infiniteSolution:
        # print(Fraction.from_float(2.5))
        letters = ["s", "t", "w",  "z", "a", "b", "c", "d"] #max null(free var)=8 because max matrix=9x9
        lettersIndex = 0
        matrixIS = matrix.astype(str)
        freeVarColumnIndex = []
        printList = []
        equationList = []
        equation = ""
        results = []
        rDisplayIndex = 2
        for i in range(rowTotal):
            if matrix[i,i] == 0:
                freeVarColumnIndex += [i]
        if not freeVarColumnIndex:
            for i in range(rowTotal,columnTotal-1):
                freeVarColumnIndex += [i]
        for index in range(-1,(1+len(freeVarColumnIndex))*-1,-1): #sets free variable (swapps old variable for free varable)
            file.write(f"let {variables[index]} = {letters[lettersIndex]}\n")
            variables[index] = letters[lettersIndex]
            results += [letters[lettersIndex]]
            lettersIndex += 1
        for rowIndex in range(rowTotal-1,-1,-1): #prints each equation with free variable in the correct place
            augment = matrix[rowIndex][columnTotal-1]
            row = matrix[rowIndex,:]
            file.write("\n")
            for columnIndex in range(columnTotal-2, -1,-1):
                coef = matrix[rowIndex][columnIndex]
                printList += [f"{coef}*{variables[columnIndex]}"]
            for i in range(len(printList)):
                if(i == 0):
                    equation += f"{printList[i]} "
                elif(i == len(printList)-1): 
                    equation += f" + {printList[i]} = {augment}"
                else:
                    equation += f" + {printList[i]}"
            equationList += [equation]
            file.write(f"{equation}\n")
            equation = ""
            printList = []
        
        #back substitution - not currently working
        """
            expected:
            test matrix 6
            66*s + 0*t + 4.000*X3 + 0*X2 + 0*X1 = 0
            (0 - 66*s) / 4.000 = X3

            9*s +5*t + -2.4*(0 -66*s/4.000) + 2.2*X2 = 0
            (0 - 9*s - 5*t - -2.4*(-66*s/4.000)) / 2.2 = X2

            10*s + -5*t + 1*X3 + 2*X2 + 5*X1 = 0
            (0 -10*s - -5*t - 1*(0 -66*s) - 2*((0 - 9*s - 5*t - -2.4*(-66*s/4.000)) / 2.2)) / 5 = X1
        
        sum = ""
        while (augIndex >= 0):
            row = matrix[rIndex]
            nonZeroRow = row[row != 0]
            condition = len(nonZeroRow)
            increment = 1
            if len(results) == 2:
                sum = f"{row[freeVarColumnIndex[0]]} - {row[freeVarColumnIndex[1]]}"
            while(condition > 2):
                sum += f" + {row[cIndex+increment]} * {results[-increment]}"
                condition -= 1
                increment += 1
            print()
            
            #prints equations with pluged in value 
            printList = []
            equationList = []
            equation = ""

            for columnIndex in range(columnTotal-2, -1, -1):
                coef = matrix[rIndex][columnIndex]
                resultsIndex = (columnTotal - 2) - columnIndex #has resultsIndex iterating backwards relative to columnIndex
                if resultsIndex < len(results):
                    printList += [f"{coef}*{results[resultsIndex]}"]
                else:
                    printList += [f"{coef}*{variables[columnIndex]}"]

            for i in range(len(printList)):
                if(i == 0):
                    equation += f"{printList[i]} "
                elif(i == len(printList)-1): 
                    equation += f" + {printList[i]} = {aug[augIndex]}"
                else:
                    equation += f" + {printList[i]}"
            equationList += [equation]
            print(equation)
            equation = ""
            printList = []

            #prints final algebra equation
            simplify = f"(({aug[augIndex]} - ({sum})) / {row[cIndex-2]})"
            simplify = re.sub(r"\b0\.0\b\*\b", "", simplify) # 0.0 *
            simplify = re.sub(r"\b\*\b0\.0", "", simplify) # * 0.0
            simplify = re.sub(r"\s-\s0\.0", "", simplify) # - 0.0
            simplify = re.sub(r"\b0\.0\s-\s", "", simplify) # 0.0 -
            simplify = re.sub(r"\s\+\s0\.0", "", simplify) # + 0.0
            simplify = re.sub(r"\b0\.0\s\+\s", "", simplify) # 0.0 +
            simplify = re.sub(r"-\s\(-\s", "", simplify) # double negative
            simplify = re.sub(r"\+\s-", "-", simplify) # redundant positive
            simplify = re.sub(r"\b1\.0\b\*\b", "", simplify) # 1.0 *
            simplify = re.sub(r"\b\*\b1\.0", "", simplify) # * 1.0
            while re.search(r"\((\d+\.\d)\)", simplify): #single digit wrapped in parentheses ex: ((77.0)) -> 77.0
                simplify = re.sub(r"\((\d+\.\d)\)", r"\1", simplify)
            print(f"{simplify} = {variables[rDisplayIndex]}")
            results += [simplify] 
            rDisplayIndex -= 1
            rIndex -= 1
            cIndex -= 1
            augIndex -= 1
            """

    # if not infiniteSolution: #doesnt work
    #     results.reverse()
    #     file.write("\n")
    #     for i in results:
    #         file.write(str(i), end=" ")
    # file.close()

# gaussian_elimination(testMatrix1)
gaussian_elimination(testMatrix2)
# gaussian_elimination(testMatrix3)
# gaussian_elimination(testMatrix4)
# gaussian_elimination(testMatrix5)
# gaussian_elimination(testMatrix6)
# gaussian_elimination(testMatrix7)

file = open("DisplayGuass.txt", "r")
print(file.read())
file.close()

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