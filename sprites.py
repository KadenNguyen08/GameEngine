#This file was created by Kaden Nguyen
#Appreciation to Chris Bradfield
import pygame as pg
from settings import *
from utils import *
from random import choice
import math
from os import path
vec =pg.math.Vector2
# needed for animated sprite
SPRITESHEET = "theBell.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# needed for animated sprite
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
       
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

        
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image.fill(GREEN)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
        self.moneybag = 0
        self.speed = 300
        self.status = ""
        self.hitpoints = 100
        self.cooling = False
        #sets the initial value of coin_count
        self.coin_count = 0
        self.pos = vec(0,0)
        print(self.hitpoints)
        self.flag_count = 0


    def get_keys(self):
        self.vx, self.vy = 0, 0 
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_e]:
            print("trying to shoot...")
            self.pew()
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    def pew(self):
        # Calculate direction based on player's orientation or any other logic
        direction = vec(1, 0)  # Example direction (to the right)
        p = PewPew(self.game, self.rect.x, self.rect.y)


    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # made possible by Aayush's question!
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                #Adds to coin score
                self.coin_count += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                effect = choice(POWER_UP_EFFECTS)
                self.game.cooldown.cd = 5
                self.cooling = True
                print(effect)
                print(self.cooling)
            if str(hits[0].__class__.__name__) == "PowerUp2":
                print(hits[0].__class__.__name__)
                self.speed += 100
            if str(hits[0].__class__.__name__) == "Mob2":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                self.hitpoints -= 1
                print(self.hitpoints)
                if self.status == "Invincible":
                    print("you can't hurt me")
            #Collisions for Cactus here
            if str(hits[0].__class__.__name__) == "Cactus":
                   # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                self.hitpoints -= 1
            #Collisions for Healthbox here
            if str(hits[0].__class__.__name__) == "HealthBox":
                self.hitpoints += 50
                #Adds 50 points to player health if player collides
            #Collisions for Speedboost here
            if str(hits[0].__class__.__name__) == "SpeedBoost":
                #adds 300 to player speed
                self.speed += 300
            if str(hits[0].__class__.__name__) == "Bullet":
                self.hitpoints -= 25
                #Adds 50 points to player health if player collides
            
 
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom              

                   
                        
     
    def update(self):
        self.get_keys()
        # self.power_up_cd.ticking()
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        if self.game.cooldown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.bullets, True)
 


 
          
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")

class Flag(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    pass

        
class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y, ):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print("I created a pew pew...")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        # if hits:
        #     if str(hits[0].__class__.__name__) == "Coin":
        #         self.moneybag += 1
 

    def update(self):
        self.collide_with_group(self.game.mobs, True)
        self.rect.y -= self.speed
        # pass

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE



class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class PowerUp2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_up2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
#new cactus class
class Cactus(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.cactus_img
        self.rect = self.image.get_rect()
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        # self.health = MOB_HEALTH
#The New Speedboost is located here.
class SpeedBoost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        #Classified as a coin
        pg.sprite.Sprite.__init__(self, self.groups)
        #initizalies groups
        self.game = game
        #Define game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.speedboost_img
        #defines self.image
        self.rect = self.image.get_rect()
        #defines self.rect
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        #sets poisitions
#The New Healthbox Class is located here.
class HealthBox(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        #Classified in the coins group
        pg.sprite.Sprite.__init__(self, self.groups)
        #Intializes the group
        self.game = game
        #Defines self.game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.healthbox_img
        #Defines the self.image
        self.rect = self.image.get_rect()
        #defines self.rect
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        #Defines positions and speed
       
        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # self.image = self.game.mob_img
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
        self.mob_hitpoints = 100
        if self.mob_hitpoints == 0:
            self.cooling = True
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def collide_with_cactus(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.cactus, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
                self.mob_hitpoints -= 1
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.cactus, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
                self.mob_hitpoints -= 1
    def update(self):
        # pass
        # # self.rect.x += 1
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        
        # if self.rect.x < self.game.player.rect.x:
        #     self.vx = 100
        # if self.rect.x > self.game.player.rect.x:
        #     self.vx = -100    
        # if self.rect.y < self.game.player.rect.y:
        #     self.vy = 100
        # if self.rect.y > self.game.player.rect.y:
        #     self.vy = -100
        self.rect.x = self.x
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')


class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mob2hitpots = 100
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        self.flag_count = 0
        # added
        self.speed = 150
        self.chasing = False
        # self.health = MOB_HEALTH
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False

    def update(self):
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            # self.image = pg.transform.rotate(self.image, 45)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            # self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            # self.rect.center = self.hit_rect.center
            # if self.health <= 0:
            #     self.kill()
    def collide_with_group_mob2(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "PewPew":
                self.mob2hitpots -= 1
import pygame as pg

# Add this code after the existing classes in your script

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 10
        #Defeins velocity
        self.velocity = self.direction * self.speed

    def update(self):
      #Updates coordinates  
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
     


            
#new turret class
class Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.turret
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)  # Adjust color as needed
        self.rect = self.image.get_rect()
        self.image = game.turret_img
        self.rect.center = (x, y)
        self.fire_rate = 125  # This is the fire rate of the turret in miliseconds
        self.last_fire = pg.time.get_ticks()
        #keeps track of time from when the last bullet was fired
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def update(self):
        #gets the time in milliseconds
        now = pg.time.get_ticks()
        #calculates the time that has passed since the last bullet was fired, fires another bullet if the time that has 
        #passed is greater than or equal to the fire rate
        if now - self.last_fire >= self.fire_rate:
            # This line calculates the bullet's direction to the player
            direction = vec(self.game.player.rect.center) - vec(self.rect.center)
            #Creates a vector from the turret to the player.
            #Ensures that the bullet travels at a constant speed regardless of distance
            direction = direction.normalize()
            # Creates an instance of the bullet class
            Bullet(self.game, self.rect.centerx, self.rect.centery, direction)
            #allows the turret to track time since shooting
            self.last_fire = now

class Mob_Spawner(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_spawner
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)  # Adjust color as needed
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.fire_rate = 0  # This is the fire rate of the turret in miliseconds
        self.last_fire = pg.time.get_ticks()
        #keeps track of time from when the last bullet was fired
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def update(self):
    # Gets the time in milliseconds
        now = pg.time.get_ticks()
    # Calculates the time that has passed since the last mob was spawned,
    # spawns another mob if the time that has passed is greater than or equal to the fire rate
        if now - self.last_fire >= self.fire_rate:
        # Creates an instance of the mob class (Mob2)
            Mob2(self.game, self.rect.centerx, self.rect.centery)
        # Allows the turret to track time since spawning a mob
            self.last_fire = now

