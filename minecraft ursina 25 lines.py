from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app, grass_texture, stone_texture, sky_texture, arm_texture, punch_sound, block_pick = Ursina(), load_texture('assets/grass_block.png'), load_texture('assets/stone_block.png'), load_texture('assets/skybox.png'), load_texture('assets/arm_texture.png'), Audio('assets/punch_sound', loop=False, autoplay=False), 1 # import textures and sound files
def update():
    global block_pick
    hand.active() if held_keys['left mouse'] or held_keys['right mouse'] else hand.passive()
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
class Voxel(Button):# when you click on a voxel (like a block) it places another voxel
    def __init__(self, position=(0,0,0), texture=grass_texture): super().__init__(parent = scene, position = position, model = 'assets/block', origin_y = 0.5, texture = texture, color = color.color(0, 0, random.uniform(0.9, 1)), scale=0.5)
    def input(self, key):
        if self.hovered:
            if key ==  'left mouse down':
                if block_pick == 1: voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2: voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
            if key == 'right mouse down': punch_sound.play(), destroy(self) # destroy block if right clicksd
class Sky(Entity):
    def __init__(self): super().__init__(parent = scene, model = 'sphere', texture = sky_texture, scale = 150, double_sided=True)
class Hand(Entity):
    def __init__(self): super().__init__(parent = camera.ui, model = 'assets/arm', texture = arm_texture, scale = 0.2, rotation = Vec3(150, -10, 0), position = Vec2(0.4, -0.6))
    def active(self): self.position = Vec2(0.3, -0.5)
    def passive(self): self.position = Vec2(0.4, -0.6)
for z in range(35):
    for x in range(35): voxel =  Voxel((x, 0, z))
player, sky, hand, app = FirstPersonController(), Sky(), Hand(), app.run()
