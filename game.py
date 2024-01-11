import pygame
import math
import random
import character
import block
import score
import obstacle
import time
import os

def load_sprite_sheet(folder, action):
    """ Loads a sprite sheet image

    Args:
        folder (String): directory where the sprite sheet is.
        action (String): sprite sheet image file.

    Returns:
        pygame.image: returns the sprite sheet as a pygame image.
    """
    sprite_sheet = pygame.image.load(folder + "/" + action + ".png").convert_alpha()
    
    return sprite_sheet

def get_sprite_list(width, height, sheet, color_key):
    """ Modifies a sprite sheet into a list of sprites.

    Args:
        width (int): width of the surface where sprite will be blit to.
        height (int): height of the surface where sprite will be blit to.
        sheet (pygame.image): the sprite
        color_key (pygame.Color): the color within the surface that will be made transparent 

    Returns:
        list: a list containing each sprite within the sprite sheet.
    """
    sprite_list = []
    for i in range(0, sheet.get_width(), width):
        sprite_surface = pygame.Surface((width, height)).convert_alpha()
        sprite_surface.blit(sheet, (0, 0), (i, 0, width, height))
        sprite_surface = pygame.transform.scale2x(sprite_surface)
        sprite_surface.set_colorkey(color_key)
        sprite_list.append(sprite_surface)
        
    return sprite_list

def load_block(x, y, width, height, sheet):
    """ Loads a block surface

    Args:
        x (int): x-coordinate of area of sheet to draw
        y (int): y_coordinate of area of sheet to draw
        width (int): width of area of sheet to draw
        height (int): height of area of sheet to draw
        sheet (pygame.image): block images.

    Returns:
        pygame.Surface: returns the desired image for the block.
    """
    block_surface = pygame.Surface((width, height)).convert_alpha()
    block_surface.blit(sheet, (0, 0), (x, y, width, height))
    
    return pygame.transform.scale2x(block_surface)

def load_background(background_name, screen_width):
    """ Loads the background

    Args:
        background_name (String): name of background file.
        screen_width (int): width of the screen.

    Returns:
        background (pygame.image): the image background.
        tiles (int): the number of background tiles to blit.
        bg_width (int): the width of the background image.
    """
    background = pygame.image.load(background_name).convert_alpha()
    bg_width = background.get_width()
    tiles = math.ceil(screen_width / bg_width) + 1 #so that this will work with any size background image.
    
    return background, tiles, bg_width
        
def load_obstacles(obstacles, dist_between_blocks):
    """ Obstacle generation and deletion.

    Args:
        obstacles (list): a list of type Obstacle
        dist_between_blocks (int): the distance between each subsequent obstacle.

    Returns:
        list: a list of the new obstacles to be generated in the game.
    """
    for o in obstacles:
        if o.rect.x + 100 < 0:
            obstacles.remove(o)
            rand = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + dist_between_blocks)
            obstacles.append(obstacle.Obstacle(rand, SCREEN_HEIGHT - GROUND_BLOCK_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_SPEED))
            
    return obstacles

def return_game_state(obstacles, player, game_state):
    """ Monitors the state of the game (start, playing, game_over)

    Args:
        obstacles (list): A list of the currently present in the game.
        player (Player): The player of the game.
        game_state (String): The current state of the game

    Returns:
        String: The new state of the game.
    """
    if game_state == "start":
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.mixer.music.unload()
            return "playing"
        else:
            return "start"
    
    if game_state == "game_over":
        return "game_over"
        
    for o in obstacles:
        if o.collision(player):
            sound_effect("die.wav")
            return "game_over"
    return "playing"
    
