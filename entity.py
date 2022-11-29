import pygame
from math import floor
from globalvars import *
import random
from soundlibrary import *

####################################################################################################################
########################################    ENTITY    ##############################################################
####################################################################################################################
class Entity:
  def __init__(self, imgs, coords, move_chance=None, move_cooldown=None, interactions=None):
    self.img = None
    self.imgs = imgs
    self.rect = None
    self.coords = coords
    self.x = self.coords[0] 
    self.y = self.coords[1]
    self.moving = ""
    self.facing = "s"
    self.move_chance = move_chance
    self.move_cooldown = move_cooldown
    self.move_cooldown_tick = move_cooldown
    self.pixels_per_action = SPRITE_PIXELS * SCALE
    self.pixels_per_frame = 1
    self.interactions = interactions
    self.interactions_counter = 1
  
  def map_coords(self):
      check_vals = (floor(self.x / (SPRITE_PIXELS*SCALE)), floor((self.y+2) /(SPRITE_PIXELS*SCALE)))
      return check_vals

  def check_collision(self, map, sprites):
    collision_check = map.collision
    collision_tiles = sprites.impassible
    movable_list = []
    check_vals = self.map_coords()
    if int(collision_check[check_vals[1]-1][check_vals[0]]) not in collision_tiles:
      movable_list.append("n")
    if int(collision_check[check_vals[1]+1][check_vals[0]]) not in collision_tiles:
      movable_list.append("s")
    if int(collision_check[check_vals[1]][check_vals[0]+1]) not in collision_tiles:
      movable_list.append("e")
    if int(collision_check[check_vals[1]][check_vals[0]-1]) not in collision_tiles:
      movable_list.append("w")
    return movable_list

  def move(self, currentMap, spritesheet):
    if self.move_chance != None:
      if self.moving == "" and self.move_cooldown_tick == self.move_cooldown:
        roll_to_move = random.randint(0, self.move_chance)
        if roll_to_move == 1:
          directions = self.check_collision(currentMap, spritesheet)
          direction = random.randint(0, (len(directions) - 1))      
          match directions[direction]:
            case "n":
              self.y -= 1
              self.pixels_per_action -= 2
              self.moving = "n"
              self.facing = self.moving
              self.move_cooldown -= 1
            case "s":
              self.y += 1
              self.pixels_per_action -= 2
              self.moving = "s"
              self.facing = self.moving
              self.move_cooldown -= 1
            case "e":
              self.x += 1
              self.pixels_per_action -= 2
              self.moving = "e"
              self.facing = self.moving
              self.move_cooldown -= 1
            case "w":
              self.x -= 1
              self.pixels_per_action -= 2
              self.moving = "w"
              self.facing = self.moving
              self.move_cooldown -= 1
      elif self.pixels_per_action > 0:
        if self.moving == "n":
          self.y -= 1
          self.pixels_per_action -= self.pixels_per_frame
          self.facing = self.moving
          self.move_cooldown -= 1
        if self.moving == "s":
          self.y += 1
          self.pixels_per_action -= self.pixels_per_frame
          self.facing = self.moving
          self.move_cooldown -= 1
        if self.moving == "w":
          self.x -= 1
          self.pixels_per_action -= self.pixels_per_frame
          self.facing = self.moving
          self.move_cooldown -= 1
        if self.moving == "e":
          self.x += 1
          self.pixels_per_action -= self.pixels_per_frame
          self.facing = self.moving
          self.move_cooldown -= 1
      else:
        self.pixels_per_action = SPRITE_PIXELS * SCALE
        self.move_cooldown_tick = self.move_cooldown
        self.moving = ""

  def draw(self, currentMap, layer, spritesheet):
      self.move(currentMap, spritesheet)
      if self.pixels_per_action >= 8:
        self.img = self.imgs[self.facing][1]
      elif self.pixels_per_action >= 1:
        self.img = self.imgs[self.facing][2]
      else:
        self.img = self.imgs[self.facing][0]
      self.img = pygame.transform.scale(self.img, ((self.img.get_width() * SCALE) + 8, (self.img.get_height() * SCALE) + 8))
      layer.blit(self.img, (self.x, self.y-18))
  
  def interacted_with(self):

    print(self.interactions[self.interactions_counter])
    if self.interactions_counter < len(self.interactions):
      self.interactions_counter += 1
