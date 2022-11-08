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

locations = {"test": "assets/world/testmap.png"}
encounterRates = {"frequent": 1000, "medium": 2500, "rare": 5000}
testTown = pygame.image.load(locations["test"]).convert()


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
    self.moving = False
    
  def move(self):
    self.moving = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      self.y -= 2
      self.moving = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      self.y += 2
      self.moving = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      self.x -= 2
      self.moving = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      self.x += 2
      self.moving = True

    self.coords = [self.x, self.y]
    
  def draw(self, screen):
    self.move()
    screen.blit(self.img, self.coords, self.imgSlice)

class Background:
  def __init__(self) -> None:
    self.width = 246
    self.height = 133



    
player = Player('assets/entities/rpgcritters2.png',0,0,0,0,50,50,30,0,0,0,0,0,0,0)
entities = [player]


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
    screen.blit(testTown, (0,0))
    for entity in entities:
      entity.draw(screen)
    if player.moving:
      randomBattleChance = random.randint(0, encounterRates["medium"])
      if randomBattleChance <= 5:
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

