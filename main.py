#This file was created by: Kaden Nguyen
# Enjoyed health bar, pewpews, speed boost    Disliked- no storyline or point to the game yet
#References-Mr. Cozort's Github, Chatgpt
'''Health Bar
   Speed Boost     
   Med Kit'''
import pygame as pg
from settings import *
from sprites import *
from utils import *
from random import randint
import sys
from os import path
from math import floor
from random import choice
import os
from random import choice
import random
from main import *
from sprites import Mobc
'''Beta Goals
  
1. More interesting enemies
2. Game Goal and End
3. More maps
Credits: Mr. Cozort's Github, Chatgpt

'''

class Game:

    def __init__(self):
  


        
       
        pg.init()
        pg.mixer.init()
      
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        self.playing = True
      
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.cactus_img = pg.image.load(path.join(self.img_folder, 'cactus.png')).convert_alpha()
        self.healthbox_img = pg.image.load(path.join(self.img_folder, 'red.png')).convert_alpha()
        self.speedboost_img = pg.image.load(path.join(self.img_folder, 'speed.png')).convert_alpha()
        self.turret_img = pg.image.load(path.join(self.img_folder, 'turret.png')).convert_alpha()
   
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        #defines map folder variable
        map_folder = "Maps"
        flag_map_folder = "flag_maps"

# Lists all of the map files in the folder, Copied from Chatgpt, modified
        map_files = [f for f in os.listdir(map_folder) if os.path.isfile(os.path.join(map_folder, f))]
        flag_map_files = [f for f in os.listdir(flag_map_folder) if os.path.isfile(os.path.join(flag_map_folder, f))]

# Randomly chooses a map Copied from Chatgpt, modified
        random_map_file = random.choice(map_files)
        random_flag_map_file = random.choice(map_files)

# Opens the random map file, Copied from Chatgpt, modified
        with open(os.path.join(map_folder, random_map_file), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
            def test_method(self):
                print("I can be called from Sprites...")


    def new(self):
     

        self.cooldown = Timer(self)
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.power_up2 = pg.sprite.Group()
        self.cactus = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.turret = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mob_spawner = pg.sprite.Group()
     
        #self.team = pg.sprite.Group()
        self.ammo = pg.sprite.Group
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob2(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'K':
                    PowerUp2(self, col, row)
                if tile == 'G':
                    Cactus(self, col, row)
                if tile == 'H':
                    HealthBox(self, col, row)
                if tile == 'S':
                    SpeedBoost(self, col, row)
                if tile == 'T':
                    Turret(self,col,row)

                if tile == 'A':
                    self.mobc = Mobc(self, col, row)

               
                if tile == 'U':
                    Mob(self, col, row)
                #aaaif tile == 'K':
                    #Teammate(self, col, row)
                    

                
                    
                    
    def run(self):

        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.places = 1
            self.events()
            self.update()
            self.draw()

                   
                
    def quit(self):
         pg.quit()
         sys.exit()
    def update(self):
    
        self.cooldown.ticking()
        self.all_sprites.update()
        self.walls.update()
        if self.player.hitpoints < 1:
            self.playing = False
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    
    def draw(self):
            self.screen.fill(BGCOLOR)

          
            self.all_sprites.draw(self.screen)
    
            self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH/2 - 32, 80)
            self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
            self.draw_text(self.screen, str(self.player.hitpoints), 100, WHITE, WIDTH/2 - 400, 0)
            self.draw_text(self.screen, str(self.mobc.mob2hitpots), 100, WHITE, WIDTH/2 - 300, 0)
            self.draw_text(self.screen, str(), 100, WHITE, WIDTH/2 - 400, 0)
            
  
            
            #Health symbol featured here
            #Coordines are 400,0
             #Changes color (green) based on health of the player in the elif statment if self.hitpoints is equal to or greater than 51.
            if self.player.hitpoints >= 51:
                self.draw_text(self.screen, str(self.player.hitpoints), 100, GREEN, WIDTH/2 - 400, 0)
            elif self.player.hitpoints <= 50:
                #Changes color (yellow) based on health of the player in the elif statment if self.hitpoints is less than or equal to 50.
                self.draw_text(self.screen, str(self.player.hitpoints), 100, YELLOW, WIDTH/2 - 400, 0)
                    #Changes color (red) based on health of the player in the elif statment if self.hitpoints is less than or equal to 30, gives a low health warning.
            if self.player.hitpoints <= 30:  
                self.draw_text(self.screen, str(self.player.hitpoints), 100, RED, WIDTH/2 - 400, 0)
                self.draw_text(self.screen, str("Warning, Low Health"), 100, RED, WIDTH/2 - -100, 0)
             #Checks if collect the coin is running, displays the coin count
            if self.collect_the_coin:
                self.draw_text(self.screen, str(self.player.coin_count), 100, YELLOW, WIDTH/2 - -400, 600)
            #Displays # of coins collected
                self.draw_text(self.screen, str("Coins"), 100, YELLOW, WIDTH/2 - -200, 600)
            #Checks if coin count is 5, then displays the screen
            if self.player.coin_count == 5:
                self.screen.fill(BGCOLOR)
                 #Displays "you win! here"
                self.draw_text(self.screen, "You win!", 100, WHITE, WIDTH/2, HEIGHT/2)
            if self.places == 0:
                self.screen.fill(BGCOLOR)
                self.draw_text(self.screen, "You died!", 100, WHITE, WIDTH/2, HEIGHT/2)

            #Displays when coin count is 5
        
           
            #Displays the player health here.
            pg.display.flip()
    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    def menu(self):

        #Menu is displayed
        #Lines of code from 226-260 were copied from Chaptgpt and modified
        menu_displayed = True
        while menu_displayed:
            self.screen.fill(BGCOLOR)
            #Draws the gamemodes
            self.draw_text(self.screen, "Choose an option:", 24, WHITE, WIDTH/2, HEIGHT/2 - 50)
            self.draw_text(self.screen, "C - Collect the Coins", 24, WHITE, WIDTH/2, HEIGHT/2)
            self.draw_text(self.screen, "F - Capture the Flag", 24, WHITE, WIDTH/2, HEIGHT/2 + 50)
            self.draw_text(self.screen, "T - Team Deathmatch", 24, WHITE, WIDTH/2, HEIGHT/2 + 100)
      
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                #Checks the key that the user chooses, will run the gamemode method if true
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        menu_displayed = False
                        self.new()
                        self.run()
                        self.collect_the_coin()
                    
                #Checks the key that the user chooses, will run the gamemode method if true     
                    elif event.key == pg.K_f:
                        self.capture_the_flag()
                        menu_displayed = False
                #Checks the key that the user chooses, will run the gamemode method if true
                    elif event.key == pg.K_t:
                    # Handle Team Deathmatsch option
                        pass  # This is a placeholder, no gamemode here yet

                # The menu will exit if any keys be pressed
                    else:
                        menu_displayed = False
            
           
        pg.display.flip()
    def collect_the_coin(self):
        #resets coin collection
        self.player.coin_count = 0
        

    def capture_the_flag(self):
        pass

    def team_deathmatch(self):
        pass




       
        



 
    

g = Game()
g.show_start_screen()

g.menu()
while True:
    
    g.new()
    g.run()
    g.all_sprites.update()