####################################################################################################################


####################################################################################################################
########################################    PLAYER    ##############################################################
####################################################################################################################
class Player(Entity):
  def __init__(self, imgs, coords):
    super().__init__(imgs, coords)
    self.collision_timer = 60
    self.collision = False
  def update_coords(self, map):
    self.x = map.startx
    self.y = map.starty

  def looking_at(self):
    x = self.x
    y = self.y
    match self.facing:
      case "n":
        y -= 1 
      case "s":
        y += 1
      case "e":
        x += 1
      case "w":
        x -= 1
    return (x, y)
  def draw(self, screen, map,sprites, scene_pos_x, scene_pos_y, entities):
    update_scene = self.move(map,sprites,scene_pos_x, scene_pos_y, entities)
    if self.pixels_per_action >= 8:
      self.img = self.imgs[self.facing][1]
    elif self.pixels_per_action >= 1:
      self.img = self.imgs[self.facing][2]
    else:
      self.img = self.imgs[self.facing][0]
    self.img = pygame.transform.scale(self.img, ((self.img.get_width() * SCALE) + 8, (self.img.get_height() * SCALE) + 8))
    screen.blit(self.img, self.coords)
    return update_scene

  def move(self, map, sprites, scene_pos_x, scene_pos_y, entities):
    collision_check = map.collision
    collision_tiles = sprites.impassible
    interact_check = sprites.interactable
    npc_coords = []
    for npc in entities:
      npc_at = npc.map_coords()
      npc_coords.append(npc_at)
    if self.moving == "":
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w] or keys[pygame.K_UP]:
        self.facing = "n"
        looking_at = self.looking_at()
        check = int(collision_check[looking_at[1]][looking_at[0]])
        if check in collision_tiles:
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        elif looking_at in npc_coords or check in interact_check:
          pass
        else:
          self.y -= 1
          scene_pos_y += 2
          self.pixels_per_action -= 2
          self.moving = "n"
          # self.facing = self.moving
      elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        self.facing = "s"
        looking_at = self.looking_at()
        check = int(collision_check[looking_at[1]][looking_at[0]])
        if check in collision_tiles:
          self.facing = "s"
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        elif looking_at in npc_coords or check in interact_check:
          pass
        else:
          self.y += 1
          scene_pos_y -= 2
          self.pixels_per_action -= 2
          self.moving = "s"
          self.facing = self.moving
      elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        self.facing = "w"
        looking_at = self.looking_at()
        check = int(collision_check[looking_at[1]][looking_at[0]])
        if check in collision_tiles:
          self.facing = "w"
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        elif looking_at in npc_coords or check in interact_check:
          pass
        else:
          self.x -= 1
          scene_pos_x += 2
          self.pixels_per_action -= 2
          self.moving = "w"
          self.facing = self.moving
      elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        self.facing = "e"
        looking_at = self.looking_at()
        check = int(collision_check[looking_at[1]][looking_at[0]])
        if check in collision_tiles:
          self.facing = "e"
          self.collision = True
          if self.collision_timer == 60:
            pygame.mixer.Sound.play(sounds["bonk"])
        elif looking_at in npc_coords or check in interact_check:
          pass
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
      self.pixels_per_action = SPRITE_PIXELS * SCALE
      self.moving = ""
    return [scene_pos_x, scene_pos_y]

  def interact(self, map, sprites, entities):
    looking_at = self.looking_at()
    entity_check = map.collision
    interact_tiles = sprites.interactable 
    if int(entity_check[looking_at[1]][looking_at[0]]) in interact_tiles:
      print("clicked")
    
    for entity in entities:
      entity_coords = entity.map_coords()
      if entity_coords == looking_at:
        entity.interacted_with()
#############################################################################################################################

class BattlePartyMember(Entity):
  def __init__(self, imgs, stats):
    super().__init__(imgs)
    self.stats = stats

  def draw(self, screen):
    pass