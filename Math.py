import numpy as np
from fractions import Fraction
np.set_printoptions(precision=10, suppress=False)

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
                    width = max(len(str(num)) for row in matrix for num in row) + 1
                    for row in matrix:
                        file.write("| ")
                        file.write(f"{str(row[0])}")
                        for element in row[1:]:
                            file.write(f" {str(element):>{width}}")
                        file.write(" |\n")
                    break
                if column[index] == 0 and index == rowTotal-1 and pivotColumnIndex+1 < columnTotal:
                    file.write(f"no pivot in column {pivotColumnIndex+1}\n")
                    check_for_swap(file, matrix, rowTotal, columnTotal, pivotRowIndex, pivotColumnIndex+1)
        else:
            file.write(f"r{pivotRowIndex+1} <=> r{pivotOfOne+1}\n")
            matrix[[pivotRowIndex, pivotOfOne]] = matrix[[pivotOfOne, pivotRowIndex]]
            width = max(len(str(num)) for row in matrix for num in row) + 1
            for row in matrix:
                file.write("| ")
                file.write(f"{str(row[0])}")
                for element in row[1:]:
                    file.write(f" {str(element):>{width}}")
                file.write(" |\n")
    return matrix

def gaussian_elimination(matrix): #string input to handle fractions
    file = open("DisplayGuass.txt", "w")
    #PRINT ALL STEPS TO THE USER
    #only handling unique solutions, tell the user if no solutions (check for contradictions)

    try:
        matrix = np.vectorize(Fraction)(matrix)
    except ValueError:
        file.write("Not all elements are integers, decimals, or fractions. Try again.")
        return

    #matrix.shape returns dim(matrix) indexing it as 1 returns the number of columns
    columnTotal = matrix.shape[1] #includes augmented column*
    rowTotal = matrix.shape[0]

    #returns list of variable names X1, X2, ..., Xn n = totalColumns-1
    variables = []
    for columnIndex in range(1, columnTotal):
        variables += [f"X{columnIndex}"]
    file.writelines(f"{str(variables)}\n")
    width = max(len(str(num)) for row in matrix for num in row) + 1
    for row in matrix:
        file.write("| ")
        file.write(f"{str(row[0])}")
        for element in row[1:]:
            file.write(f" {str(element):>{width}}")
        file.write(" |\n")
    
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
                rowMultiplier = Fraction(column[indexR] / (pivot * -1)).limit_denominator(1000)
            else:
                rowMultiplier = 0
            for c in range(columnTotal):
                element = matrix[indexR][c]
                element += (matrix[pivotRowIndex][c] * rowMultiplier)
                matrix[indexR][c] = Fraction(element).limit_denominator(1000)
            if rowMultiplier != 0:
                file.write(f"{rowMultiplier} * r{pivotRowIndex+1} + r{indexR+1}\n") if rowMultiplier != 1 else file.write(f"r{pivotRowIndex+1} + r{indexR+1}\n")
                width = max(len(str(num)) for row in matrix for num in row) + 1
                for row in matrix:
                    file.write("| ")
                    file.write(f"{str(row[0])}")
                    for element in row[1:]:
                        file.write(f" {str(element):>{width}}")
                    file.write(" |\n")
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
    noSolution = False
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
            noSolution = True
            return 0
        
        #check for infinite solution
        allZeroRowMask = np.all(matrix == 0, axis=1)
        noZeroMatrixMask = ~allZeroRowMask
        matrix = matrix[noZeroMatrixMask] #masks remove all zero rows before checking for infinite solution
        columnTotal = matrix.shape[1] #includes augmented column*
        rowTotal = matrix.shape[0]
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
    aug = matrix[:,-1] 
    augIndex = len(aug)-1
    
    if not infiniteSolution:
        sum = 0
        while (augIndex >= 0):
            row = matrix[rIndex] 
            nonZeroRow = row[row != 0]
            if results:
                sum = 0
                for i in range(columnTotal-2, rIndex, -1):
                    sum += row[i] * results[(columnTotal-2) - i]

            file.write("\n")

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
            file.write(f"{equation}\n")
            equation = ""
            printList = []
            #prints final algebra equation
            file.write(f"({aug[augIndex]} - {sum}) / {row[rIndex]} = {(aug[augIndex] - sum) / row[rIndex]}\n")
            results += [(aug[augIndex] - sum) / row[rIndex]]
            rIndex -= 1            
            augIndex -= 1

    if not infiniteSolution:
        results.reverse()
        file.write("\n")
        for i in range(len(results)):
            file.write(f"{variables[i]} = {results[i]}  ")
    file.close()
    return matrix, infiniteSolution, noSolution