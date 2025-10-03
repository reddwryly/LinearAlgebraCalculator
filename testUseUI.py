import pygame, pygame_textinput

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

# example code; replace with importing from other files
numColumns = 2
numRows = 3

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1360, 765))
clock = pygame.time.Clock()
running = True

fontButtons = pygame.font.Font(None, 32)
fontDimensions = pygame.font.Font(None, 40)

''' USER INPUT '''
# is the library best for handling user text input
textInput = pygame_textinput.TextInputVisualizer(font_color = (255, 100, 0), font_object = fontDimensions)
# NOTE: access user input via textInput.value


# needs to click on box, and start typing to enter in that box. when clicked elsewhere, or enter, or escape, then exit typing
activeTyping = False # if the user is actively typing
inputColumns = "" # what the user inputs for number of columns
inputRows = "" # user input for number of rows

# code needs to establish a matrix based on the dimensions provided by user
# perhaps the width of the matrix itself shall stay the same;
#   * more rows will be appended as needed
#   * the columns will get closer together and be smaller the more there are
#   * if there are lots of rows, what should happen? should:
#       - the user be able to scroll?
#       - there be a limit on maximum equations?
#       - the matrix resizes itself to fit the screen?

# information for the rectangles and text - coords, dimensions, color
# creates a list storing all textboxes
listTextboxes = []
activeTextbox = ""

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
              
            # checks if the user is actively typing something
            elif activeTyping == False:
            
                if event.type == pygame.MOUSEBUTTONDOWN: # if user clicks their mouse
                    if event.button == 1: # if the user clicks MB1 (left clicks)

                        # loops through each existing textbox to check if one was clicked
                        for textbox in listTextboxes:
                            if textbox.collidepoint(event.pos): 
                                print("textbox clicked")
                                activeTyping = True
                                activeTextbox = textbox
                                

                        # if the main button is clicked on
                        if buttonMain.collidepoint(event.pos): # if the button collides, at a point, with the event position (which is the click)
                            print("box successfully clicked!")
                        
                        # if the columns button is clicked
                        elif buttonColumns.collidepoint(event.pos):
                            buttonColumnsColor = ("dark gray")
                            activeTyping = True
                            continue
    
    # executes if activeTyping == True, AKA when the user has clicked on a text box to enter a value into
            #else:
                
        # needs to loop through and figure out which text box the user clicked on
        # best way to do this is likely storing all buttons in a list, then using a for-loop to check if the button collides with click


    screen.fill("dark blue") # fills the screen with one color to clear it of last frame

    ### RECTANGLES ###
    # main menu button
    buttonMain = pygame.draw.rect(screen, buttonMainColor, buttonMainCoords)

    # the area (dark green) where the matrix boxes will be
    areaMatrix = pygame.draw.rect(screen, areaMatrixColor, areaMatrixCoords)

    # the textbox button for column entry
    buttonColumns = pygame.draw.rect(screen, buttonColumnsColor, buttonColumnsCoords)
    if buttonColumns not in listTextboxes:
        listTextboxes.append(buttonColumns)


    ### TEXT ### 
    textMain = fontButtons.render("Main Menu", True, "black")
    screen.blit(textMain, (60, 70))

    textDimensions = fontDimensions.render("DIMENSIONS: ", True, textDimensionsColor)
    screen.blit(textDimensions, (textDimensionsCoords))



    # flip() the display to put  work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 30
    print(listTextboxes)


pygame.quit()