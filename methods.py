''' METHODS to use for main file '''
from classTextbox import Textbox
import data, copy, pygame
fontMatrix = data.fontMatrix



'''--- FUNCTIONS ---'''
# code needs to establish a matrix based on the dimensions provided by user
#   * if there are lots of rows,there is a limit on the matrix size = 9x9

# function for creating the matrix based on user input
# numRows and numColumns will be the "textinput.value" for the dimensions textboxes,
# startX and startY are the starting x- and y-coords for the matrix
# width and height are the dimensions of each textbox
# spacing is the space between boxes in pixels. by default, good values for x- and y-spacing are 120 and 60
matrixCreated = False
def createMatrix(numRows, numColumns, startX, startY, width, height, xSpacing, ySpacing):

    # iterates through the dimensions, creating textboxes
    # goes row by row, creating each entry then moving to the next row
    for r in range(numRows):

        # establishes the y-value for the current row being made, changing by a multiple of spacing
        y = startY + (r * ySpacing)
        for c in range(numColumns):

            # establishes the x-value for the textbox, incrementing the x-value to space them out on the row
            # because this creates the textboxes per row, they all have the same y-value
            x = startX + (c * xSpacing)

            # creates the textboxes with the provided values then appends them to the textboxes list to be displayed onscreen
            # "row" and "column" are the textbox's row and column coords; the +1 is needed because of the for-in-range loops
            box = Textbox(x, y, width, height, fontMatrix, row=r+1, column=c+1, maxLength=7, allowedChars="0123456789/.")
            data.matrixTextboxes.append(box)
'''#########################################'''

# gathers and stores all matrix textbox entries
# should be called when trying to solve matrix, or when updating matrix size
def storeValues():
    print("Initial:", data.matrixValues)

    ''' ONLY executes when there are matrix textboxes existing '''
    if data.matrixTextboxes:
        # matrixTextboxes is the list of all matrix textboxes, tempList is the tempList used to create it (technically the active row),
        # and matrixValues is the master 2D list of values
        tempList = []

        
        # clears the lists used to make room for new values
        data.matrixValues.clear()
        tempList.clear()

        # with the lists cleared, it adds the appropriate amount of rows and columns depending on the dimensions
        targetColumns = int(data.boxColumns.textinput.value)
        currentColumns = 0
        
        # assigns the number of elements to tempList; this is how many columns there are
        # for example, four columns will make tempList be ["", "", "", ""]
        while currentColumns < targetColumns:
            tempList.append("")
            currentColumns += 1

        print("tempList:", tempList)

        targetRows = int(data.boxRows.textinput.value)
        currentRows = 0

        # adds the appropriate amount of rows to the master list
        while currentRows < targetRows:
            data.matrixValues.append(tempList)
            currentRows += 1

        print("Master list: ", data.matrixValues)


        # now that the master list is created to be the same dimension as matrix, stores the matrix values according to row and column
        for textbox in data.matrixTextboxes:
            value = textbox.textinput.value

            # uses the textbox position to set each master list element to the right value
            print(textbox.row, textbox.column)
            print(data.matrixValues)
            data.matrixValues[(textbox.row - 1)][(textbox.column - 1)] = int(value)



'''#########################################'''

# clears all matrix elements, setting textboxes to empty
def clearMatrix():

    # iterates through all matrix textboxes, clearing their values
    for textbox in data.matrixTextboxes:
        textbox.textinput.value =("")
        textbox.textinput.update([])

'''#########################################'''

# is called when the user clicks on the "Fill with Zeroes" button
# iterates through all matrix textboxes, filling empty ones with zero
def fillWithZeroes():

    # iterates through every matrix textbox. if empty, fill with zero
    for textbox in data.matrixTextboxes:
        if textbox.textinput.value == "":
            textbox.textinput.value = "0"


'''#########################################'''

# is called when the user tries to solve their matrix
# fills empty entries with zero and then proceeds with a solving method
def solveMatrix(method):

    # calls the zero-fill function to complete the matrix
    fillWithZeroes()

    # executes a method to execute with based off of the selected method

'''#########################################'''

