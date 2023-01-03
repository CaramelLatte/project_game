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
    self.imgs = []
    self.coords = coords
    self.selected = None
    self.options = options
    self.set_color()
    self.draw_background()
    self.write_options()

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

  def write_options(self):

    for option in self.options:
      print(option)




