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

        self.mob_wave = 1
        #Starts first wave of mobs
        self.mob_spawn_time = 0
        #Time since last mob spawn, will increase as game goes on
        self.mob_spawn_interval = 1
        #Ticks between each spawn
        self.dt = 0
        #time past since last frame update, ensures smooth movement
        self.player_death_time = None
        #this variable is the amoutn of time the moment the player died, player has no died yet, so it is set to none.

      
    def load_data(self):
        
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.cactus_img = pg.image.load(path.join(self.img_folder, 'cactus.png')).convert_alpha()
        self.healthbox_img = pg.image.load(path.join(self.img_folder, 'red.png')).convert_alpha()
        self.speedboost_img = pg.image.load(path.join(self.img_folder, 'speed.png')).convert_alpha()
        self.turret_img = pg.image.load(path.join(self.img_folder, 'turret.png')).convert_alpha()
        self.s = False
        #S is a condition and placeholder detecking when the waves function is running, will open flag maps folder if running
        self.c = False
        self.map_data = []
        #Different map folder for different Gamemodes
        if self.s == True:
            self.load_data_w()
        if self.c == True:
            self.load_data_c()
    
        
      

        
    def load_data_w(self):
        
        map_folder = "Flag_Maps"
        map_files = [f for f in os.listdir(map_folder) if os.path.isfile(os.path.join(map_folder, f))]
        map_file_name = random.choice(map_files)
        with open(os.path.join(map_folder, map_file_name), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
     


    def load_data_c(self):
        
        map_folder = "Maps"
        map_files = [f for f in os.listdir(map_folder) if os.path.isfile(os.path.join(map_folder, f))]
        map_file_name = random.choice(map_files)
        with open(os.path.join(map_folder, map_file_name), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    

# If the condition s is true, choose a different map file from the flag_maps folder
    # Lists all of the map files in the chosen folder
 
            

            
 

    def new(self):
      
        

        self.cooldown = Timer(self)
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.power_up2 = pg.sprite.Group()
        self.cactus = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.turret = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mob_spawner = pg.sprite.Group()
    
       # self.spawners = pg.sprite.Group()
        
        self.pew_pews = pg.sprite.Group()
        #self.team = pg.sprite.Group()
        self.ammo = pg.sprite.Group()
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
                    Turret(self, col, row)
         
  


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
            if self.s:  # Check if s is True, will run waves (apocalypse) if true
                self.waves()
            self.mob_spawn_time += self.dt#Keeps track of when the time is to spawn the next mob, updates it prettymuch
            if self.player.hitpoints <= 0:
            # If the player is dead, set playing to False to exit the game loop
            #Copied and modified from Chaptgpt

                self.player_death_time = pg.time.get_ticks() / 1000
                self.draw()
                self.playing = False

                
            
    

                   
                
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
        self.draw_text(self.screen, str(self.player.hitpoints), 100, GREEN, WIDTH/2 - 400, 0)
       
        if self.player.hitpoints == 30:
            self.draw_text(self.screen, str(self.player.hitpoints), 100, RED, WIDTH/2 - 400, 0)
        
        elif self.player.hitpoints <= 50:
                #Changes color (yellow) based on health of the player in the elif statment if self.hitpoints is less than or equal to 50.
                self.draw_text(self.screen, str(self.player.hitpoints), 100, YELLOW, WIDTH/2 - 400, 0)
                    #Changes color (red) based on health of the player in the elif statment if self.hitpoints is less than or equal to 30, gives a low health warning.
        if self.player.hitpoints <= 30:  
            self.draw_text(self.screen, str(self.player.hitpoints), 100, RED, WIDTH/2 - 400, 0)
            self.draw_text(self.screen, str("Warning, Low Health"), 100, RED, WIDTH/2 - -100, 0)
        if self.c is not False:
            self.draw_text(self.screen, str(self.player.coin_count), 100, YELLOW, WIDTH/2 - -400, 600)
            self.draw_text(self.screen, str("Coins"), 100, YELLOW, WIDTH/2 - -200, 600)
    

        

        

        if self.player.coin_count == 5:
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, "You win!", 100, WHITE, WIDTH/2, HEIGHT/2)
        if self.s and self.player.hitpoints == 0 and self.player_death_time is not None:
            #Prints out how many secodns the player survived for
         
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, f"Time of death (Seconds): {self.player_death_time}", 24, WHITE, WIDTH/2 - 32, 80)
            self.playing = False

          

 


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

    def menu(self):
        self.player_death_time = None
        #Menu is displayed
        #Lines of code from 226-260 were copied from Chaptgpt and modified
        menu_displayed = True
        while menu_displayed:
            self.screen.fill(BGCOLOR)
            #Draws the gamemodes
            self.draw_text(self.screen, "Choose an option:", 24, WHITE, WIDTH/2, HEIGHT/2 - 50)
            self.draw_text(self.screen, "C - Collect the Coins", 24, WHITE, WIDTH/2, HEIGHT/2)
            self.draw_text(self.screen, "W - Apocalypse Mode, For how many seconds can you survive!", 24, WHITE, WIDTH/2, HEIGHT/2 + 50)
         
      
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                #Checks the key that the user chooses, will run the gamemode method if true
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        menu_displayed = False
                        self.collect_the_coin()
                        self.c == True
                        self.s == False
                    
                        self.new()
                        self.run()
                    
                        
                    
                #Checks the key that the user chooses, will run the gamemode method if true     
                    if event.key == pg.K_w:
                        menu_displayed = False
                        self.waves()
                        self.s == True  # Set self.s for selection, will run apocalypse mode
                        self.c == False
                       
                        self.new()
                        self.run()
                        
                        
                        
                     

                        
                #Checks the key that the user chooses, will run the gamemode method if true
             
                    else:
                        print("""Wrong choice!               
                              """)
                        #g.quit()
                        
            
           
        pg.display.flip()
    def collect_the_coin(self):
 
        self.load_data_c()
       
        #Load_data_c-loads the maps in the maps folder
    
        

    def waves(self):
        self.s = True
        self.load_data_w()
        #loads map from flag_mas folder
    
    # 5- Mob spawns every 5 ticks
        spawn_interval = 5
    #Copied and modified from Chaptpgt
    # Check if it's time to spawn mobs
        if self.mob_spawn_time >= spawn_interval:
            #Checks if the spawn time is greater than the time interval
            for i in range(self.mob_wave):
            # Will run the loop if this is true-mob_wave-the number of mobs in each wave, will slowly increase
                valid_position = False
                #Loop searches for valid_position for the mob to spawn in, no valid position yet for the mob to spawn, will be set to true if a valid position is found
                while not valid_position:
                    mob_x = randint(0, WIDTH // TILESIZE - 1)
                    mob_y = randint(0, HEIGHT // TILESIZE - 1)
                    #Generates random coordinates for the mob to spawn in
                # This checks if the position is not a wall, will spawn a mob if not a wall
                    if not any(isinstance(sprite, Wall) for sprite in self.all_sprites if sprite.rect.collidepoint(mob_x * TILESIZE, mob_y * TILESIZE)):
                        valid_position = True
                        #valid position will be set to true if not a wall
                Mobc(self, mob_x, mob_y)
                #Creates instances of the Mobc class
        
        # Increases the wave of mobs
            self.mob_wave += 1
        
        # Spawn time between each mob
            self.mob_spawn_time = 0
    
    #This updates the spawn time
   
        self.mob_spawn_time += self.dt
        

 


        
      

        
        
       
        
     
        
        # Set the wave number to the saved value
        
        






       
        


 
    

g = Game()


g.menu()

while True:

    g.new()
    g.run()
    g.all_sprites.update()

