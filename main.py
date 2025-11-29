import numpy as np, copy

"""
ideas for expanding this project:
    *ui for maxrix value entry
    *differnt pages for differnt calculators (like the calculator websites!!)
    *have guassian(/jordan) elimination work for infinite solutions (solve parametrically)
"""
# variables
tempList = [] # the active row of values being entered; only temporarily stored, then cleared for the next row
masterList = [] # the list that will contain the other lists (other rows). will be turned into array

def menu():
    #any non-int input should bring you back to menu at any time

    #loop for menu
    print("""\nSystem of Equations using Matrix Calculator *Showing Steps* \n----------------------------------------------------------
1.) Guassian Elimination \n2.) Guasian-Jordan Elimination \n3.) Matrix Multiplication \n4.) Exit\n""")


#start with multiplication to get a better understanding of indexing**
#################################



# checks the user input to see if it's numeric or otherwise (to go back to menu)
def checkInput(string):
    # declares variables that will be used if the input is a fraction
    numerator = 0.0
    numeratorString = ""
    denominator = 0.0
    denominatorString = ""
    passedDivision = False # Boolean to tell if we're still on the numerator or denominator
    letterDetected = False # Boolean to tell if the user has entered a letter/non-usable symbol

    # checks if the string is entirely numbers
    if string.isdigit() == True:
        output = float(string)
        return output
    
    # if the string is not entirely numbers, then it checks for special symbols, like the division sign "/" for fractions
    else:

        
        # checks if the user enters a character that is neither a fraction slash nor a number
        for character in string:
            if character != "/" and character.isdigit() == False:
                letterDetected = True
                return menu()
                if letterDetected == True:
                    pass

                
            
            # if there is no letter/bad symbol in the input, then the user has to have entered numbers with a fraction slash
            else:
                # a float that contains "/" will automatically perform the division,
                # BUT it has to be a float data type, not a string.
                # a string containing "/" will not be instantly converted to float so it must be done here

                # this iterates through the input and performs the fractional division to make the number a float
                # the float is used only for computer and calculation purposes. 
                # the value should still be stored as a fraction - the original string - to display to the user

                # there is no need to check for other characters or input validation here, as that has already been done
                if character != "/" and passedDivision == False: # if the character is not "/" and we're still in the numerator
                    numeratorString += character
                elif character == "/": # if the character is "/" then it marks that we have reached the denominator
                    passedDivision = True
                else:
                    denominatorString += character # this executes when we are in the denominator
                    
                # once all the characters have been parsed and the numerators and denominators are filled, it executes the division.
                # code here


        numerator = float(numeratorString)
        denominator = float(denominatorString)
        output = float(numerator/denominator)
    return output

# takes user input and appends it to the tempList (the current row)
def addToList(string):
    global tempList
    tempList.append(string)

def get_matrix_from_user():
    global tempList, masterList

    targetRows = int(input("How many rows/equations do you have: ")) # the number of rows needed
    currentRows = 0 # the current amount of rows complete
    targetVariables = int(input("How many variables do you have?\nRemember the equation's right-side has no variables: ")) # the target number of vars/columns
    
    while currentRows < targetRows: # while the current number of completed rows is less than the target rows:
        tempList.clear() # clears the temp list (current row) for each new row being entered
        currentVariables = 0 # the number of variable coefficients entered for the current row
        print("Enter a non-number at any time to go back to the main menu.")
        
        while currentVariables < targetVariables: # asks for input for each variable coefficient until all are met
            inputVariable = input("enter value: ")
            checkInput(inputVariable)
            addToList(inputVariable) # adds the current var coefficient to the tempList/current row
            currentVariables += 1 # increments the number of vars complete on this row
        
        answer = input("Enter the answer (right side) for this row: ") # once all the vars have values, the right side is entered
        checkInput(answer)
        addToList(answer)
        masterList.append(copy.deepcopy(tempList)) # adds the temporary list (the current row) to the master list (the matrix)
        currentRows += 1 # increments the total completed rows by 1 until all rows are entered
    #return an array called matrix 

    matrix = np.array(masterList) 
    return matrix

print(get_matrix_from_user())