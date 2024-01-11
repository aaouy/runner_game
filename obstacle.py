import pygame
from block import *
import game

class Obstacle(Block):
    def __init__(self, x, y, width, height, speed):
        """ Obstacle class, inherits from Block class.

        Args:
            x (int): x-position of the obstacle.
            y (int): y-position of the obstacle.
            width (int): width of obstacle
            height (int): height of obstacle
            speed (int): speed of obstacle
        """
        super().__init__(x, y, width, height)
        self.__speed = -speed
        self.__seen = False
        self.sprite = pygame.transform.scale_by(game.load_block(240, 0, 16, 48, self.sprite_sheet), 0.5)
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.collided = False
    
    def move(self):
        """ Moves the obstacle
        """
        self.rect.x += self.__speed

    def collision(self, player):
        """ Checks collision of obstacle with player

        Args:
            player (Player): the player

        Returns:
            bool: Returns True if collision has occured
        """
        if pygame.sprite.collide_mask(self, player) and not self.collided:
            self.collided = True
            return self.collided
    
    def stop(self):
        """ Defines player movement stopping
        """
        self.__speed = 0
    
    def setSpeed(self, speed):
        """ Sets player speed

        Args:
            speed (int): player speed
        """
        self.__speed = speed
            
    def setSeen(self, seen):
        """ Defines if the obstacle has passed the position of the player

        Args:
            seen (bool): True if obstacle has passed position of the player, otherwise False
        """
        self.__seen = seen
    
    def getSeen(self):
        """ Returns if obstacle has passed player position

        Returns:
            bool: Returns True if obstacle has passed position of player
        """
        return self.__seen