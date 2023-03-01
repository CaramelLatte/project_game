import pygame,csv,os
from math import floor
class Sprites:
  def __init__(self,size,file, impassible = None, interactable = None):
     self.file = file
     self.size = size
     self.sprites = self.generate_sheet()
     self.impassible = impassible
     self.interactable = interactable

  def generate_sheet(self):

    len_sprt_x = self.size
    len_sprt_y = self.size
    sprt_rect_x = 0 
    sprt_rect_y = 0

    sheet = pygame.image.load(self.file).convert_alpha()
    sheet_rect = sheet.get_rect()
    sprites = []
    for i in range(0,(sheet_rect.height-len_sprt_y)+16,self.size):
        for i in range(0,sheet_rect.width-len_sprt_x,self.size):
          sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y))
          sprite = sheet.subsurface(sheet.get_clip())
          sprites.append(sprite)
          sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    return sprites

class Map:
  def __init__(self, csv, collision, startx, starty, spritesheet, effect=None):
    self.csv = self.read_csv(csv)
    self.collision = self.read_csv(collision)
    self.effect = self.read_csv(effect)
    self.startx = startx
    self.starty = starty
    self.spritesheet = spritesheet
    self.w = len(self.csv[0])
    self.wpix = self.w * 16
    self.h = len(self.csv)
    self.hpix = self.h * 16
    self.surface = pygame.Surface((self.wpix, self.hpix))
    self.draw_map(self.csv)
    self.draw_map(self.collision)
    self.draw_map(self.effect)

  def read_csv(self, filename):
    if filename == None:
      return
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    return map
  
  def draw_map(self, file):
    if file == None:
      return
    for idxy, list in enumerate(file):
      for idxx,item in enumerate(list):
        if item != '-1':
          sprite = self.spritesheet.sprites[int(item) - floor(int(item) / 16)]
          self.surface.blit(sprite, (idxx*16,idxy*16))

