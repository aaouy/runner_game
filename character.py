import pygame
import game 

class Character(pygame.sprite.Sprite):
    #constants
    GRAVITY = 1
    SPEED = 3
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height) -> None:
        """ Class that defines a player

        Args:
            x (int): x position of player
            y (int): y position of player
            width (int): width of player
            height (int): height of player
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.__x_vel = 0
        self.__y_vel = 0
        self.__fall_count = 0
        self.__jumping = False
        self.sprite_sheet = game.load_sprite_sheet("sprites", "run")
        self.sprite_list = game.get_sprite_list(game.PLAYER_WIDTH, game.PLAYER_HEIGHT, self.sprite_sheet, game.BLACK)
        self.sprite = self.sprite_list[0]
        self.animation_count = 0
        self.mask = pygame.mask.from_surface(self.sprite)
        self.falling = True
        
    def descend(self):
        """ Descending movement of player
        """
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.__y_vel += 1.25
    
    def move(self, dx, dy):
        """ Moves the player

        Args:
            dx (int): horizontal speed
            dy (int): horizontal speed
        """
        self.rect.y += dy
        self.rect.x += dx
    
    def loop(self, fps, objects):
        """ Combines this class' other methods

        Args:
            fps (int): FPS game runs at
            objects (Block): Objects to detect collision with (ground)
        """
        self.jump("jump.wav")
        self.descend()
        self.fall(fps)
        self.move(self.__x_vel, self.__y_vel)
        self.collision(objects)
        
    def fall(self, fps):
        """ Falling movement of the player.

        Args:
            fps (int): FPS game runs at
        """
        self.__y_vel += min(1, (self.__fall_count / fps) * self.GRAVITY)
        self.__fall_count += 1
        if not self.falling:
            self.falling = True
    
    def jump(self, sound):
        """ Jumping mechanism of player

        Args:
            sound (String): Name of jumping sound file
        """
        if (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]) and not self.falling:
                pygame.mixer.music.load("sounds/" + sound)
                pygame.mixer.music.play()
                self.__y_vel = -self.GRAVITY * 6
    
    def collision(self, rectangles):
        """ Collision mechanism of player

        Args:
            rectangles (Block): objects player potentially can collide with.
        """
        for r in rectangles:
            if pygame.sprite.collide_mask(self, r):
                self.rect.bottom = r.rect.top
                self.__fall_count = 0
                if self.falling:
                    self.falling = False
            
    def draw(self, surface):
        """ Draws the player

        Args:
            surface (pygame.Surface): Surface where player is drawn on.
        """
        self.update_sprite()
        surface.blit(self.sprite, (self.rect.x, self.rect.y))
    
    def update(self):
        """ Makes player's rectangle position matches its sprite position
        """
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def update_sprite(self):
        """ Updates sprite based on its current action.
        """
        if self.__jumping:
            self.sprite_sheet = game.load_sprite_sheet("sprites", "jump")
        elif self.__fall_count != 0:
            self.sprite_sheet = game.load_sprite_sheet("sprites", "fall")
        else:
            self.sprite_sheet = game.load_sprite_sheet("sprites", "run")
        
        self.sprite_list = game.get_sprite_list(32, 32, self.sprite_sheet, game.BLACK)
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(self.sprite_list)
        self.sprite = self.sprite_list[sprite_index]
        self.animation_count += 1
        self.update()
    
    def set_y_vel(self, val):
        """ Sets y-velocity

        Args:
            val (int): y-velocity 
        """
        self.__y_vel = val
    
    def set_fall_count(self, val):
        """ Sets fall count

        Args:
            val (int): fall count
        """
        self.__fall_count = val
  
            
        
        
            
            
            
        
        
        
        
        
    
        
        
        
