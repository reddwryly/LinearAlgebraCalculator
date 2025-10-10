import pygame, pygame_textinput

# imports needed files
from classTextbox import Textbox

''' PYGAME INFORMATION

* The origin (coords of 0,0) is the top left corner. Positive directions are right and down

* rectangle format goes pygame.draw.rect(screen, (color), (rectangle location))
    - color is RGB values, from (0, 0, 0) to (255, 255, 255) OR a simple string such as "white" or "red" or "dark blue"
    - rectangle location goes (x-coord, y-coord, width, height)
    - the "origin" of a rectangle or text box is its upper left corner

'''

# for the UI, the user needs to be able to click on specific matrix elements and enter their values
# they can also use their keyboard to navigate elements:
#   * TAB should move to the next element in the row
#   * ENTER should move to the next row?


#  *UI, windows for each calculator + menu/selector page 
#            -input for each element in the matrix (dynamic ammount depending on dim)
#            -shows each steps (math papa style)

'''
BUTTONS that will be needed:
* main menu
* solving mode - Gaussian or Gauss-Jordan
* reset elements
* reset dimensions
* 

'''

''' 
MATRICES' dimensions are in the format of (rows) X (columns)
for example, a 3x2 matrix has 3 rows and 2 columns
'''

# example code; replace with user entering dimensions in textboxes
numColumns = 2
numRows = 3

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1360, 765))
clock = pygame.time.Clock()
running = True

fontButtons = pygame.font.Font(None, 32)
fontDimensions = pygame.font.Font(None, 40)
fontMatrix = pygame.font.Font(None, 32)

''' USER INPUT '''
# is the library best for handling user text input
textInput = pygame_textinput.TextInputVisualizer(font_color = (255, 100, 0), font_object = fontDimensions)
# NOTE: access user input via textInput.value

# creates some textboxes on the screen. these ones are static and will not move
# these are where the user specifies the matrix size. these textboxes  take exactly 1 number
boxRows = Textbox(700, 60, 40, 40, fontDimensions, 1, "0123456789")
boxColumns = Textbox(810, 60, 40, 40, fontDimensions, 1, "0123456789")

# creates a list that will store all matrix textboxes
textboxes = []
textboxes.append(boxRows)
textboxes.append(boxColumns)

# code needs to establish a matrix based on the dimensions provided by user
#   * if there are lots of rows,there is a limit on the matrix size = 9x9

# function for creating the matrix based on user input
# numRows and numColumns will be the "textinput.value" for the dimensions textboxes,
# startX and startY are the starting x- and y-coords for the matrix
# width and height are the dimensions of each textbox
# spacing is the space in pixels between each column and row
matrixCreated = False
def createMatrix(numRows, numColumns, startX, startY, width, height, spacing):
    global textboxes
    totalTextboxes = (int(numRows) * int(numColumns))

    # iterates through the dimensions, creating textboxes
    # goes row by row, creating each entry then moving to the next row
    for r in range(numRows):
        # establishes the y-value for the current row being made
        y = startY + (r * spacing)

        for c in range(numColumns):

            # establishes the x-value for the textbox, incrementing the x-value to space them out on the row
            # because this creates the textboxes per row, they all have the same y-value
            # creates the textboxes with the provided values then appends them to the textboxes list to be displayed onscreen
            x = startX + (c * spacing)
            box = Textbox(x, y, width, height, fontMatrix, maxLength=7, allowedChars="0123456789/.")
            textboxes.append(box)
            


''' ### NECESSARY: DYNAMIC MATRIX TEXTBOX SPACING ###
This is necessary because if spacing is even all around, the vertical spacing is too much and 9 rows go off the page. horizontal
is too little and 9 columns end up touching. 
    # spacing is determined based on matrix size
    # vertical spacing needs to be small. horizontal spacing needs to be enough to hold all 9 columns, with each box being pretty wide
    verticalSpacing = 0
    horizontalSpacing = 0
    spacingIncrement = 0

    # textbox width is based on how many columns there are
    width = 0

    # textbox height is based on how many rows there are
    height = 0

    ### determines spacing, width and height ###
    # the loops for spacing make the spacing between 10 pixels (for 9 rows/columns) and 80 pixels (for 2 rows/columns)
    # if the max matrix size is 9x9, then imagine the spacing is the difference of 10 and number of rows/columns, times 10 pixels
    # for example, if the matrix is 3x6, then the spacing vertically should be (10-3) * 10 = 7 * 10 = 70 pixels
    # the horizontal spacing should be (10-6) * 10 = 4 * 10 = 40 pixels
    # code here

    # loops and creates every textbox needed until the right amount is created
    for i in range(totalTextboxes):
        y = startY + (i * spacing)
'''

