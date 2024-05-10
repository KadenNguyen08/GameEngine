class MobC(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mob2hitpots = 100
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        self.flag_count = 0
        self.speed = 150
        self.chasing = False
        self.fire_rate = 1000  # This is the fire rate of the turret in miliseconds
        self.last_fire = pg.time.get_ticks()
        self.flag = None  # Reference to the enemy flag carried by Mob2
        self.carried = False

    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False

    def update(self):
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.walls, 'y')
            flag_hits = pg.sprite.spritecollide(self, self.game.flags, False)
            if flag_hits:
                flag = flag_hits[0]
                if not flag.carried:
                    flag.pickup(self)

        # Check for collision with enemy flag
        if self.flag is None:
            flag_hits = pg.sprite.spritecollide(self, self.game.flags, False)
            if flag_hits:
                flag = flag_hits[0]
                if not flag.carried:
                    flag.pickup(self)
                    self.flag = flag
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
            Bullett(self.game, self.rect.centerx, self.rect.centery, direction)
            #allows the turret to track time since shooting
            self.last_fire = now

    def collide_with_group_mob2(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "PewPew":
                self.mob2hitpots -= 1

    def pickup_enemy_flag(self, flag):
        if self.flag is None:
            self.flag = flag
            self.flag.carried = True

    def drop_enemy_flag(self):
        if self.flag:
            self.flag.carried = False
            self.flag = None


    
