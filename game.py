import pygame
from globalvars import *
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", SPRITE_PIXELS)



import random
from spritesheet import *
from math import floor
from entity import *
import entitylibrary

locations = {"test": "assets/world/test.png"}
encounterRates = {"frequent": 1000, "medium": 2500, "rare": 5000, "none": 0}
spritesheet = Sprites(SPRITE_PIXELS,'assets/world/spritesheet.png', [13,69], [89])
testTown = Map('mapbuild/test1.csv','mapbuild/test2.csv', 10, 10, spritesheet)
currentMap = testTown
entity_layer = pygame.Surface((currentMap.wpix, currentMap.hpix))
entity_layer.set_colorkey((0,0,0))




player = Player(entitylibrary.hero, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

testNPC = Entity(entitylibrary.girl[0], entitylibrary.girl[1], entitylibrary.girl[2], entitylibrary.girl[3], entitylibrary.girl[4])

npc_entities = [testNPC]
enemy_party = []
ally_party = []

player.update_coords(currentMap)
gameState = "title"
scene_pos = [(SPRITE_PIXELS * 0) * SCALE, (SPRITE_PIXELS * -2) * SCALE]

while True:
  ####################################################EVENT CHECK
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if event.type == pygame.KEYDOWN and gameState == "title":
      gameState = "overworld"
    if event.type == pygame.KEYDOWN and gameState == "overworld":
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
        player.interact(currentMap, spritesheet, npc_entities)

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
    startSurface = FONT.render("Press any key to start", False, "white")
    screen.blit(startSurface, ((SCREEN_WIDTH - startSurface.get_width()) / 2, (SCREEN_HEIGHT - startSurface.get_height()) / 2))



  elif gameState == "overworld":
    screen.fill((0,0,0))
    currentMap.surface = pygame.transform.scale(currentMap.surface, (currentMap.wpix * SCALE, currentMap.hpix * SCALE))
    screen.blit(currentMap.surface, (scene_pos[0], scene_pos[1]))
    

    #####################################################MOVE AND DRAW ENTITIES
    entity_layer = pygame.Surface((currentMap.wpix, currentMap.hpix))
    entity_layer.set_colorkey((0,0,0))
    for entity in npc_entities:
      entity.draw(currentMap, entity_layer, spritesheet)
    screen.blit(entity_layer, [scene_pos[0], scene_pos[1]])
    scene_pos = player.draw(screen, currentMap, spritesheet, scene_pos[0], scene_pos[1], npc_entities)

    if player.moving != "":
      randomBattleChance = random.randint(0, encounterRates["medium"])
      if randomBattleChance < 10:
        gameState = "battle"




  elif gameState == "battle":
    screen.fill((0,0,0))
    backgroundSurface = pygame.image.load("assets/world/background.png")
    backgroundSurface = pygame.transform.scale(backgroundSurface, (SCREEN_WIDTH, floor(SCREEN_HEIGHT*.8)))
    screen.blit(backgroundSurface, (0,0))


    uiSurface = pygame.Surface((SCREEN_WIDTH, floor(SCREEN_HEIGHT/5)))
    uiSurface.fill("green")
    uiSurface.set_alpha(50)
    screen.blit(uiSurface, (0, floor(SCREEN_HEIGHT*.8)))


    enemySurface = pygame.Surface((SCREEN_WIDTH/2, SCREEN_HEIGHT*.8))
    enemySurface.fill("blue")
    enemySurface.set_alpha(100)
    screen.blit(enemySurface, (0,0))


    partySurface = pygame.Surface((SCREEN_WIDTH/2, SCREEN_HEIGHT*.8))
    partySurface.fill("red")
    partySurface.set_alpha(100)
    screen.blit(partySurface, (SCREEN_WIDTH/2, 0))

    
  else:
    pass


  pygame.display.update()
  CLOCK.tick(CLOCK_TICK)