def draw(screen, ground, player, obstacles, scoreboard, game_state, space_bar, start_menu_font):
    """ Draws all components to the screen.

    Args:
        screen (pygame.display): The display
        ground (list): A list of blocks representing the ground.
        player (Player): The player
        obstacles (list): A list of type Obstacles.
        scoreboard (Scoreboard): The scoreboard
        game_state (String): The current state of the game.
        space_bar (pygame.Surface): Surface of the spacebar image. 
        start_menu_font (pygame.font): Font for the text in the starting screen.
    """
    for g in ground:
        g.draw(screen)
        
    if game_state == "start":
        start_menu_text = "Press Space to Start"
        start_menu_font = pygame.font.Font("fonts/" + start_menu_font, 20)
        start_menu_surface = start_menu_font.render(start_menu_text, True, (0,0,0))
        start_menu_surface_rect = start_menu_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 140))
        screen.blit(start_menu_surface, start_menu_surface_rect)
        space_bar_rect = space_bar.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        screen.blit(space_bar, space_bar_rect)
        
    if game_state != "start":
        player.draw(screen)
        screen.blit(scoreboard.getText(), (scoreboard.rect.x, scoreboard.rect.y))
        for obstacle in obstacles:
            obstacle.draw(screen)

def game_over_text(scoreboard):
    """ Draws the text for the game over screen

    Args:
        scoreboard (Scoreboard): The scoreboard.
    """
    game_over_font = pygame.font.Font("fonts/font1.ttf", 20)
    game_over_text = game_over_font.render("You Scored: {}".format(scoreboard.score), True, (0,0,0))
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
    play_again_text = game_over_font.render("Press the Spacebar to play again.", True, (0,0,0))
    play_again_text_rect = play_again_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(play_again_text, play_again_text_rect)
    
def update_score(scoreboard, obstacles, player):
    """ Updates the score of the scoreboard

    Args:
        scoreboard (Scoreboard): The scoreboard.
        obstacles (list): list of type Obstacle.
        player (Player): the player.
    """
    for o in obstacles:
        if o.rect.x + OBSTACLE_WIDTH < player.rect.x and not o.getSeen():
            scoreboard.incrementScore()
            if scoreboard.getScore() % 10 == 0:
                sound_effect("point.wav")
            scoreboard.updateText()
            o.setSeen(True)