# information for the rectangles and text - coords, dimensions, color

buttonMainCoords = (40, 40, 160, 80) # x-coord, y-coord, width, height
buttonMainColor = ("white")

areaMatrixCoords = (240, 0, 1120, 765)
areaMatrixColor = ("dark green")

textDimensionsCoords = (680, 20) # text coords are just x- and y-coords, no width and height needed
textDimensionsColor = ("coral")

buttonColumnsCoords = (620, 60, 80, 40)
buttonColumnsColor = ("white")



inputColumnsCoords = ()


while running:
    events = pygame.event.get()
    
    # textInput needs events every frame
    textInput.update(events)
    screen.blit(textInput.surface, (60, 80))
    

    for event in events:

            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                running = False

            
            elif event.type == pygame.MOUSEBUTTONDOWN: # if user clicks their mouse

                # stores the position of the mouse click
                pos = event.pos

                # Boolean for if the user has clicked on a textbox
                clickedAny = False
                if event.button == 1: # if the user clicks MB1 (left clicks)

                    # loops through each existing textbox to check if one was clicked
                    # if textbox is clicked, sets that textbox to be active
                    for textbox in textboxes:

                        # checks if the mouseclick is on a textbox
                        if textbox.clickedInside(pos):
                            textbox.active = True
                            clickedAny = True
                        else:
                            textbox.active = False

                    # deactivates all textboxes if user has clicked away from them all
                    if clickedAny == False:
                        for textbox in textboxes:
                            textbox.active = False

                    # checks if the matrix has already been created or not
                    if matrixCreated == False:
                        # if the matrix is not created, then it checks for values in the dimensions textboxes
                        if boxRows.textinput.value and boxColumns.textinput.value:
                            # these "final" values are just semi-permanent dimension values so the matrix doesn't always clear itself
                            finalColumnValue = int(boxColumns.textinput.value)
                            finalRowValue = int(boxRows.textinput.value)
                            
                            # creates the matrix with the input values
                            createMatrix(numRows=finalRowValue, numColumns=finalColumnValue, startX=250, startY=120,
                                         width=90, height=30, spacing=90)

                            # declares a matrix is created
                            matrixCreated = True
                    
                    # runs if the matrix has already been created
                    # the user can change their matrix at any time but it will (as of right now) replace it with a new one
                    else:
                        isDifferent = False
                        # checks if the current dimension values are different than what are saved
                        if (boxColumns.textinput.value != str(finalColumnValue)):
                            finalColumnValue = boxColumns.textinput.value
                            isDifferent = True                    
                        if (boxRows.textinput.value != str(finalRowValue)):
                            finalRowValue = boxRows.textinput.value
                            isDifferent = True
                        
                        # if the user changes the dimensions, then it creates a new matrix with those dimensions
                        if isDifferent == True:
                            createMatrix(finalRowValue, finalColumnValue, 250, 120, 90, 30, 50)

                    # if the main button is clicked on
                    if buttonMain.collidepoint(event.pos):
                        print("box successfully clicked!")

                ''' *** THIS CODE IS FOR PRESSING TAB AND ENTER ***
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        ### code for tabbing over one textbox (or going to next row if end of row)

                    elif event.key == pygame.K_RETURN:
                        ### code for pressing enter, moving to next row 
                '''
    
    # if a textbox is active, this will "handle events" AKA update the textbox with user text
    for textbox in textboxes:
        textbox.handleEvents(events)

    screen.fill("dark blue") # fills the screen with one color to clear it of last frame

    ### RECTANGLES ###
    # main menu button
    buttonMain = pygame.draw.rect(screen, buttonMainColor, buttonMainCoords)

    # the area (dark green) where the matrix boxes will be
    areaMatrix = pygame.draw.rect(screen, areaMatrixColor, areaMatrixCoords)

    ### TEXT ### 
    textMain = fontButtons.render("Main Menu", True, "black")
    screen.blit(textMain, (60, 70))

    textDimensions = fontDimensions.render("DIMENSIONS: ", True, textDimensionsColor)
    screen.blit(textDimensions, (textDimensionsCoords))

    textDimensionsCross = fontDimensions.render("X", True, textDimensionsColor)
    screen.blit(textDimensionsCross, (textDimensionsCoords[0] + 85, textDimensionsCoords[1] + 50))
       
    # draws all the textboxes
    for textbox in textboxes:
        textbox.draw(screen)

    # flip() the display to put  work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 30
    #print(textboxes)

pygame.quit()