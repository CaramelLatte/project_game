import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CLOCK_TICK = 60


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
gameState = "title"
font = pygame.font.SysFont("Arial", 16)

locations = {"test": "assets/world/testmapbig.png"}
encounterRates = {"frequent": 1000, "medium": 2500, "rare": 5000, "none": 0}
testTown = pygame.image.load(locations["test"]).convert()
scene_pos_x = 0
scene_pos_y = 0


class Entity:
  def __init__(self, img, x, y, imgStartX, imgStartY, width, height, hp, mp, strength, defense, intelligence, spirit, luck, exp):
    self.img = pygame.image.load(img).convert()
    self.x = x
    self.y = y
    self.coords = [x, y]
    self.imgSlice = (imgStartX, imgStartY, width, height)
    self.stats = {"hp": hp, "mp": mp, "strength": strength, "defense": defense, "intelligence": intelligence, "spirit": spirit, "luck": luck, "exp": exp}

  
  def draw(self, screen):
    screen.blit(self.img, (self.coords[0], self.coords[1]), self.imgSlice)

class Player(Entity):
  def __init__(self, img, x, y, imgStartX, imgStartY, width, height, hp, mp, strength, defense, intelligence, spirit, luck, exp):
    super().__init__(img, x, y, imgStartX, imgStartY, width, height, hp, mp, strength, defense, intelligence, spirit, luck, exp)
    self.imgStartX = imgStartX
    self.imgStartY = imgStartY
    self.width = width
    self.height = height
    self.moving = ""
    self.facing = "s"
    self.pixels_per_action = 16
    self.pixels_per_frame = 1
    self.frame = 0
    self.images = {"n": [(self.imgStartX,self.imgStartY+48, width, height), (self.imgStartX+16,self.imgStartY+48, width, height), (self.imgStartX+32,self.imgStartY+48, width, height)], "s": [(self.imgStartX, self.imgStartY, width, height), (self.imgStartX + 16, self.imgStartY, width, height), (self.imgStartX+32, self.imgStartY, width, height)], "w": [(self.imgStartX, self.imgStartY+16, width, height), (self.imgStartX+16, self.imgStartY+16, width, height), (self.imgStartX+32, self.imgStartY+16, width, height)], "e": [(self.imgStartX, self.imgStartY+32, width, height), (self.imgStartX+16, self.imgStartY+32, width, height), (self.imgStartX+32, self.imgStartY+32, width, height)]}
    
  def move(self):
    global scene_pos_x
    global scene_pos_y
    if self.moving == "":
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w] or keys[pygame.K_UP]:
        # self.y -= 2
        scene_pos_y += 2
        self.moving = "n"
        self.facing = self.moving
        self.pixels_per_action -= 2
      elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        # self.y += 2
        scene_pos_y -= 2
        self.moving = "s"
        self.pixels_per_action -= 2

      elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        # self.x -= 2
        scene_pos_x += self.pixels_per_frame
        self.moving = "w"
        self.pixels_per_action -= self.pixels_per_frame
      elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        # self.x += 2
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
      self.pixels_per_action = 16
      self.moving = ""
      

    self.coords = [self.x, self.y]
    
  def draw(self, screen):
    self.move()
    if self.pixels_per_action >= 8:
      self.frame = 1
    elif self.pixels_per_action >= 1:
      self.frame = 2
    else:
      self.frame = 0
    self.imgSlice = self.images[self.facing][self.frame]
    screen.blit(self.img, self.coords, self.imgSlice)

# class Spritesheet:
#   def __init__(self, filepath):
#     self.sheet = pygame.image.load(filepath).convert()
  
#   def image_at(self, rectangle):
#     rect = pygame.Rect(rectangle)
#     image = pygame.Surface(rect.size).convert()
#     image.blit(self.sheet, (0,0), rect)
#     return image
  
#   def images_at(self, rectangle):
#     return [self.image_at(rectangle) for rect in rectangle]

#   def load_strip(self, rect, image_count):
#     tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
#     return self.images_at(tups)

# class Map:
#   def __init__(self, image, encounters = "none"):
#     self.image = pygame.image.load(image)
#     self.encounters = encounters

    

    
player = Player('assets/world/spritesheet.png',(SCREEN_WIDTH/2),(SCREEN_HEIGHT/2),0,128,16,16,30,0,0,0,0,0,0,0)
entities = []
# spritesheet = Spritesheet('assets/world/spritesheet.png')
# image = spritesheet.image_at((0,0,16,16))

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
    # image = spritesheet.image_at((0,144,16,16))
    # screen.blit(image, (0,0))



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

