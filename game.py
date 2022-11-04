import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CLOCK_TICK = 60


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
gameState = "Overworld"


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
    
  def move(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      self.y -= 2
    if keys[pygame.K_s]:
      self.y += 2
    if keys[pygame.K_a]:
      self.x -= 2
    if keys[pygame.K_d]:
      self.x += 2
    self.coords = [self.x, self.y]
    
  def draw(self, screen):
    self.move()
    screen.blit(self.img, self.coords, self.imgSlice)

    
player = Player('assets/entities/rpgcritters2.png',0,0,0,0,50,50,30,0,0,0,0,0,0,0)
entities = [player]


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()


  if gameState == "Overworld":
    screen.fill("black")
    for entity in entities:
      entity.draw(screen)



  else:
    pass

  pygame.display.update()
  clock.tick(CLOCK_TICK)

