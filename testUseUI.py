# imports pygame and python libraries
import pygame, pygame_textinput, copy

# imports custom files
from classTextbox import Textbox
import data, methods

''' Accesses data from data.py (see file for details), methods from methods.py '''

''' PYGAME INFORMATION

* The origin (coords of 0,0) is the top left corner. Positive directions are right and down

* rectangle format goes pygame.draw.rect(screen, (color), (rectangle location))
    - color is RGB values, from (0, 0, 0) to (255, 255, 255) OR a simple string such as "white" or "red" or "dark blue"
    - rectangle location goes (x-coord, y-coord, width, height)
    - the "origin" of a rectangle or text box is its upper left corner

'''
''' FILE LAYOUT (OLD)
[pygame initialization]
[button and text data (coords, color, sizes) ]
[user input initialization - pygame textinput, dimension textboxes, value lists]
[functions]
[MAIN LOOP:
    * updates every frame and checks events
        - key presses, textbox updates, matrix creation and updates, matrix navigation
    * update all textboxes, rectangles, and text
    * updates the frame 
]
'''





# for the UI, the user needs to be able to click on specific matrix elements and enter their values
# they can also use their keyboard to navigate elements:
#   * TAB should move to the next element in the row
#   * ENTER should move to the next row
#   * if have time, TAB + ENTER should move exactly one row down, same column


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

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1360, 765))
clock = pygame.time.Clock()
running = True

# fonts for different texts. first parameter is font, second is size
fontButtons = pygame.font.Font(None, 32)
fontButtonsSmaller = pygame.font.Font(None, 29)
fontDimensions = pygame.font.Font(None, 40)
fontMatrix = pygame.font.Font(None, 32)

textInput = data.textInput

''' BUTTONS '''
buttonList = data.buttons
''' ###### CODE HERE ###### '''

''' ### OPTIONAL: DYNAMIC MATRIX TEXTBOX SPACING ###

    ### OPTIONAL: spacing is determined based on matrix size ###
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



''' ####### MAIN PYGAME LOOP ####### '''
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

                    # calls functions that handle if textboxes and buttons are clicked on
                    # if a textbox is clicked on, it is automatically set to be active
                    methods.areTextboxesActive(event)

                    # returns values if buttons are clicked on
                    clickResult = methods.checkClickedAny(buttonList, event)

                    # if the user clicks, but no textbox was clicked on, updates matrix size if changed
                    if clickResult == False:
                        methods.changeMatrixSize()
                    
                    # else, if the user clicks and they clicked on a button:
                    else:
                        methods.buttonClicked(clickResult, buttonList)
                    
                                

                ''' *** THIS CODE IS FOR PRESSING TAB AND ENTER ***
                # user can press tab to navigate textboxes, left -> right and top to bottom like a book
                # each textbox records its row and column, which are used for this navigation
                '''

                '''
                The code checks for which textbox is currently active. It then gets the row and column of that box.
                When TAB or ENTER or pressed, the textbox deactivates and the NEXT textbox becomes active
                However, if the last textbox in the whole matrix is active and TAB or ENTER are pressed, all textboxes deactivate
                Also, the user currently cannot press TAB or ENTER for the dimensions textboxes. this can be fixed
                '''
            # executes if the user presses a key
            elif event.type == pygame.KEYDOWN:

                # checks if the key that was pressed is TAB or ENTER
                if event.key == pygame.K_TAB or event.key == pygame.K_RETURN:

                    # gathers active textbox info (index, row, column) or returns False
                    activeInfo = methods.gatherActiveTextboxInfo()

                    # if there is an active textbox:
                    if activeInfo != False:
                        # if the user pressed TAB:
                        if event.key == pygame.K_TAB:
                            methods.tab(activeInfo)

                        # else if the user presses ENTER
                        elif event.key == pygame.K_RETURN:
                            methods.enter(activeInfo)

                
    
    # if a textbox is active, this will "handle events" AKA update the textbox with user text
    # the "updates" will update the text in them.
    #   - this is a little redundant in some places, but this guarantees all textboxes display live values 
    for textbox in data.textboxes:
        textbox.handleEvents(events)
        textbox.textinput.update([])
    for textbox in data.matrixTextboxes:
        textbox.handleEvents(events)
        textbox.textinput.update([])

    screen.fill("dark blue") # fills the screen with one color to clear it of last frame

    ''' RECTANGLES and BUTTONS '''
    # main menu button
    buttonMain = pygame.draw.rect(screen, data.buttonColor, data.buttonMainCoords)
    methods.addToButtons(buttonMain, buttonList)

    # "Clear Matrix" button
    buttonClearMatrix = pygame.draw.rect(screen, data.buttonColor, data.buttonClearMatrixCoords)
    methods.addToButtons(buttonClearMatrix, buttonList)

    # "Fill with Zeroes" button
    buttonFillWithZeroes = pygame.draw.rect(screen, data.buttonColor, data.buttonFillWithZeroesCoords)
    methods.addToButtons(buttonFillWithZeroes, buttonList)

    # the area (dark green) where the matrix boxes will be
    areaMatrix = pygame.draw.rect(screen, data.areaMatrixColor, data.areaMatrixCoords)
    

    ### TEXT ### 
    textDimensions = fontDimensions.render("DIMENSIONS: ", True, data.textDimensionsColor)
    screen.blit(textDimensions, (data.textDimensionsCoords))

    textDimensionsCross = fontDimensions.render("X", True, data.textDimensionsColor)
    screen.blit(textDimensionsCross, (data.textDimensionsCoords[0] + 85, data.textDimensionsCoords[1] + 50))

    textMain = fontButtons.render("Main Menu", True, "black")
    screen.blit(textMain, (60, 70))

    textClearMatrix = fontButtons.render("Clear Matrix", True, "red")
    screen.blit(textClearMatrix, (50, 190))
    
    textFillWithZeroes = fontButtonsSmaller.render("Fill with Zeroes", True, "black")
    screen.blit(textFillWithZeroes, (48, 310))

    # draws all the textboxes and updates active cursors
    for textbox in data.textboxes:
        textbox.draw(screen)
        textbox.checkCursor()
    for textbox in data.matrixTextboxes:
        textbox.draw(screen)
        textbox.checkCursor()

    # flip() the display to put work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 30

pygame.quit()