''' CLASS for text input boxes, of the Matrix Calculator 
    * used for matrix dimensions plus user manually entering matrix values
    * allows for numerous instances of text boxes to be created 

'''


import pygame, pygame_textinput

# is the textbox class; each textbox will be instantiated from this
class Textbox:

    # declares new Pygame Rectangle objects. the parameters are x-coord, y-coord, width, height, font, max length and allowed characters
    # maxLength and allowedChars are needed because the user can only enter specific characters, and a specific amount of them
    # maxLength will likely be 7 because there could be a 3-digit over a 3-digit number in a fraction
    # allowedChars should typically be only numbers, decimals, and fraction slashes within a matrix.
    # for dimension textboxes, those should be only numbers
    def __init__(self, x, y, width, height, font, maxLength = None, allowedChars = None):
        self.rect = pygame.Rect(x, y, width, height)
        
        # pygame_textinput has the TextInputVisualizer (visualizes text)
        self.textinput =  pygame_textinput.TextInputVisualizer(font_object=font)

        # Boolean to tell if a textbox object is currently active or not
        self.active = False

        # validation variable to ensure the user enters proper data
        self.allowedChars = allowedChars
    
    # is called when an event occurs, like when the user clicks or presses a key
    # also validates input when the user enters data
    def handleEvents(self, events):
        # IF a textbox is active, then it will update its text based on the event.
        # for example, if textbox is active, then when the user presses a key that textbox updates with that key
        if self.active:
            self.textinput.update(events)

        # validates input type
        if self.allowedChars:
            filteredText = ""
            for char in self.textinput.value:
                if char in self.allowedChars:
                    filteredText += char 
            self.textinput.value = filteredText
        
        # validates input length
        if self.maxLength is not None and len(self.textinput.value) > self.maxLength:

            # truncates any extra letters immediately if the entry is max length
            self.textinput.value = self.textinput.value[:self.maxLength]

    # draws the textbox on the screen. the parameters go: surface, color, Rectangle object
    # the textbox will have a colored border around it when it is active
    '''
    This is the flow of the "draw" function: 
    * Draws background rectangle > draws border outline > blits text surface (self.textinput.surface) into textbox
    * Displayed with the later "pygame.display.flip()"
    '''
    def draw(self, surface):
        # draws the main textbox itself. fills it with white
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        
        # sets the border color depending on if the textbox is active
        if self.active:
            color = (0, 255, 255)
        else:
            color = (150, 150, 150)
        
        # draws the textbox rectangle with a border width/stroke of 2 pixels, using the specified border color
        pygame.draw.rect(surface, color, self.rect, 2)

        # draws the data onto the screen. format goes as follows:
        # "surface" is the target surface to copy ONTO. "self.textinput.surface" is the surface to copy FROM
        # "self.textinput.surface" automatically creates a surface every frame from user events
        # the last parameter is (x,y) coords of where to copy the data; in this case, the top left of the textbox
        surface.blit(self.textinput.surface, (self.rect.x + 5, self.rect.y + 5) )

    # returns Boolean based on if the user clicks on the textbox
    def clickedInside(self, pos):
        return self.rect.collidepoint(pos)