class UI:
  def __init__(self, spritesheet, font, height, width, colorkey, options=None, coords=(0,0)):
    self.spritesheet = spritesheet
    self.font = font
    self.height = height
    self.width = width
    self.colorkey = colorkey
    self.surface = pygame.Surface((self.width, self.height))
    self.surface.set_colorkey((0,0,0))
    self.imgs = []
    self.coords = coords
    self.selected = 0
    self.options = options
    self.cursor_timeout = 0
    self.timeout = 15
    self.state = None
    self.state_window = None
    self.set_color()
    self.draw_background()
    self.write_menu()

  def set_color(self):
    if self.colorkey == "light":
      self.imgs = [self.spritesheet.sprites[0],self.spritesheet.sprites[1],self.spritesheet.sprites[2],self.spritesheet.sprites[19],self.spritesheet.sprites[20],self.spritesheet.sprites[21],self.spritesheet.sprites[38],self.spritesheet.sprites[39],self.spritesheet.sprites[40]]
    if self.colorkey == "medium":
      self.imgs = [self.spritesheet.sprites[57],self.spritesheet.sprites[58],self.spritesheet.sprites[59],self.spritesheet.sprites[76],self.spritesheet.sprites[77],self.spritesheet.sprites[78],self.spritesheet.sprites[95],self.spritesheet.sprites[96],self.spritesheet.sprites[97]]
    if self.colorkey == "dark":
      self.imgs = [self.spritesheet.sprites[114],self.spritesheet.sprites[115],self.spritesheet.sprites[116],self.spritesheet.sprites[133],self.spritesheet.sprites[134],self.spritesheet.sprites[135],self.spritesheet.sprites[152],self.spritesheet.sprites[153],self.spritesheet.sprites[154]]

  def draw_background(self):
    
    for idxy in range(int(self.height / 16)):
      for idxx in range(int(self.width / 16)):
        if idxy == 0:
          if idxx == 0:
            self.surface.blit(self.imgs[0], (idxx*16, idxy*16))
          elif (idxx*16) + 16 < self.width:
            self.surface.blit(self.imgs[1], (idxx*16, idxy*16))
          elif (idxx*16) + 16 == self.width:
            self.surface.blit(self.imgs[2], (idxx*16, idxy*16))
        elif (idxy*16)+16 < self.height:
          if idxx == 0:
            self.surface.blit(self.imgs[3], (idxx*16, idxy*16))
          elif (idxx*16) + 16 < self.width:
            self.surface.blit(self.imgs[4], (idxx*16, idxy*16))
          elif (idxx*16) + 16 == self.width:
            self.surface.blit(self.imgs[5], (idxx*16, idxy*16))
        elif (idxy*16)+16 == self.height:
          if idxx == 0:
            self.surface.blit(self.imgs[6], (idxx*16, idxy*16))
          elif (idxx*16)+16 < self.width:
            self.surface.blit(self.imgs[7], (idxx*16, idxy*16))
          elif (idxx*16)+16 == self.width:
            self.surface.blit(self.imgs[8], (idxx*16, idxy*16))
    if self.state == None:
      pass
    else:
      ui = pygame.Surface((480,120))
      for idxy in range(int(ui.get_height() / 16)):
        for idxx in range(int(ui.get_width() / 16)):
          if idxy == 0:
            if idxx == 0:
              self.surface.blit(self.imgs[0], (idxx*16, idxy*16))
            elif (idxx*16) + 16 < self.width:
              self.surface.blit(self.imgs[1], (idxx*16, idxy*16))
            elif (idxx*16) + 16 == self.width:
              self.surface.blit(self.imgs[2], (idxx*16, idxy*16))
          elif (idxy*16)+16 < self.height:
            if idxx == 0:
              self.surface.blit(self.imgs[3], (idxx*16, idxy*16))
            elif (idxx*16) + 16 < self.width:
              self.surface.blit(self.imgs[4], (idxx*16, idxy*16))
            elif (idxx*16) + 16 == self.width:
              self.surface.blit(self.imgs[5], (idxx*16, idxy*16))
          elif (idxy*16)+16 == self.height:
            if idxx == 0:
              self.surface.blit(self.imgs[6], (idxx*16, idxy*16))
            elif (idxx*16)+16 < self.width:
              self.surface.blit(self.imgs[7], (idxx*16, idxy*16))
            elif (idxx*16)+16 == self.width:
              self.surface.blit(self.imgs[8], (idxx*16, idxy*16))
              
                  
  def write_menu(self, ally_party=None, enemy_party=None):
    option_list = None
    if self.state == None:
      option_list = self.options
      for idx, option in enumerate(self.options):
        if idx <= 3:
          option_x = 32
          option_y = 16+(idx*16)
          option_font = self.font.render(option, True, (42,46,43))
          self.surface.blit(option_font, (option_x, option_y) )
    elif self.state == "Attack":
      option_list = enemy_party
      for idx, enemy in enumerate(enemy_party):
        if idx < 4:
          option_x = 32
          option_y = 16+(idx*16)
        elif idx < 8:
          option_x = 112
          option_y = 16+(idx%4)*16
        else:
          option_x = 192
          option_y = 16+(idx%4)*16
        option_font = self.font.render(enemy.name, True, (42, 46, 63))
        self.surface.blit(option_font, (option_x, option_y))
    elif self.state == "Defend":
      self.state = None
    elif self.state == "Spell":
      self.state = None
    elif self.state == "Item":
      self.state = None
    selector = self.font.render(">", True, (42,46,43))

    if self.cursor_timeout > 0:
      self.cursor_timeout -= 1
    if self.cursor_timeout == 0:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if self.selected == len(option_list) - 1:
          pass
        else: 
          self.selected += 1
          self.cursor_timeout += self.timeout
      elif keys[pygame.K_UP] or keys[pygame.K_w]:
        if self.selected == 0:
          pass
        else:
          self.selected -= 1
          self.cursor_timeout += self.timeout
      elif keys[pygame.K_RETURN]:
        if self.state == None:
          self.state = self.options[self.selected]
          self.selected = 0 
        elif self.state == "Attack":
          self.state = None
          self.selected = 0
          for idx, ally in enumerate(ally_party):
            if ally.active == True:
              if idx == len(ally_party)-1:
                ally_party[0].active = True
                ally.active = False
                
              else:
                ally_party[idx+1].active = True
                ally.active = False
                break
          print(enemy_party, "/n", enemy_party[self.selected])
          enemy_party[self.selected].stats["hp"] = 0
            
        self.cursor_timeout += self.timeout
    if self.selected < 4:
      self.surface.blit(selector,(16,(16+(self.selected*16))))
      
    elif self.selected < 8:
      self.surface.blit(selector,(32+64,(16+(self.selected%4)*16)))
      
    else:
      self.surface.blit(selector,(48+128, (16+(self.selected%4)*16)))




