import pygame,csv,os
from math import floor
class Sprites:
  def __init__(self,size,file, impassible = None):
     self.file = file
     self.size = size
     self.sprites = self.generate_sheet()
     self.impassible = impassible

  def generate_sheet(self):

    len_sprt_x = self.size
    len_sprt_y = self.size
    sprt_rect_x = 0 
    sprt_rect_y = 0

    sheet = pygame.image.load(self.file).convert_alpha()
    sheet_rect = sheet.get_rect()
    sprites = []
    for i in range(0,sheet_rect.height-len_sprt_y,self.size):
        for i in range(0,sheet_rect.width-len_sprt_x,self.size):
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y))
            sprite = sheet.subsurface(sheet.get_clip())
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x

        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    return sprites

class Map:
  def __init__(self,csv, collision, startx, starty, spritesheet):
    self.csv = self.read_csv(csv)
    self.collision = self.read_csv(collision)
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

  def read_csv(self, filename):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    return map
  
  def draw_map(self, file):
    for idxy, list in enumerate(file):
      for idxx,item in enumerate(list):
        if item != '-1':
          sprite = self.spritesheet.sprites[int(item) - floor(int(item) / 16)]
          self.surface.blit(sprite, (idxx*16,idxy*16))