# changes matrix dimensions. checks if and executes when dimension values change
def changeMatrixSize():
    global boxColumns, boxRows
    print(data.matrixValues)

    savedRows = int(data.savedRows)
    savedColumns = int(data.savedColumns)

    # flags to indicate if rows or columns are being added or removed
    addSize = False
    removeSize = False

    storeValues()

    # checks if a matrix has already been created. if not created, do nothing
    # savedColumns or Rows is what is stored from the last textbox value check (the old value)
    # in data.py, textboxes[0] and textboxes[1] are the Rows and Columns textboxes respectively
    # these values ^ should be the live (possibly new) values
    numRows = data.textboxes[0].textinput.value
    numColumns = data.textboxes[1].textinput.value

    if data.matrixCreated:
        # checks if the user has updated the dimensions values. does nothing if no change, executes if there is
        if (int(savedColumns) == int(numColumns)) and (int(savedRows) == int(numRows)):
            pass

        # else, if the user has changed either the columns or dimensions:
        else:
            print("Matrix changed.")
            print("Saved rows, columns: ", savedRows, savedColumns)
            print("New rows, columns: ", numRows, numColumns)
            storeValues()

            # runs if the matrix has already been created
            # the user can change their matrix at any time
            isDifferent = False

            # checks if the current dimension values are different than what are saved
            if (boxColumns.textinput.value != str(savedColumns)):
                print("Columns different")
                savedColumns = int(boxColumns.textinput.value)
                isDifferent = True                    
            if (boxRows.textinput.value != str(savedRows)):
                print("Rows different")
                savedRows = int(boxRows.textinput.value)
                isDifferent = True
            
            # if the user changes the dimensions, then it deletes the old matrix & creates a new matrix with new dimensions
            # needs to compare stored matrix textboxes to the new ones. those that remain must carry their values over
            if isDifferent == True:
                print("Deleting old matrix...")
                print("creating new matrix...")

                # a copy of the matrix textbox list is made here before the new matrix is created
                matrixCopy = data.matrixTextboxes

                # removes the old matrix textboxes here then creates new ones
                data.matrixTextboxes = []
                createMatrix(savedRows, savedColumns, 250, 120, 100, 30, 110, 45)

                # once the new matrix has been created, compares new and old textboxes to carry over applicable old values
                # the row and column of each textbox just need to be the same
                for textbox in data.matrixTextboxes:
                    for oldBox in matrixCopy:
                        if textbox.row == oldBox.row and textbox.column == oldBox.column:
                            
                            # if textboxes match row and column, the new textbox carries the same value
                            textbox.textinput.value = oldBox.textinput.value

                data.savedRows = numRows
                data.savedColumns = numColumns
            

            
     
'''#########################################'''

# adds buttons to the main list of buttons if they aren't in already
# in data.py, there is a list called buttons. buttonList should be data.py.buttons? when called in main 
# to be called every frame update to add buttons to the list. if nothing changes, no buttons get added
def addToButtons(button, buttonList):
    # a flag to check if the button to add is in the list or not 
    isInList = False 

    # iterates the buttonList to check if button is in list. sets flag to True if button is already in list
    for item in buttonList:
        if button == item:
            isInList = True
    
    # once the loop is complete, if the button is not in the list, then add it to the list
    if isInList == False:
        buttonList.append(button)

'''#########################################'''

# activates any textbox that is clicked on
# called by the method "checkClickedAny"
def areTextboxesActive(click):
    clickedAny = False
    for textbox in data.textboxes:
        # if textbox is clicked, sets that textbox to be active
        if textbox.clickedInside(click.pos):
            textbox.active = True
            clickedAny = True

        else:
            textbox.active = False

    for textbox in data.matrixTextboxes:
        if textbox.clickedInside(click.pos):
            textbox.active = True
            clickedAny = True
        else:
            textbox.active = False
    
    return clickedAny

'''#########################################'''

# returns true or false depending on if the user clicks on any textbox or button
# is called when the user clicks their mouse
# upon user clicks, this function is called and will return: False, button.topleft, or will create a matrix if not already created
# will also activate and deactivate textboxes per click as needed
def checkClickedAny(buttonList, click):
    # first, calls method to check if textboxes have been clicked on
    if areTextboxesActive(click) == False:
        
        # once the user has clicked away and deactivated all textboxes:
        # checks if the matrix has already been created or not
        if data.matrixCreated == False:
            # if the matrix is not created, then it checks for values in the dimensions textboxes
            if data.boxRows.textinput.value and data.boxColumns.textinput.value:
                # these "saved" values are just semi-permanent dimension values so the matrix doesn't always clear itself
                savedColumnValue = int(data.boxColumns.textinput.value)
                savedRowValue = int(data.boxRows.textinput.value)
                
                # creates the matrix with the input values
                createMatrix(numRows=savedRowValue, numColumns=savedColumnValue, startX=250, startY=120,
                                width=100, height=30, xSpacing=110, ySpacing=45)

                # declares a matrix is created
                data.matrixCreated = True

                # updates the saved dimensions values with the first matrix creation
                data.savedRows = data.boxRows.textinput.value
                data.savedColumns = data.boxColumns.textinput.value
        
    # returns an identifer (button location) whenever button is clicked 
    for button in buttonList:
        if button.collidepoint(click.pos):
            return button.topleft
    
    # if no button was clicked on, returns False
    else:
        return False

