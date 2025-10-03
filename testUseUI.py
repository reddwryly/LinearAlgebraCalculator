import pygame

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

'''

# example code; replace with importing from other files
numColumns = 2
numRows = 3

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 32)

# code needs to establish a matrix based on the dimensions provided by user
# perhaps the width of the matrix itself shall stay the same;
#   * more rows will be appended as needed
#   * the columns will get closer together and be smaller the more there are
#   * if there are lots of rows, what should happen? should:
#       - the user be able to scroll?
#       - there be a limit on maximum equations?
#       - the matrix resizes itself to fit the screen?


buttonMainCoords = (40, 40, 160, 80) # x-coord, y-coord, width, height
buttonMainColor = ("white")
areaMatrix = ()


while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN: # if user clicks their mouse
            if event.button == 1: # if the user clicks MB1 (left clicks)

                # if the box is clicked on
                if buttonMain.collidepoint(event.pos): # if the box collides, at a point, with the event position (which is the click)
                    print("box successfully clicked!")

    screen.fill("dark blue") # fills the screen with one color to clear it of last frame
    buttonMain = pygame.draw.rect(screen, buttonMainColor, buttonMainCoords)
    textMain = font.render("Main Menu", True, "black")
    screen.blit(textMain, (60, 70))


    # flip() the display to put  work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()