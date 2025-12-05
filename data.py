''' DATA '''
''' Contains variables, lists, pygame objects (like rectangles/buttons), textboxes '''
import pygame, pygame_textinput, copy

# imports needed files
from classTextbox import Textbox

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1360, 765))
clock = pygame.time.Clock()
running = True
newSurface = False

# fonts for different texts. first parameter is font, second is size
fontButtons = pygame.font.Font(None, 32)
fontButtonsSmaller = pygame.font.Font(None, 29)
fontDimensions = pygame.font.Font(None, 40)
fontMatrix = pygame.font.Font(None, 32)

''' --- ESTABLISHING buttons and text --- '''
# information for the rectangles and text - coords, dimensions, color
# x-coord, y-coord, width, height
buttonColor = ("white")

# BUTTON coords
buttonX = 40
buttonWidth = 160
buttonHeight = 80
solveX = 250

buttonMainCoords = (buttonX, 40, buttonWidth, buttonHeight)
buttonClearMatrixCoords = (buttonX, 160, buttonWidth, buttonHeight)
buttonFillWithZeroesCoords = (buttonX, 280, buttonWidth, buttonHeight)
buttonGaussianCoords = (solveX, 600, buttonWidth, buttonHeight)

# green background of matrix
areaMatrixCoords = (240, 0, 1120, 765)
areaMatrixColor = ("dark green")

# data for dimensions boxes
textDimensionsCoords = (680, 20) # text coords are just x- and y-coords, no width and height needed
textDimensionsColor = ("coral")
buttonColumnsCoords = (620, 60, 80, 40)
buttonColumnsColor = ("white")

# creates a list to store all the buttons
buttons = []

'''--- USER INPUT ---'''
# is the library best for handling user text input
textInput = pygame_textinput.TextInputVisualizer(font_color = (255, 100, 0), font_object = fontDimensions)
# NOTE: access user input via textInput.value

# creates some textboxes on the screen. these ones are static and will not move
# these are where the user specifies the matrix size. these textboxes  take exactly 1 number
boxRows = Textbox(700, 60, 40, 40, fontDimensions, row=None, column=None, maxLength=1, allowedChars="0123456789")
boxColumns = Textbox(810, 60, 40, 40, fontDimensions, row=None, column=None, maxLength= 1, allowedChars="0123456789")

# the saved and stored values for the matrix dimensions
savedRows = "0"
savedColumns = "0"

# creates a list that will store all non-matrix textboxes
# the input for dimensions will be the first two boxes (indices 0 and 1) in order of rows and columns. 
# every other box past it is part of the matrix
textboxes = []
textboxes.append(boxRows)
textboxes.append(boxColumns)

# creates a list storing all matrix textboxes
matrixTextboxes = []

# creates a list storing matrix values
matrixValues = []
tempList = [] # used to create the 2D list/array

# a flag to determine if the matrix is created or not
matrixCreated = False

# activeRow is the current row being modified in the 2D list, used for methods.storeValues()
activeRow = 1

# panel[] is the list that contains the panel that displays when solving
# this is just data validation code; only one panel should be in here

panelList = []

''' Panel Info '''
# pygame.Surface((panelLength, panelWidth))
panelLength = 600
panelWidth = 765
borderWidth = 10

# color
panelColor = ((0, 20, 60))
borderColor = ((10, 120, 240))

# font
panelFont = pygame.font.Font(None, size=16)
panelFontColor = "white"

# file to pull answers from
filename = ""

# text and scrolling info
beginX = 10
beginY = 10
charSpacing = 10
textOffset = 0
lineSpacing = 5

# data to be blitted
blitUserMatrix = None
surfacesValuesRendered = []