'''#########################################'''

# called when " checkClickedAny() " is not False (a button is clicked on)
# in the main loop, a global variable is declared when checkClickedAny() is called. that variable is used for this
# for now, it is called clickResult, which should be passed into clickID. it is either False or a button.topleft
# executes a function depending on the button that is clicked
# ALL buttons have a relatively UNIQUE identifier to them - their coords. for simplicity this is each button's topLeft
# clickID should be a button's topLeft, as pygame also recognizes a rectangle's location as its topLeft
def buttonClicked(clickID, buttonList, screen):
    
    # activeButton is the button that is confirmed to be clicked, through loop iteration of the clickID
    # index comes from this - in the main loop, buttons are appended to the buttonList in this order:
    '''
    buttonMain
    buttonClearMatrix
    buttonFillWithZeroes
    buttonSolveGaussian

    '''
    # iterates through the button list, gathering the index of which button was clicked
    # compares each button's topleft to the clickID to check for a match
    activeButtonIndex = 0
    while activeButtonIndex < len(buttonList):
        if buttonList[activeButtonIndex].topleft == clickID:
            break
        else:
            activeButtonIndex += 1
    
    # iterates through all button names, calling the appropiate function for them using the order above
    if activeButtonIndex == 0:
        clearMatrix()
    
    elif activeButtonIndex == 1:
        clearMatrix()
    
    elif activeButtonIndex == 2:
        fillWithZeroes()

    # if a Solve button is clicked, it calls the functions needed to create and show the solving panel
    elif activeButtonIndex == 3:
        
        # all Solve methods must fill empty slots with zeroes before starting
        fillWithZeroes()
        createSurface()

''' ***************************************************************************** '''

# onKeyPress() is called when the user presses TAB or ENTER
# it sets up data necessary for the tab() and enter() functions
def gatherActiveTextboxInfo():
    # iterates through all textboxes to find which one is active. uses an index incrementer to track which is active
    # (so the next one can be activated)
    activeIndex = 0

    # gets the active textbox's index, including its column and row
    for textbox in data.matrixTextboxes:
        if textbox.active:
            break
        else:
            activeIndex += 1
    
    # once the list has been iterated, if there is an active textbox (checked by index value), then gather its row and column
    if activeIndex < len(data.matrixTextboxes):
        activeRow = data.matrixTextboxes[activeIndex].row
        activeColumn = data.matrixTextboxes[activeIndex].column

        # also checks and returns a variable if the textbox is in the last column or row
        # in data.textboxes, the rows box is first and the columns box is second
        isAtEndColumn = False
        if activeColumn == int(data.textboxes[1].textinput.value):
            isAtEndColumn = True
        
        isAtEndRow = False
        if activeRow == int(data.textboxes[0].textinput.value):
            isAtEndRow = True


        # function is complete. return the textbox index, row, column, and if at matrix edges if active
        return (activeIndex, activeRow, activeColumn, isAtEndRow, isAtEndColumn)

    # if there is no active textbox on keypress, then return False
    return False

''' ***************************************************************************** '''

# functions for the user pressing TAB and ENTER, called when gatherActiveTextboxInfo() returns NOT False
# both functions will exit the matrix if last textbox is active (or last row for ENTER)

# TAB will move to the next textbox (one to the right, or beginning of next row)
# there will be a variable in main.py set to the gatherActiveTextboxInfo() results. is passed into tab() as "info"
def tab(info):
    index = info[0]
    
    # deactivates the current textbox
    data.matrixTextboxes[index].active = False

    # if the active textbox is not in the last row and last column:
    if info[3] == False or info[4] == False:

        # activates next textbox
        index += 1
        data.matrixTextboxes[index].active = True

    # else, textbox is in last row and column. active textbox already deactivated