def move(player, obstacles, scoreboard, ground, game_state):
    """ Moves all components

    Args:
        player (Player): The player
        obstacles (list): list of type Obstacle.
        scoreboard (Scoreboard): the Scoreboard
        ground (list): list of type Block representing the ground.
        game_state (String): The current state of the game.
    """
    if game_state == "playing":
        for o in obstacles:
            o.setSpeed((-(scoreboard.getScore() + 30) // 10) - scoreboard.getScore() / 10)
            o.move()
        player.loop(60, ground)

def reset_game(player, scoreboard):
    """ Resets the game

    Args:
        player (Player): the Player of the game.
        scoreboard (Scoreboard): The scoreboard.

    Returns:
        list: the starting list of type Obstacle.
    """
    player.rect.x, player.rect.y = PLAYER_START_X, PLAYER_START_Y
    scoreboard.score = 0
    obstacles = [obstacle.Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_BLOCK_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_SPEED), 
                 obstacle.Obstacle(SCREEN_WIDTH + random.randint(RAND_DIST_BETWEEN_BLOCKS[0], RAND_DIST_BETWEEN_BLOCKS[1]), 
                          SCREEN_HEIGHT - GROUND_BLOCK_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_SPEED)]
    
    return obstacles

def lobby_music(music, volume):
    """ Plays the lobby music.

    Args:
        music (String): The name of the music file.
        volume (int): The volume as a ratio of the original volume
    """
    pygame.mixer.music.load("sounds/" + music + ".mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)
    
def spacebar_animation(spacebar, x, y, width, height):
    """ Creates a surface for the starting page spacebar

    Args:
        spacebar (pygame.Surface): The surface of the spacebar sprite
        x (int): x-coordinate of area of spacebar to be drawn
        y (int): y-coordinate of area of spacebar to be drawn.
        width (int): width of area of spacebar to be drawn.
        height (int): height of area of spacebar to be drawn.

    Returns:
        pygame.Surface: The surface of the spacebar to be drawn on the window.
    """
    space_bar_surface = pygame.Surface((318, 120)).convert_alpha()
    space_bar_surface.set_colorkey(BLACK)
    space_bar_surface.blit(spacebar, (0, 0), (x, y, width, height))
    return space_bar_surface

def sound_effect(sound_effect):
    """ Plays the sound effects for the game.

    Args:
        sound_effect (File): The file name of the sound effect.
    """
    pygame.mixer.music.unload()
    pygame.mixer.music.load("sounds/" + sound_effect)
    pygame.mixer.music.play()

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
INFO = pygame.display.Info()
SCREEN_WIDTH = INFO.current_w * 0.5
SCREEN_HEIGHT = INFO.current_h * 0.5
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Endless Running Game')

#constants
BLACK = (0, 0, 0)
RAND_DIST_BETWEEN_BLOCKS = [250, 500] # [start, end]
GROUND_BLOCK_HEIGHT, GROUND_BLOCK_WIDTH = 96, 96
PLAYER_START_X, PLAYER_START_Y = 100, 200
PLAYER_WIDTH, PLAYER_HEIGHT = 32, 32
PLAYER_MAX_HEIGHT = 100 # y_pos of player at highest point of jump.
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 25, 48
OBSTACLE_SPEED = 5
SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT = 100, 25
SCOREBOARD_X, SCOREBOARD_Y = 650, 25
LOBBY_MUSIC_VOLUME = 0.1
SPACE_BAR_DIMENSIONS = [135, 230, 318, 120] # [x, y, width, height]
GAME_OVER_BUFFER = 0.5 # wait time after game is over.
        
def main():
    #object initialisation
    clock = pygame.time.Clock()
    running = True
    player = character.Character(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
    ground = [block.Block(b, int(SCREEN_HEIGHT) - GROUND_BLOCK_HEIGHT, GROUND_BLOCK_WIDTH, GROUND_BLOCK_HEIGHT) for b in range(0, int(SCREEN_WIDTH), GROUND_BLOCK_WIDTH)]
    obstacles = [obstacle.Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_BLOCK_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_SPEED), 
                 obstacle.Obstacle(SCREEN_WIDTH + random.randint(RAND_DIST_BETWEEN_BLOCKS[0], RAND_DIST_BETWEEN_BLOCKS[1]), 
                          SCREEN_HEIGHT - GROUND_BLOCK_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_SPEED)]
    scoreboard = score.Scoreboard(SCREEN_WIDTH - (2 * SCOREBOARD_WIDTH), SCOREBOARD_Y + 10, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT, 20)
    background, tiles, bg_width = load_background("backgrounds/nature.jpeg", SCREEN_WIDTH)
    game_state = "start"
    spacebar = pygame.transform.scale_by(load_sprite_sheet("other", "space_bar"), 0.5)
    spacebar_surface = spacebar_animation(spacebar, SPACE_BAR_DIMENSIONS[0], SPACE_BAR_DIMENSIONS[1], SPACE_BAR_DIMENSIONS[2], SPACE_BAR_DIMENSIONS[3]) 
    lobby_music("runner_game_music", LOBBY_MUSIC_VOLUME)

    #game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game_state = return_game_state(obstacles, player, game_state)
        
        #draw background
        for i in range(tiles):    
            screen.blit(background, (i * bg_width, 0))

        if game_state == "playing":
            update_score(scoreboard, obstacles, player)
            obstacles = load_obstacles(obstacles, RAND_DIST_BETWEEN_BLOCKS[1])    
            move(player, obstacles, scoreboard, ground, game_state) 
            
        if game_state == "game_over":
            game_over_text(scoreboard)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                time.sleep(GAME_OVER_BUFFER) #buffer after game is over so that game over screen is displayed properly.
                player.set_y_vel(0)
                player.set_fall_count(0)
                player.falling = True
                obstacles = reset_game(player, scoreboard)
                game_state = "playing"
                scoreboard.updateText()
        
        draw(screen, ground, player, obstacles, scoreboard, game_state, spacebar_surface, "font1.ttf")

        pygame.display.update()
           
        clock.tick(60)
        
    pygame.quit()


        