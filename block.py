import pygame
import game

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        """ Defines a block.

        Args:
            x (int): the x position of the block
            y (int): the y position of the block.
            width (int): the width of the block.
            height (int): the height of the block.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.sprite_sheet = game.load_sprite_sheet("terrain", "Terrain")
        self.sprite = game.load_block(96, 0, 48, 48, self.sprite_sheet)
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, surface):
        """ Draw the block onto the screen

        Args:
            surface (Surface): The surface where the block is drawn on.
        """
        surface.blit(self.sprite, (self.rect.x, self.rect.y))
    
            
            
    
    

    
