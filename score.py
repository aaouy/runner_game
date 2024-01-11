import pygame

class Scoreboard:
    def __init__(self, x, y, width, height, font_size):
        """ Defines the scoreboard of the game

        Args:
            x (int): x-position of the scoreboard.
            y (int): y-position of the scoreboard
            width (int): width of the scoreboard
            height (int): height of the scoreboard
        """
        self.score = 0
        self.rect= pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font("fonts/font1.ttf", font_size)
        self.text = self.font.render("Dodged: " + str(self.score), True, (0, 0, 0))
    
    def getText(self):
        """ Returns the text of the scoreboard

        Returns:
            pygame.font: The text of the scoreboard.
        """
        return self.text
    
    def updateText(self):
        """ Updates the text of the scorebard based on the current score.
        """
        self.text = self.font.render("Dodged: " + str(self.score), True, (0, 0, 0))

    def incrementScore(self):
        """ incremenets current score.
        """
        self.score += 1
        
    def getScore(self):
        """ Returns the current score.

        Returns:
            _type_: _description_
        """
        return self.score
    
        
  
    
    
       
    