from spritesheet import *
from globalvars import *

spritesheet = Sprites(SPRITE_PIXELS,'assets/world/spritesheet.png', [13,69], [89])

hero = {"s": [spritesheet.sprites[120], spritesheet.sprites[121],spritesheet.sprites[122]], "n": [spritesheet.sprites[165], spritesheet.sprites[166], spritesheet.sprites[167]], "e":[spritesheet.sprites[150], spritesheet.sprites[151], spritesheet.sprites[152]], "w": [spritesheet.sprites[135], spritesheet.sprites[136], spritesheet.sprites[137]]}

girl = {"s": [spritesheet.sprites[123], spritesheet.sprites[124],spritesheet.sprites[125]], "n": [spritesheet.sprites[168], spritesheet.sprites[169], spritesheet.sprites[170]], "e":[spritesheet.sprites[153], spritesheet.sprites[154], spritesheet.sprites[155]], "w": [spritesheet.sprites[138], spritesheet.sprites[139], spritesheet.sprites[140]]}, (6 * (SPRITE_PIXELS*SCALE),10*(SPRITE_PIXELS*SCALE)), 300,300, {1: "Hi!", 2: "Hi, again!", 3: "Why do you keep talking to me?"}

skeleton = {"e": [spritesheet.sprites[156]]}