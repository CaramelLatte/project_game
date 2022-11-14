import pygame
import random
from spritesheet import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CLOCK_TICK = 60
SPRITE_PIXELS = 16


pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
scale = 2
clock = pygame.time.Clock()
gameState = "title"
font = pygame.font.SysFont("Arial", 16)
scene_pos_x = ((SPRITE_PIXELS * 0) * scale)
scene_pos_y = ((SPRITE_PIXELS * -2) * scale)

locations = {"test": "assets/world/test.png"}
encounterRates = {"frequent": 1000, "medium": 2500, "rare": 5000, "none": 0}
sounds = {"bonk": pygame.mixer.Sound("assets/sounds/bonk.ogg")}
bonksound = pygame.mixer.Sound("assets/sounds/bonk.ogg")


class Entity:
  def __init__(self, imgs, coords, hp, mp, strength, defense, intelligence, spirit, luck, exp):
    self.img = None
    self.imgs = imgs
    self.rect = None
    self.x = 0
    self.y = 0
    self.coords = coords
    self.moving = ""
    self.facing = "s"
    self.pixels_per_action = 16 * scale
    self.pixels_per_frame = 1
    self.stats = {"hp": hp, "mp": mp, "strength": strength, "defense": defense, "intelligence": intelligence, "spirit": spirit, "luck": luck, "exp": exp}
  
  # def draw(self, screen):
  #     self.move()
  #     if self.pixels_per_action >= 8:
  #       self.img = self.imgs[self.facing][1]
  #     elif self.pixels_per_action >= 1:
  #       self.img = self.imgs[self.facing][2]
  #     else:
  #       self.img = self.imgs[self.facing][0]
  #     self.img = pygame.transform.scale(self.img, ((self.img.get_width() * scale) + 8, (self.img.get_height() * scale) + 8))
  #     screen.blit(self.img, self.coords)
      

class Player(Entity):
  def __init__(self, imgs, coords, hp, mp, strength, defense, intelligence, spirit, luck, exp):
    super().__init__(imgs, coords, hp, mp, strength, defense, intelligence, spirit, luck, exp)
    self.collision_timer = 60
    self.collision = False
  def update_coords(self, map):
    self.x = map.startx
    self.y = map.starty


  def draw(self, screen, map,sprites):
    self.move(map,sprites)
    if self.pixels_per_action >= 8:
      self.img = self.imgs[self.facing][1]
    elif self.pixels_per_action >= 1:
      self.img = self.imgs[self.facing][2]
    else:
      self.img = self.imgs[self.facing][0]
    self.img = pygame.transform.scale(self.img, ((self.img.get_width() * scale) + 8, (self.img.get_height() * scale) + 8))
    screen.blit(self.img, self.coords)

  def move(self, map, sprites):
    global scene_pos_x
    global scene_pos_y
    collision_check = map.collision
    collision_tiles = sprites.impassible
    if self.moving == "":
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w] or keys[pygame.K_UP]:
        if int(collision_check[self.y-1][self.x]) in collision_tiles:
          self.facing = "n"
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        else:
          self.y -= 1
          scene_pos_y += 2
          self.pixels_per_action -= 2
          self.moving = "n"
          self.facing = self.moving
      elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if int(collision_check[self.y+1][self.x]) in collision_tiles:
          self.facing = "s"
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        else:
          self.y += 1
          scene_pos_y -= 2
          self.pixels_per_action -= 2
          self.moving = "s"
          self.facing = self.moving
      elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if int(collision_check[self.y][self.x-1]) in collision_tiles:
          self.facing = "w"
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        else:
          self.x -= 1
          scene_pos_x += 2
          self.pixels_per_action -= 2
          self.moving = "w"
          self.facing = self.moving
      elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if int(collision_check[self.y][self.x+1]) in collision_tiles:
          self.facing = "e"
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        else:
          self.x += 1
          scene_pos_x -= 2
          self.pixels_per_action -= 2
          self.moving = "e"
          self.facing = self.moving
    elif self.pixels_per_action > 0:
      if self.moving == "n":
        self.pixels_per_action -= self.pixels_per_frame
        scene_pos_y += self.pixels_per_frame
        self.facing = self.moving
      if self.moving == "s":
        self.pixels_per_action -= self.pixels_per_frame
        scene_pos_y -= self.pixels_per_frame
        self.facing = self.moving
      if self.moving == "w":
        self.pixels_per_action -= self.pixels_per_frame
        scene_pos_x += self.pixels_per_frame
        self.facing = self.moving
      if self.moving == "e":
        self.pixels_per_action -= self.pixels_per_frame
        scene_pos_x -= self.pixels_per_frame
        self.facing = self.moving
    else:
      self.pixels_per_action = 16 * scale
      self.moving = ""


spritesheet = Sprites(16,'assets/world/spritesheet.png', [13])

testTown = Map('mapbuild/test1.csv','mapbuild/test2.csv', 10, 10, spritesheet)

player = Player({"s": [spritesheet.sprites[120], spritesheet.sprites[121],spritesheet.sprites[122]], "n": [spritesheet.sprites[165], spritesheet.sprites[166], spritesheet.sprites[167]], "e":[spritesheet.sprites[150], spritesheet.sprites[151], spritesheet.sprites[152]], "w": [spritesheet.sprites[135], spritesheet.sprites[136], spritesheet.sprites[137]]}, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 100, 20, 15, 15, 7, 10, 10, 100)

entities = []
currentMap = testTown

player.update_coords(currentMap)


while True:
  ####################################################EVENT CHECK
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if event.type == pygame.KEYDOWN and gameState == "title":
      gameState = "overworld"

  #######################################COOLDOWN CYCLING
  if player.collision is True:
    if player.collision_timer != 0:
      player.collision_timer -= 1
    else:
      player.collision = False
      player.collision_timer = 60
########################################## GAME STATE DRAW
  if gameState == "title":
    screen.fill((0,0,0))
    startSurface = font.render("Press any key to start", False, "white")
    screen.blit(startSurface, ((SCREEN_WIDTH - startSurface.get_width()) / 2, (SCREEN_HEIGHT - startSurface.get_height()) / 2))



  elif gameState == "overworld":
    screen.fill((0,0,0))
    currentMap.surface = pygame.transform.scale(currentMap.surface, (currentMap.wpix * scale, currentMap.hpix * scale))
    screen.blit(currentMap.surface, (scene_pos_x,scene_pos_y))
    #####################################################M MOVE AND DRAW ENTITIES
    for entity in entities:
      entity.draw(screen)
    player.draw(screen, currentMap, spritesheet)
    if player.moving != "":
      randomBattleChance = random.randint(0, encounterRates["medium"])
      if randomBattleChance < 0:
        gameState = "battle"




  elif gameState == "battle":
    screen.fill((0,0,0))
    backgroundSurface = pygame.image.load("assets/world/background.png")
    backgroundSurface = pygame.transform.scale(backgroundSurface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(backgroundSurface, (0,0))

  else:
    pass


  pygame.display.update()
  clock.tick(CLOCK_TICK)