# ENTER function
def enter(info):
    # needs to move the active textbox to the first of the next row
    activeRow = info[1]
    nextRow = activeRow + 1
    index = info[0]

    # deactivates the current textbox
    data.matrixTextboxes[index].active = False
    
    # if active textbox is not in last row:
    if info[3] == False:
        # starts iterating through matrix textboxes from active textbox until it reaches the first of the next row
        index += 1
        while activeRow != nextRow:
            if data.matrixTextboxes[index].row == nextRow:
                activeRow = nextRow
            else:
                index += 1
        
        # once the next row has been acquired, sets that textbox to be active. the current index value should be the right textbox
        data.matrixTextboxes[index].active = True
    
    # else, the textbox is in the last row, and it is already deactivated


''' SOLVING SURFACE/PANEL '''
# this code is for creating, calling, and updating the surface that displays when the user tries to solve their matrix
# when the user clicks "Solve", the surface is created (in main loop, surface is displayed every refresh)
# all panel data is stored in data.py

''' Panel Code Notes '''
# pygame visual workflow: child objects --> drawn to surface --> blitted to screen --> screen/display is flipped
# for example: rectangle object created --> drawn to panel surface --> panel blitted to screen --> screen flipped in main loop
# DRAWING != BLITTING:
# "draw" doesn't actually display data on screen, it puts that data in an image. the image is blitted to the screen
# "blit" actually displays data on screen

def createSurface():
    # pygame.Surface((length, width))
    panel = pygame.Surface((data.panelLength, data.panelWidth))

    # once panel has been created, appends it to data.panel[] for the main loop
    data.panelList.append(panel)


# draws the panel border every frame
def drawPanelBorder(surface):
    # info
    panel = surface
    borderColor = data.borderColor
    rectValue = panel.get_rect()
    
    # draws border and color to the panel surface
    pygame.draw.rect(surface=panel, color=borderColor, rect=rectValue, width=data.borderWidth)

    test = data.panelFont.render("Test", True, borderColor)

# on top of the background, draws/prerenders the rest of the items that are needed
# needs to add matrix values, solutions
def drawPanelItems():
    # info
    userMatrix = data.matrixValues
    color = data.panelFontColor
    ''' CODE to PULL from SOLUTION FILE here '''

    # draws the matrix values:
    # iterates through every matrix value, rendering it to a surface then appending those surfaces to a list
    print(data.matrixValues)
    for row in userMatrix:
        for item in row:
            value = str(item) # each "value" is a matrix value input by the user
            valueSurface = data.panelFont.render(value, True, color) # renders the value 

            # appends the rendered text surfaces to a list; these will be blitted later
            data.surfacesValuesRendered.append(valueSurface)
            
    # draws the solving text
    ''' code that draws data from the solution file, already gathered above '''

# blits matrix text to the screen or panel surface
# recap: iterates through each text surface, blitting them. adjusts spacing for the text on each iteration
def blitMatrixText(targetSurface):
    # info
    xSpacing = 5 # horizontal spacing of text
    ySpacing = 5 # vertical spacing of text
    location = (50, 20) # active location to blit text. initial value here is starting point

    # iterates through all the text surfaces, blitting them
    for surfaceText in data.surfacesValuesRendered:

        # blits the text to the screen
        targetSurface.blit(surfaceText, location)

        # adjusts spacing (the spacing itself remains the same; is used to move text as desrired)
        xSpacing += 5
        ySpacing += 5

        # updates the location with the spacing increments. also needs to convert to list and back to change tuple values
        location = list(location)
        location[0] += xSpacing
        location[1] += ySpacing
        location = tuple(location)

# blits the panel surface and info to the main screen
def blitSurface(screen):
    # gets the panel Surface from data.py, created by createSurface()
    ''' the panel HAS to be ready FIRST, then everything is drawn to it, then the panel is blitted '''
    panel = data.panelList[0]
    panel.fill(data.panelColor)
    drawPanelBorder(panel)

    # blits the panel information
    blitMatrixText(panel)



    ''' BLITS the panel LAST because everything must be drawn to the panel first '''
    screen.blit(panel, (0, 0)) # panel will be on the left side, so it starts topLeft at (0, 0)

    ''' code for solving matrix goes here '''
    ''' the code is pulled from another function that prerenders it '''