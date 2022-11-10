import pygame
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CLOCK_TICK = 60


pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
scale = 2
clock = pygame.time.Clock()
gameState = "title"
font = pygame.font.SysFont("Arial", 16)

locations = {"test": "assets/world/test.png"}
encounterRates = {"frequent": 1000, "medium": 2500, "rare": 5000, "none": 0}
testTown = pygame.image.load(locations["test"]).convert()
testTown = pygame.transform.scale(testTown, (testTown.get_width() * scale, testTown.get_height() * scale))
scene_pos_x = -176 * scale
scene_pos_y = -160 * scale



class Entity:
  def __init__(self, imgs, x, y, hp, mp, strength, defense, intelligence, spirit, luck, exp):
    self.img = None
    self.imgs = imgs
    self.rect = None
    self.x = x
    self.y = y
    self.coords = [x, y]
    self.moving = ""
    self.facing = "s"
    self.pixels_per_action = 16 * scale
    self.pixels_per_frame = 1
    self.stats = {"hp": hp, "mp": mp, "strength": strength, "defense": defense, "intelligence": intelligence, "spirit": spirit, "luck": luck, "exp": exp}

  
  def draw(self, screen):
      self.move()
      if self.pixels_per_action >= 8:
        self.img = self.imgs[self.facing][1]
      elif self.pixels_per_action >= 1:
        self.img = self.imgs[self.facing][2]
      else:
        self.img = self.imgs[self.facing][0]
      self.img = pygame.transform.scale(self.img, (self.img.get_width() * scale, self.img.get_height() * scale))
      screen.blit(self.img, self.coords)

class Player(Entity):  
  def move(self):
    global scene_pos_x
    global scene_pos_y
    if self.moving == "":
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w] or keys[pygame.K_UP]:
        self.y -= 1
        scene_pos_y += 2
        self.moving = "n"
        self.facing = self.moving
        self.pixels_per_action -= 2
      elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        self.y += 1
        scene_pos_y -= 2
        self.moving = "s"
        self.pixels_per_action -= 2
      elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        self.x -= 1
        scene_pos_x += self.pixels_per_frame
        self.moving = "w"
        self.pixels_per_action -= self.pixels_per_frame
      elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        self.x += 1
        scene_pos_x -= self.pixels_per_frame
        self.moving = "e"
        self.pixels_per_action -= self.pixels_per_frame
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

      
class Map:
  def __init__(self, csv, exits=[]):
    self.csv = csv
    self.exits = exits
    

def sprite_sheet(size,file):

  len_sprt_x = size
  len_sprt_y = size
  sprt_rect_x = 0 
  sprt_rect_y = 0

  sheet = pygame.image.load(file).convert_alpha()
  sheet_rect = sheet.get_rect()
  sprites = []
  for i in range(0,sheet_rect.height-len_sprt_y,size):#rows
      for i in range(0,sheet_rect.width-len_sprt_x,size):#columns
          sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
          sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
          
          sprites.append(sprite)
          sprt_rect_x += len_sprt_x

      sprt_rect_y += len_sprt_y
      sprt_rect_x = 0
  return sprites
spritesheet = sprite_sheet(16,'assets/world/spritesheet.png')

player = Player({"s": [spritesheet[120], spritesheet[121],spritesheet[122]], "n": [spritesheet[165], spritesheet[166], spritesheet[167]], "e":[spritesheet[150], spritesheet[151], spritesheet[152]], "w": [spritesheet[135], spritesheet[136], spritesheet[137]]}, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 100, 20, 15, 15, 7, 10, 10, 100)
entities = []



while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if event.type == pygame.KEYDOWN and gameState == "title":
      gameState = "overworld"

  if gameState == "title":
    screen.fill((0,0,0))
    startSurface = font.render("Press any key to start", False, "white")
    screen.blit(startSurface, ((SCREEN_WIDTH - startSurface.get_width()) / 2, (SCREEN_HEIGHT - startSurface.get_height()) / 2))



  elif gameState == "overworld":
    screen.blit(testTown, (scene_pos_x,scene_pos_y))
    for entity in entities:
      entity.draw(screen)
    player.draw(screen)
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

