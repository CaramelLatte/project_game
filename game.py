import pygame
import random
from spritesheet import *
from math import floor
from entity import *
from globalvars import *

pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
gameState = "title"
font = pygame.font.SysFont("Arial", SPRITE_PIXELS)
scene_pos = [(SPRITE_PIXELS * 0) * SCALE, (SPRITE_PIXELS * -2) * SCALE]

locations = {"test": "assets/world/test.png"}
encounterRates = {"frequent": 1000, "medium": 2500, "rare": 5000, "none": 0}
sounds = {"bonk": pygame.mixer.Sound("assets/sounds/bonk.ogg")}
bonksound = pygame.mixer.Sound("assets/sounds/bonk.ogg")

spritesheet = Sprites(SPRITE_PIXELS,'assets/world/spritesheet.png', [13])
testTown = Map('mapbuild/test1.csv','mapbuild/test2.csv', 10, 10, spritesheet)
currentMap = testTown
entity_layer = pygame.Surface((currentMap.wpix, currentMap.hpix))
entity_layer.set_colorkey((0,0,0))




player = Player({"s": [spritesheet.sprites[120], spritesheet.sprites[121],spritesheet.sprites[122]], "n": [spritesheet.sprites[165], spritesheet.sprites[166], spritesheet.sprites[167]], "e":[spritesheet.sprites[150], spritesheet.sprites[151], spritesheet.sprites[152]], "w": [spritesheet.sprites[135], spritesheet.sprites[136], spritesheet.sprites[137]]}, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), {100, 20, 15, 15, 7, 10, 10, 100})

testNPC = Entity({"s": [spritesheet.sprites[123], spritesheet.sprites[124],spritesheet.sprites[125]], "n": [spritesheet.sprites[168], spritesheet.sprites[169], spritesheet.sprites[170]], "e":[spritesheet.sprites[153], spritesheet.sprites[154], spritesheet.sprites[155]], "w": [spritesheet.sprites[138], spritesheet.sprites[139], spritesheet.sprites[140]]}, (10 * (SPRITE_PIXELS*SCALE),10*(SPRITE_PIXELS*SCALE)), {1,1,1,1,1,1,1,1}, 100,300)

npc_entities = [testNPC]
enemy_party = []

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
    currentMap.surface = pygame.transform.scale(currentMap.surface, (currentMap.wpix * SCALE, currentMap.hpix * SCALE))
    screen.blit(currentMap.surface, (scene_pos[0], scene_pos[1]))
    

    #####################################################MOVE AND DRAW ENTITIES
    entity_layer = pygame.Surface((currentMap.wpix, currentMap.hpix))
    entity_layer.set_colorkey((0,0,0))
    for entity in npc_entities:
      entity.draw(currentMap, entity_layer, spritesheet)
    screen.blit(entity_layer, [scene_pos[0], scene_pos[1]])
    scene_pos = player.draw(screen, currentMap, spritesheet, scene_pos[0], scene_pos[1])

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